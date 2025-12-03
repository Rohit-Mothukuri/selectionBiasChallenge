"""
Create the final statistics meme by assembling all four panels.
Creates a professional four-panel visualization demonstrating selection bias.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


def create_statistics_meme(
    original_img: np.ndarray,
    stipple_img: np.ndarray,
    block_letter_img: np.ndarray,
    masked_stipple_img: np.ndarray,
    output_path: str,
    dpi: int = 150,
    background_color: str = "white"
) -> None:
    """
    Assemble all four panels into a professional four-panel statistics meme.
    
    The meme demonstrates selection bias through visual metaphor:
    - Panel 1 (Reality): Original image representing the true population
    - Panel 2 (Your Model): Stippled image representing data collection
    - Panel 3 (Selection Bias): Block letter representing systematic missing data pattern
    - Panel 4 (Estimate): Masked stippled image showing the biased estimate
    
    Parameters
    ----------
    original_img : np.ndarray
        Original grayscale image as 2D array (height, width) with values in [0, 1]
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1]
    block_letter_img : np.ndarray
        Block letter image as 2D array (height, width) with values in [0, 1]
    masked_stipple_img : np.ndarray
        Masked stippled image as 2D array (height, width) with values in [0, 1]
    output_path : str
        Path where the final meme PNG file will be saved
    dpi : int
        Resolution (dots per inch) for the output image. Default 150.
        Higher values (200-300) produce publication-quality images.
    background_color : str
        Background color for the meme. Default "white".
        Can be any valid matplotlib color name (e.g., "pink", "lightgray").
    
    Returns
    -------
    None
        The function saves the meme as a PNG file at output_path.
    """
    # Get image dimensions (all should be the same)
    h, w = original_img.shape
    
    # Helper function to ensure image has correct dimensions
    def ensure_size(img: np.ndarray, target_h: int, target_w: int, name: str) -> np.ndarray:
        """Resize image if it doesn't match target dimensions."""
        if img.shape != (target_h, target_w):
            print(f"Warning: {name} has shape {img.shape}, expected {(target_h, target_w)}")
            print(f"  Resizing {name} to match original image dimensions...")
            from PIL import Image
            img_pil = Image.fromarray((img * 255).astype(np.uint8))
            img_resized = img_pil.resize((target_w, target_h), Image.Resampling.LANCZOS)
            img_array = np.array(img_resized, dtype=np.float32) / 255.0
            return img_array
        return img
    
    # Ensure all images have the same dimensions
    stipple_img = ensure_size(stipple_img, h, w, "stipple_img")
    block_letter_img = ensure_size(block_letter_img, h, w, "block_letter_img")
    masked_stipple_img = ensure_size(masked_stipple_img, h, w, "masked_stipple_img")
    
    # Create figure with four panels side by side
    fig = plt.figure(figsize=(20, 7), facecolor=background_color)
    
    gs = GridSpec(1, 4, figure=fig, wspace=0.0, hspace=0.0,
                  left=0.0, right=1.0, top=0.97, bottom=0.03)
    
    labels = ["Reality", "Your Model", "Selection Bias", "Estimate"]
    panel_data = [original_img, stipple_img, block_letter_img, masked_stipple_img]
    
    # Create each panel
    for i, (label, img_data) in enumerate(zip(labels, panel_data)):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(img_data, cmap='gray', vmin=0, vmax=1, aspect='auto')
        ax.axis('off')
        ax.set_title(label, fontsize=16, fontweight='bold', pad=2)
    
    # Add vertical separator lines between panels
    for x_pos in [0.25, 0.5, 0.75]:
        line = Line2D([x_pos, x_pos], [0.03, 0.97],
                     transform=fig.transFigure,
                     color='lightblue',
                     linewidth=3,
                     clip_on=False,
                     zorder=10)
        fig.add_artist(line)
    
    plt.subplots_adjust(left=0.0, right=1.0, top=0.97, bottom=0.03, wspace=0.0, hspace=0.0)
    plt.savefig(output_path, dpi=dpi, facecolor=background_color, 
                bbox_inches='tight', pad_inches=0.0)
    plt.close()
    
    print(f"Statistics meme saved to: {output_path}")
    print(f"  Image dimensions: {w} × {h} pixels per panel")
    print(f"  Total meme size: {w * 4} × {h} pixels")
    print(f"  Resolution: {dpi} DPI")

