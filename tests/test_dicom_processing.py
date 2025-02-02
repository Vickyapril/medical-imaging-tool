import sys
import os
import numpy as np

# ✅ Add 'app/' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

# ✅ Now import the functions correctly
from image_processor import load_dicom_image, get_dicom_metadata, get_dicom_series_metadata, segment_dicom

def test_load_dicom_image():
    """Test if a DICOM image loads correctly."""
    dicom_path = "data/sample_xray.dcm"  # Make sure this file exists in your repo!
    
    image = load_dicom_image(dicom_path)
    
    assert isinstance(image, np.ndarray), "DICOM image should be a NumPy array"
    assert image.shape[0] > 0 and image.shape[1] > 0, "Image should not be empty"

def test_get_dicom_metadata():
    """Test if metadata is extracted correctly from a DICOM file."""
    dicom_path = "data/sample_xray.dcm"

    metadata = get_dicom_metadata(dicom_path)

    assert "Patient ID" in metadata, "Metadata should include 'Patient ID'"
    assert "Study Date" in metadata, "Metadata should include 'Study Date'"
    assert isinstance(metadata["Patient ID"], str), "Patient ID should be a string"

def test_get_dicom_series_metadata():
    """Test if metadata is extracted from a full DICOM series."""
    series_path = "data/case2"  # Make sure this folder contains multiple .dcm files

    metadata_list = get_dicom_series_metadata(series_path)

    assert len(metadata_list) > 1, "DICOM series should contain multiple files"
    assert "Instance Number" in metadata_list[0], "Metadata should include 'Instance Number'"
    
def test_segment_dicom():
    """Test if segmentation works on a DICOM image."""
    dicom_path = "data/sample_xray.dcm"

    image = load_dicom_image(dicom_path)
    segmented_image = segment_dicom(image)

    assert isinstance(segmented_image, np.ndarray), "Segmented image should be a NumPy array"
    assert segmented_image.shape[0] > 0 and segmented_image.shape[1] > 0, "Segmented image should not be empty"

