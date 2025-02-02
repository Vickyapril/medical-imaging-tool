import cv2
import numpy as np
import pydicom
import itk
import vtk
import os

def load_dicom_series(directory):
    """Loads a DICOM series from a folder and returns a VTK image"""
    
    # Set up the DICOM reader
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(directory)
    reader.Update()

    return reader

def load_dicom_image(filepath):
    """Loads a single DICOM X-ray image."""
    dicom_img = pydicom.dcmread(filepath)
    return dicom_img.pixel_array

import cv2
import numpy as np

def segment_dicom(image):
    """Allows interactive region selection and applies segmentation."""

    if image.dtype != np.uint8:
        print("Converting image to uint8 for segmentation...")
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Let the user select a region interactively
    print("Select a region with your mouse and press ENTER to confirm.")
    roi = cv2.selectROI("Select Region", image, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Region")

    x, y, w, h = map(int, roi)
    print(f"Selected region: x={x}, y={y}, width={w}, height={h}")

    # Crop the selected region
    cropped_image = image[y:y+h, x:x+w]

    # Apply threshold-based segmentation
    _, segmented = cv2.threshold(cropped_image, 100, 255, cv2.THRESH_BINARY)

    # Apply morphological operations for better segmentation
    kernel = np.ones((5,5), np.uint8)
    segmented = cv2.morphologyEx(segmented, cv2.MORPH_CLOSE, kernel)

    return segmented


def save_segmented_image(image, filename):
    """Saves segmented image as PNG."""
    cv2.imwrite(filename, image)