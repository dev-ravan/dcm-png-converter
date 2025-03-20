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
    if not zip_file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP file")

    filename = zip_file.filename.replace(".zip", "")
    batch_folder = create_batch_directory(OUTPUT_DIRECTORY, filename)

    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = save_uploaded_file(zip_file, temp_dir)
        dicom_files = extract_dicom_files(zip_path)

        if not dicom_files:
            raise HTTPException(status_code=400, detail="No DICOM files found in the ZIP archive")

        stored_png_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for dicom_file_name in dicom_files:
                try:
                    png_file_name = os.path.splitext(dicom_file_name)[0] + '.png'
                    storage_path = os.path.join(batch_folder, png_file_name)
                    os.makedirs(os.path.dirname(storage_path), exist_ok=True)

                    with zip_ref.open(dicom_file_name) as dicom_file:
                        convert_dicom_to_png(dicom_file, storage_path)

                    # Convert absolute path to URL
                    relative_path = os.path.relpath(storage_path, OUTPUT_DIRECTORY)
                    image_url = f"http://127.0.0.1:8000/files/{relative_path}"
                    stored_png_files.append(image_url)

                except ConversionError as e:
                    print(f"Error processing {dicom_file_name}: {str(e)}")

        if not stored_png_files:
            raise HTTPException(status_code=500, detail="Failed to convert any DICOM files to PNG")

        return JSONResponse(content={
    "message": f"Successfully converted {len(stored_png_files)} files",
    "output_directory": f"http://127.0.0.1:8000/files/{filename}",
    "stored_files": stored_png_files if stored_png_files else []  # Ensure non-null
})
