"""
Step 4: Create a block letter matching the image dimensions.
Generates a bold letter (default "S") on a white background to represent selection bias.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


def create_block_letter_s(
    height: int,
    width: int,
    letter: str = "S",
    font_size_ratio: float = 0.9
) -> np.ndarray:
    """
    Create a block letter image matching the specified dimensions.
    
    Parameters
    ----------
    height : int
        Height of the output image in pixels
    width : int
        Width of the output image in pixels
    letter : str
        Letter to render (default "S" for "Selection bias")
    font_size_ratio : float
        Ratio of font size relative to image size (default 0.9)
        Determines how large the letter appears in the image
    
    Returns
    -------
    block_letter : np.ndarray
        2D numpy array (height × width) with values in [0, 1]
        Black letter (0.0) on white background (1.0)
    """
    # Create a white background image
    img = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(img)
    
    # Calculate font size based on the smaller dimension
    font_size = int(min(height, width) * font_size_ratio)
    
    # Try to find a suitable bold font
    font = None
    
    # Common system font paths (cross-platform)
    font_paths = [
        # Windows
        "C:/Windows/Fonts/arialbd.ttf",  # Arial Bold
        "C:/Windows/Fonts/arial.ttf",    # Arial
        "C:/Windows/Fonts/calibrib.ttf", # Calibri Bold
        "C:/Windows/Fonts/timesbd.ttf",  # Times Bold
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    
    # Try to load a bold font
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except Exception:
                continue
    
    # If no font found, use default (bitmap font)
    if font is None:
        try:
            # Try to use a default truetype font
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            # Fall back to default bitmap font
            font = ImageFont.load_default()
    
    # Get text bounding box to center the letter
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position to center the letter
    x = (width - text_width) // 2 - bbox[0]
    y = (height - text_height) // 2 - bbox[1]
    
    # Draw the letter in black
    draw.text((x, y), letter, fill=0, font=font)
    
    # Convert PIL image to numpy array and normalize to [0, 1]
    # PIL image: 0 = black, 255 = white
    # After normalization: 0.0 = black, 1.0 = white
    # This matches the requirement: black letter (0.0) on white background (1.0)
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    return img_array

