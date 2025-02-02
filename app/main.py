from image_processor import load_dicom_image, enhance_contrast
import matplotlib.pyplot as plt

# Path to a sample DICOM file (Replace with your actual path)
dicom_path = "data/sample_xray.dcm"

# Load the DICOM image
try:
    img = load_dicom_image(dicom_path)
    print("DICOM image loaded successfully!")

    # Enhance contrast
    enhanced_img = enhance_contrast(img)
    print("Contrast enhancement applied successfully!")

    # Show original and enhanced images
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(img, cmap="gray")
    axes[0].set_title("Original X-ray")
    axes[0].axis("off")

    axes[1].imshow(enhanced_img, cmap="gray")
    axes[1].set_title("Enhanced X-ray")
    axes[1].axis("off")

    plt.show()

except Exception as e:

    print(f"Error: {e}")

