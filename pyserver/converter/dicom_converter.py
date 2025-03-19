import os
import numpy as np
import pydicom
from PIL import Image
from io import BytesIO

class ConversionError(Exception):
    """Custom exception for conversion errors"""
    pass

def convert_dicom_to_png(dicom_file, output_path=None):
    """
    Convert a DICOM file to PNG format
    
    Args:
        dicom_file: File-like object or path containing DICOM data
        output_path: Optional path to save the PNG file
        
    Returns:
        BytesIO buffer containing the PNG data, or the path where the PNG was saved
    """
    try:
        dicom_data = pydicom.dcmread(dicom_file)
        
        # Handle different image formats and bit depths
        pixel_array = dicom_data.pixel_array
        
        # Normalize pixel values based on the data type
        if pixel_array.dtype != 'uint8':
            # Get min/max values
            min_val = pixel_array.min()
            max_val = pixel_array.max()
            
            # Scale to 0-255 range for 8-bit PNG
            if max_val != min_val:
                scaled_array = ((pixel_array - min_val) / (max_val - min_val) * 255).astype('uint8')
            else:
                scaled_array = pixel_array.astype('uint8')
        else:
            scaled_array = pixel_array
        
        # Create image from array
        image = Image.fromarray(scaled_array)
        
        # Get DICOM metadata for image processing
        window_center = getattr(dicom_data, 'WindowCenter', None)
        window_width = getattr(dicom_data, 'WindowWidth', None)
        
        # Apply windowing if available (common in CT/MRI)
        if window_center is not None and window_width is not None:
            # Convert to single values if they're sequences
            if hasattr(window_center, '__getitem__') and not isinstance(window_center, (int, float)):
                window_center = window_center[0]
            if hasattr(window_width, '__getitem__') and not isinstance(window_width, (int, float)):
                window_width = window_width[0]
                
            # Apply window level processing
            min_value = window_center - window_width/2
            max_value = window_center + window_width/2
            
            # Create enhanced image with windowing
            lut = [0] * 256
            for i in range(256):
                scaled_value = min_value + (i/255) * (max_value - min_value)
                if scaled_value <= min_value:
                    lut[i] = 0
                elif scaled_value > max_value:
                    lut[i] = 255
                else:
                    lut[i] = int(((scaled_value - min_value) / (max_value - min_value)) * 255)
        
        if output_path:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image.save(output_path, format="PNG")
            return output_path
        else:
            png_buffer = BytesIO()
            image.save(png_buffer, format="PNG")
            png_buffer.seek(0)
            return png_buffer
            
    except Exception as e:
        raise ConversionError(f"Error converting DICOM to PNG: {str(e)}")

