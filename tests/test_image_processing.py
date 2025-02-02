import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from image_processor import enhance_contrast

def test_enhance_contrast():
    """Test contrast enhancement function"""
    sample_img = np.ones((128, 128), dtype=np.uint8) * 100
    enhanced = enhance_contrast(sample_img)
    assert enhanced.shape == sample_img.shape, "Output shape must match input shape"
    assert enhanced.mean() > sample_img.mean(), "Contrast should be improved"
