"""
Step 5: Create a masked stippled image by applying a block letter mask.
Removes stipples in the masked areas to demonstrate selection bias.
"""

import numpy as np


def create_masked_stipple(
    stipple_img: np.ndarray,
    mask_img: np.ndarray,
    threshold: float = 0.5
) -> np.ndarray:
    """
    Apply a mask to a stippled image, removing stipples in masked areas.
    
    This function creates a "biased estimate" by systematically removing
    data points (stipples) where the mask is dark, demonstrating how
    selection bias affects data analysis.
    
    Parameters
    ----------
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1]
        0.0 = black dot (stipple), 1.0 = white background
    mask_img : np.ndarray
        Mask image as 2D array (height, width) with values in [0, 1]
        0.0 = black (mask area, remove stipples)
        1.0 = white (keep area, preserve stipples)
    threshold : float
        Threshold value to determine what counts as "part of the mask"
        Pixels below threshold are considered part of the mask (remove stipples)
        Pixels above threshold are considered keep area (preserve stipples)
        Default 0.5
    
    Returns
    -------
    masked_stipple : np.ndarray
        2D numpy array with the same shape as the input images
        Stipples are removed (set to white/1.0) where mask is dark (below threshold)
        Stipples are preserved where mask is light (above threshold)
    """
    # Ensure both images have the same shape
    if stipple_img.shape != mask_img.shape:
        raise ValueError(
            f"Images must have the same shape. "
            f"stipple_img: {stipple_img.shape}, mask_img: {mask_img.shape}"
        )
    
    # Create a copy of the stippled image to avoid modifying the original
    masked_stipple = stipple_img.copy()
    
    # Identify mask areas (where mask is dark, below threshold)
    mask_areas = mask_img < threshold
    
    # Remove stipples in masked areas by setting them to white (1.0)
    masked_stipple[mask_areas] = 1.0
    
    return masked_stipple

