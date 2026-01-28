"""
Image similarity detection using perceptual hashing and SIFT features.

Perceptual hash (dhash) is stored in the database for quick lookups.
SIFT is used for detailed comparison between specific images.
"""
import io
from typing import Optional

import cv2
import numpy as np
from PIL import Image


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif'}


def is_image_file(filename: str) -> bool:
    """Check if filename is an image based on extension."""
    if not filename:
        return False
    ext = '.' + filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    return ext in IMAGE_EXTENSIONS


def compute_dhash(image_file, hash_size: int = 16) -> Optional[str]:
    """
    Compute difference hash (dhash) for an image.
    Returns a hex string representing the perceptual hash.

    dhash works by:
    1. Converting to grayscale
    2. Resizing to (hash_size+1, hash_size)
    3. Computing horizontal gradient (difference between adjacent pixels)
    4. Converting to binary based on whether left pixel > right pixel
    """
    try:
        image_file.seek(0)
        img = Image.open(image_file)

        # Convert to grayscale
        img = img.convert('L')

        # Resize to hash_size+1 x hash_size
        img = img.resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)

        # Convert to numpy array
        pixels = np.array(img)

        # Compute differences between adjacent pixels
        diff = pixels[:, 1:] > pixels[:, :-1]

        # Convert to hash
        hash_value = 0
        for bit in diff.flatten():
            hash_value = (hash_value << 1) | int(bit)

        image_file.seek(0)
        return format(hash_value, f'0{hash_size * hash_size // 4}x')
    except Exception:
        return None


def hamming_distance(hash1: str, hash2: str) -> int:
    """
    Calculate Hamming distance between two hex hashes.
    Lower distance = more similar images.
    """
    if not hash1 or not hash2 or len(hash1) != len(hash2):
        return -1

    # Convert hex to integers and XOR
    val1 = int(hash1, 16)
    val2 = int(hash2, 16)
    xor = val1 ^ val2

    # Count differing bits
    distance = bin(xor).count('1')
    return distance


def similarity_percentage(hash1: str, hash2: str, hash_size: int = 16) -> float:
    """
    Calculate similarity percentage between two hashes.
    Returns 0-100 where 100 is identical.
    """
    distance = hamming_distance(hash1, hash2)
    if distance < 0:
        return 0.0

    max_distance = hash_size * hash_size
    return ((max_distance - distance) / max_distance) * 100


def compute_sift_descriptors(image_file) -> Optional[np.ndarray]:
    """
    Extract SIFT descriptors from an image.
    Returns numpy array of descriptors or None if extraction fails.
    """
    try:
        image_file.seek(0)
        img_bytes = image_file.read()
        image_file.seek(0)

        # Decode image using OpenCV
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return None

        # Create SIFT detector
        sift = cv2.SIFT_create()

        # Detect keypoints and compute descriptors
        keypoints, descriptors = sift.detectAndCompute(img, None)

        return descriptors
    except Exception:
        return None


def compare_sift_images(file1, file2, threshold: float = 0.75) -> dict:
    """
    Compare two images using SIFT feature matching.

    Returns dict with:
    - matches: number of good matches
    - total_keypoints: average keypoints in both images
    - similarity_score: 0-100 score based on match ratio
    """
    desc1 = compute_sift_descriptors(file1)
    desc2 = compute_sift_descriptors(file2)

    if desc1 is None or desc2 is None:
        return {'matches': 0, 'total_keypoints': 0, 'similarity_score': 0}

    if len(desc1) < 2 or len(desc2) < 2:
        return {'matches': 0, 'total_keypoints': 0, 'similarity_score': 0}

    # Use FLANN-based matcher for efficiency
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Find matches using KNN
    matches = flann.knnMatch(desc1, desc2, k=2)

    # Apply Lowe's ratio test
    good_matches = []
    for match_pair in matches:
        if len(match_pair) == 2:
            m, n = match_pair
            if m.distance < threshold * n.distance:
                good_matches.append(m)

    # Calculate similarity score
    avg_keypoints = (len(desc1) + len(desc2)) / 2
    match_ratio = len(good_matches) / avg_keypoints if avg_keypoints > 0 else 0
    similarity_score = min(100, match_ratio * 100)

    return {
        'matches': len(good_matches),
        'total_keypoints': int(avg_keypoints),
        'similarity_score': round(similarity_score, 2)
    }


def find_similar_by_dhash(target_hash: str, all_hashes: list, threshold: int = 20) -> list:
    """
    Find images with similar dhash within threshold Hamming distance.

    Args:
        target_hash: The dhash to compare against
        all_hashes: List of (id, dhash) tuples
        threshold: Maximum Hamming distance (lower = stricter)

    Returns:
        List of (id, distance, similarity_pct) tuples sorted by distance
    """
    similar = []
    for doc_id, hash_value in all_hashes:
        if hash_value == target_hash:
            continue
        distance = hamming_distance(target_hash, hash_value)
        if 0 <= distance <= threshold:
            similarity = similarity_percentage(target_hash, hash_value)
            similar.append((doc_id, distance, similarity))

    return sorted(similar, key=lambda x: x[1])
