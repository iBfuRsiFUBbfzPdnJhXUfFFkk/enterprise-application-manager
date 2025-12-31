import os
import subprocess
import tempfile
from io import BytesIO
from typing import Optional

from pdf2image import convert_from_bytes
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

MAX_EMBED_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_WIDTH = 2000
MAX_IMAGE_HEIGHT = 2000


def convert_docx_to_pdf(docx_bytes: bytes) -> Optional[bytes]:
    """Convert DOCX bytes to PDF bytes. Tries Microsoft Word first, then LibreOffice, then textutil."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "input.docx")
        pdf_path = os.path.join(tmpdir, "input.pdf")

        with open(docx_path, "wb") as f:
            f.write(docx_bytes)

        # Try Microsoft Word first (macOS via AppleScript)
        if os.path.exists("/Applications/Microsoft Word.app"):
            try:
                applescript = f'''
                tell application "Microsoft Word"
                    activate
                    open POSIX file "{docx_path}"
                    set doc to active document
                    save as doc file name "{pdf_path}" file format format PDF
                    close doc saving no
                    quit
                end tell
                '''
                result = subprocess.run(
                    ["osascript", "-e", applescript],
                    capture_output=True,
                    timeout=30,
                )
                if result.returncode == 0 and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        return f.read()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                pass

        # Try LibreOffice as fallback
        try:
            result = subprocess.run(
                ["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmpdir, docx_path],
                capture_output=True,
                timeout=30,
            )
            if result.returncode == 0 and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    return f.read()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass

        # Try macOS textutil as last resort (built-in, always available on macOS)
        try:
            result = subprocess.run(
                ["textutil", "-convert", "pdf", "-output", pdf_path, docx_path],
                capture_output=True,
                timeout=30,
            )
            if result.returncode == 0 and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    return f.read()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass

        return None


def create_text_content_page(text: str, filename: str) -> bytes:
    """Create a PDF page with text content from a file."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    story = []
    styles = getSampleStyleSheet()

    title = Paragraph(f"<b>{filename}</b>", styles["Heading1"])
    story.append(title)
    story.append(Spacer(1, 0.2 * inch))

    lines = text.split("\n")
    for line in lines:
        # Empty lines create spacing (like line breaks)
        if not line.strip():
            story.append(Spacer(1, 0.1 * inch))
        elif len(line) > 80:
            wrapped_lines = [line[i : i + 80] for i in range(0, len(line), 80)]
            for wrapped in wrapped_lines:
                para = Paragraph(f'<font name="Courier" size="8">{wrapped}</font>', styles["Normal"])
                story.append(para)
        else:
            para = Paragraph(f'<font name="Courier" size="8">{line}</font>', styles["Normal"])
            story.append(para)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def create_image_content_page(image_bytes: bytes, filename: str) -> bytes:
    """Create a PDF page with embedded image."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    story = []
    styles = getSampleStyleSheet()

    title = Paragraph(f"<b>{filename}</b>", styles["Heading1"])
    story.append(title)
    story.append(Spacer(1, 0.2 * inch))

    try:
        img = Image.open(BytesIO(image_bytes))

        if img.width > MAX_IMAGE_WIDTH or img.height > MAX_IMAGE_HEIGHT:
            img.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), Image.Resampling.LANCZOS)

        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        max_width = 6.5 * inch
        max_height = 8 * inch
        width_ratio = max_width / img.width
        height_ratio = max_height / img.height
        ratio = min(width_ratio, height_ratio)

        rl_image = RLImage(img_buffer, width=img.width * ratio, height=img.height * ratio)
        story.append(rl_image)

    except Exception:
        error_para = Paragraph("<i>Error: Unable to load image</i>", styles["Normal"])
        story.append(error_para)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def create_unsupported_file_page(filename: str, size: int, content_type: str, note: str = None) -> bytes:
    """Create a PDF page for unsupported file types showing metadata."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    story = []
    styles = getSampleStyleSheet()

    title = Paragraph(f"<b>{filename}</b>", styles["Heading1"])
    story.append(title)
    story.append(Spacer(1, 0.2 * inch))

    info_text = f"""
    <b>File Type:</b> {content_type}<br/>
    <b>File Size:</b> {format_file_size(size)}<br/>
    <br/>
    <i>This file type cannot be embedded in the PDF export.</i>
    """

    if note:
        info_text += f"<br/><br/><i>{note}</i>"

    para = Paragraph(info_text, styles["Normal"])
    story.append(para)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def merge_pdfs(pdf_bytes_list: list[bytes]) -> bytes:
    """Merge multiple PDF byte streams into a single PDF."""
    writer = PdfWriter()

    for pdf_bytes in pdf_bytes_list:
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    output_buffer = BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.getvalue()


def get_attachment_handler(content_type: str) -> str:
    """Determine how to handle an attachment based on content type."""
    if not content_type:
        return "unsupported"

    content_type_lower = content_type.lower()

    if content_type_lower.startswith("text/"):
        return "text"
    if content_type_lower in ("application/json", "application/xml"):
        return "text"
    if content_type_lower.startswith("image/"):
        return "image"
    if content_type_lower == "application/pdf":
        return "pdf"

    return "unsupported"


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def convert_pdf_to_images(pdf_bytes: bytes, max_pages: int = 50) -> list[Image.Image]:
    """Convert PDF bytes to a list of PIL images (one per page)."""
    import tempfile

    try:
        # Use /tmp/claude for temp files (sandbox-allowed directory)
        with tempfile.TemporaryDirectory(dir="/tmp/claude") as tmpdir:
            images = convert_from_bytes(
                pdf_bytes,
                dpi=150,
                fmt="png",
                use_pdftoppm=True,
                output_folder=tmpdir
            )
            # Limit number of pages to avoid memory issues
            return images[:max_pages]
    except Exception as e:
        print(f"PDF to image conversion error: {e}")
        import traceback
        traceback.print_exc()
        return []
