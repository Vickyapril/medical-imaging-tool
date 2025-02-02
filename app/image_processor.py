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

def get_dicom_metadata(filepath):
    """Extracts metadata from a DICOM file."""
    dicom_img = pydicom.dcmread(filepath)
    metadata = {
        "Patient Name": dicom_img.get("PatientName", "Unknown"),
        "Patient ID": dicom_img.get("PatientID", "Unknown"),
        "Patient Age": dicom_img.get("PatientAge", "Unknown"),
        "Patient Sex": dicom_img.get("PatientSex", "Unknown"),
        "Study Date": dicom_img.get("StudyDate", "Unknown"),
        "Study Time": dicom_img.get("StudyTime", "Unknown"),
        "Modality": dicom_img.get("Modality", "Unknown"),
        "Study Description": dicom_img.get("StudyDescription", "Unknown"),
        "Institution": dicom_img.get("InstitutionName", "Unknown"),
        "Manufacturer": dicom_img.get("Manufacturer", "Unknown"),
        "Rows": dicom_img.get("Rows", "Unknown"),
        "Columns": dicom_img.get("Columns", "Unknown"),
        "Pixel Spacing": dicom_img.get("PixelSpacing", "Unknown"),
        "Bits Allocated": dicom_img.get("BitsAllocated", "Unknown"),
        "Bits Stored": dicom_img.get("BitsStored", "Unknown"),
        "High Bit": dicom_img.get("HighBit", "Unknown"),
        "Rescale Intercept": dicom_img.get("RescaleIntercept", "Unknown"),
        "Rescale Slope": dicom_img.get("RescaleSlope", "Unknown"),
    }
    return metadata

def get_dicom_series_metadata(directory):
    """Extracts metadata from all DICOM files in a series folder."""
    
    metadata_list = []
    
    for filename in sorted(os.listdir(directory)):  # Ensure files are read in order
        if filename.endswith(".dcm"):  
            dicom_path = os.path.join(directory, filename)
            dicom_img = pydicom.dcmread(dicom_path)
            
            metadata = {
                "File Name": filename,
                "Instance Number": dicom_img.get("InstanceNumber", "Unknown"),
                "Slice Location": dicom_img.get("SliceLocation", "Unknown"),
                "Patient ID": dicom_img.get("PatientID", "Unknown"),
                "Study Date": dicom_img.get("StudyDate", "Unknown"),
                "Modality": dicom_img.get("Modality", "Unknown"),
                "Institution": dicom_img.get("InstitutionName", "Unknown"),
                "Rows": dicom_img.get("Rows", "Unknown"),
                "Columns": dicom_img.get("Columns", "Unknown"),
                "Pixel Spacing": dicom_img.get("PixelSpacing", "Unknown"),
                "Slice Thickness": dicom_img.get("SliceThickness", "Unknown"),
            }
            
            metadata_list.append(metadata)

    return metadata_list  # Returns metadata for all slices


def save_segmented_image(image, filename):
    """Saves segmented image as PNG."""
    cv2.imwrite(filename, image)