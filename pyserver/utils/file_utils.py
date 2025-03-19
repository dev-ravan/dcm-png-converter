import os
import zipfile
import tempfile
import datetime
from typing import List, Tuple

def create_batch_directory(base_dir,filename):
    """
    Create a timestamped batch directory for this conversion job
    
    Args:
        base_dir: Base directory path
    
    Returns:
        Path to the created batch directory
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_folder = os.path.join(base_dir, f"{filename}_{timestamp}")
    os.makedirs(batch_folder, exist_ok=True)
    return batch_folder

def save_uploaded_file(uploaded_file, temp_dir):
    """
    Save an uploaded file to a temporary directory
    
    Args:
        uploaded_file: FastAPI UploadFile object
        temp_dir: Temporary directory path
    
    Returns:
        Path to the saved file
    """
    file_path = os.path.join(temp_dir, uploaded_file.filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())
    return file_path

def extract_dicom_files(zip_path):
    """
    Get a list of DICOM files from a ZIP archive
    
    Args:
        zip_path: Path to the ZIP file
    
    Returns:
        List of DICOM file names in the ZIP
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        dicom_files = [f for f in zip_ref.namelist() 
                      if f.lower().endswith(('.dcm', '.dicom'))]
    return dicom_files