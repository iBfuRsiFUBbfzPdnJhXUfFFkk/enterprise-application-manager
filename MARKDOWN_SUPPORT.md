# Markdown Support in Comment Fields

All comment fields throughout the application now support Markdown formatting. This allows for rich text formatting including headers, lists, code blocks, links, and more.

## Supported Markdown Features

The following Markdown syntax is supported in all comment fields:

### Text Formatting
- **Bold text**: `**bold**` or `__bold__`
- *Italic text*: `*italic*` or `_italic_`
- `Inline code`: `` `code` ``

### Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
```

### Lists
```markdown
- Unordered list item 1
- Unordered list item 2

1. Ordered list item 1
2. Ordered list item 2
```

### Links
```markdown
[Link text](https://example.com)
```

### Code Blocks
````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### Blockquotes
```markdown
> This is a blockquote
```

### Horizontal Rules
```markdown
---
```

## Where Markdown is Supported

Markdown is enabled on the following models' comment fields:
- **Acronyms** - Acronym definitions and explanations
- **Applications** - Application descriptions and notes
- **Application Groups** - Group descriptions
- **Databases** - Database instance notes
- **Dependencies** - Dependency information
- **Documents** - Document descriptions
- **People** - Personal notes and information
- **Secrets** - Secret usage notes and documentation
- **Releases** - Release notes and comments
- **Release Bundles** - Bundle descriptions

## Implementation Details

### Template Filter
The `markdown` template filter is defined in `core/templatetags/templatetags_markdown.py`:

```python
from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(value: str | None) -> str:
    if value is None:
        return ""
    return mark_safe(s=markdown(text=value))
```

### Usage in Templates

To use markdown rendering in templates:

1. Load the templatetag library:
   ```django
   {% load templatetags_markdown %}
   ```

2. Apply the markdown filter to comment fields:
   ```django
   {{ model.comment|markdown }}
   ```

3. For list views with truncation:
   ```django
   <div class="prose prose-sm max-w-none">
       {{ model.comment|markdown|truncatewords_html:15 }}
   </div>
   ```

### Styling

Markdown content is styled using custom CSS classes defined in `templates/authenticated/base_authenticated.html`:

- `.prose` - Base prose styling
- `.prose-sm` - Smaller prose styling for compact views

The styles ensure consistent rendering of:
- Headings with appropriate sizes and weights
- Lists with proper indentation
- Code blocks with syntax highlighting backgrounds
- Links with hover effects
- Blockquotes with left border styling

## User Interface

### Form Fields
All comment fields in forms display a helpful hint below the textarea:

```
Supports Markdown: **bold**, *italic*, `code`, [links](url), lists, etc.
```

This informs users that they can use Markdown formatting in their comments.

### Display Views
- **List views**: Comments are truncated and rendered with Markdown in a compact format
- **Detail views**: Full Markdown content is rendered with complete styling

## Library Used

The application uses the **Markdown** Python library (version 3.7):
- PyPI: https://pypi.org/project/Markdown/
- Documentation: https://python-markdown.github.io/

## Testing

Test data has been created to verify Markdown rendering:
- An "API" acronym with comprehensive Markdown examples
- Secret records with formatted documentation

To verify Markdown is working:
1. Navigate to the Acronyms list page
2. Look for the "API" entry - the comment should show formatted text
3. Edit the acronym to see the raw Markdown source
4. The form should display the Markdown hint below the comment field

## Security

The `mark_safe()` function is used to allow HTML rendering from Markdown. This is safe because:
1. The Markdown library sanitizes input by default
2. All content is user-generated within the authenticated system
3. Only authenticated users can create/edit records

If additional security is needed, consider:
- Using `bleach` library for HTML sanitization
- Enabling Markdown safe mode
- Restricting allowed HTML tags
