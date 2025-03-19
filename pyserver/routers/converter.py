import os
import zipfile
import tempfile
from typing import List

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from config import OUTPUT_DIRECTORY
from converter.dicom_converter import convert_dicom_to_png, ConversionError
from utils.file_utils import create_batch_directory, save_uploaded_file, extract_dicom_files

router = APIRouter(
    prefix="/converter",
    tags=["converter"],
    responses={404: {"description": "Not found"}},
)

@router.post("/dicom-to-png/")
async def convert_dicom_to_png_api(zip_file: UploadFile = File(...)):
    """
    Convert multiple DICOM files in a ZIP archive to PNG format and store them in a local folder
    
    - **zip_file**: ZIP file containing one or more DICOM (.dcm) files
    
    Returns a list of paths to the generated PNG files
    """
    if not zip_file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP file")
    
    filename = zip_file.filename.replace(".zip","")

    # Create a batch folder for this conversion job
    batch_folder = create_batch_directory(OUTPUT_DIRECTORY,filename)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded ZIP file to temporary directory
        zip_path = save_uploaded_file(zip_file, temp_dir)
        
        # Get DICOM files from ZIP
        dicom_files = extract_dicom_files(zip_path)
        
        if not dicom_files:
            raise HTTPException(status_code=400, detail="No DICOM files found in the ZIP archive")
        
        # Process each DICOM file
        stored_png_files = []
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for dicom_file_name in dicom_files:
                try:
                    # Create PNG file name (preserve directory structure)
                    png_file_name = os.path.splitext(dicom_file_name)[0] + '.png'
                    
                    # Create full path for storage
                    storage_path = os.path.join(batch_folder, png_file_name)
                    
                    # Ensure directory exists for nested files
                    os.makedirs(os.path.dirname(storage_path), exist_ok=True)
                    
                    # Convert DICOM to PNG
                    with zip_ref.open(dicom_file_name) as dicom_file:
                        convert_dicom_to_png(dicom_file, storage_path)
                    
                    # Store the relative path for response
                    stored_png_files.append(storage_path)
                    print(f"Successfully converted and stored: {storage_path}")
                    
                except ConversionError as e:
                    # Log the error but continue processing other files
                    print(f"Error processing {dicom_file_name}: {str(e)}")
        
        if not stored_png_files:
            raise HTTPException(status_code=500, detail="Failed to convert any DICOM files to PNG")
            
        # Return the list of stored file paths
        return JSONResponse(content={
            "message": f"Successfully converted {len(stored_png_files)} files",
            "output_directory": batch_folder,
            "stored_files": stored_png_files
        })