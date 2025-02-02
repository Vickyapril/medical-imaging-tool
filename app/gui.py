import os
import cv2
import numpy as np
import pydicom
import vtk
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from image_processor import load_dicom_image, load_dicom_series,segment_dicom, save_segmented_image
import matplotlib.pyplot as plt

class XRayViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('XIMED Medical Imaging Tool')
        self.setGeometry(100, 100, 600, 500)

        self.label = QLabel("Upload a DICOM Image or Series", self)

        self.upload_btn = QPushButton("Load DICOM File", self)
        self.upload_btn.clicked.connect(self.load_single_dicom)

        self.upload_series_btn = QPushButton("Load DICOM Series", self)
        self.upload_series_btn.clicked.connect(self.load_dicom_series)

        self.segment_btn = QPushButton("Segment Image", self)
        self.segment_btn.clicked.connect(self.segment_image)

        self.view_3d_btn = QPushButton("View in 3D", self)
        self.view_3d_btn.clicked.connect(self.view_3d)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.upload_series_btn)
        layout.addWidget(self.segment_btn)
        layout.addWidget(self.view_3d_btn)
        self.setLayout(layout)

    def load_single_dicom(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open DICOM Image", "", "DICOM Files (*.dcm)")
        if filepath:
            self.image = load_dicom_image(filepath)
            
            # Debugging: Print image properties
            print(f"Loaded image: {filepath}")
            print(f"Image dtype: {self.image.dtype}, shape: {self.image.shape}")

            self.label.setText(f"Loaded: {filepath}")

            # Show the image in a pop-up to confirm it's loading
            self.show_image(self.image, "Loaded DICOM")


    def load_dicom_series(self):
        directory = QFileDialog.getExistingDirectory(self, "Select DICOM Folder")
        if directory:
            self.reader = load_dicom_series(directory)
            self.label.setText(f"DICOM Series Loaded: {directory}")

    def show_image(self, image, title):
        """Displays an image using Matplotlib (non-blocking)."""
        plt.figure()
        plt.imshow(image, cmap="gray")  # Ensure grayscale display
        plt.title(title)
        plt.axis("off")
        plt.show(block=False)  # Non-blocking mode

    def show_3d_viewer(self):
        """Displays a 3D volume rendering of a DICOM series using VTK."""
        print("Rendering 3D View...")  # Debugging print

        volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputConnection(self.reader.GetOutputPort())

        volume_property = vtk.vtkVolumeProperty()
        volume_property.ShadeOn()
        volume_property.SetInterpolationTypeToLinear()

        color_function = vtk.vtkColorTransferFunction()
        color_function.AddRGBPoint(-500, 0.0, 0.0, 0.0)
        color_function.AddRGBPoint(0, 1.0, 1.0, 1.0)
        color_function.AddRGBPoint(500, 1.0, 0.0, 0.0)

        opacity_function = vtk.vtkPiecewiseFunction()
        opacity_function.AddPoint(-500, 0.0)
        opacity_function.AddPoint(0, 0.1)
        opacity_function.AddPoint(500, 1.0)

        volume_property.SetColor(color_function)
        volume_property.SetScalarOpacity(opacity_function)

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

        renderer = vtk.vtkRenderer()
        renderer.AddVolume(volume)
        renderer.SetBackground(0, 0, 0)

        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)

        render_window.SetSize(1200, 800)
        render_window.SetWindowName("XIMED 3D Medical Viewer")

        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(render_window)

        print("Rendering now...")  # Debugging print
        render_window.Render()
        interactor.Start()

    def segment_image(self):
        if hasattr(self, 'image'):
            print("Segmenting image...")  # Debugging
            self.processed_image = segment_dicom(self.image)

            if self.processed_image is not None:
                print("Segmentation successful!")
                self.show_image(self.processed_image, "Segmented Image")
            else:
                print("Error: Segmentation failed.")
        else:
            self.label.setText("Please load an image first.")


    def view_3d(self):
        if hasattr(self, 'reader'):
            print("VTK Reader Output Details:")
            print(f"Reader File Path: {self.reader.GetDirectoryName()}")
            self.show_3d_viewer()
        else:
            self.label.setText("Please load a DICOM series first.")

if __name__ == '__main__':
    app = QApplication([])
    viewer = XRayViewer()
    viewer.show()
    app.exec_()
