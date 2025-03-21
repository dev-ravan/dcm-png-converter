import sys
from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from config import OUTPUT_DIRECTORY
from routers import converter, health

app = FastAPI(
    title="DICOM to PNG Converter API",
    description="API for converting DICOM medical images to PNG format",
    version="1.0.0"
)

app.mount("/files", StaticFiles(directory=OUTPUT_DIRECTORY), name="files")

# Include routers
app.include_router(converter.router)
app.include_router(health.router)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint showing API information"""
    return {
        "app_name": "DICOM to PNG Converter API",
        "version": "1.0.0",
        "endpoints": {
            "converter": "/converter/dicom-to-png/",
            "health": "/health/",
            "storage_info": "/health/storage"
        }
    }

if __name__ == "__main__":
    from config import OUTPUT_DIRECTORY
    import os
    print(f"Images will be stored in: {os.path.abspath(OUTPUT_DIRECTORY)}")
    if __name__ == "__main__":
        # For Windows, it's better to use host="127.0.0.1" instead of "0.0.0.0"
        # "0.0.0.0" might require admin privileges on Windows
        host = "127.0.0.1" if sys.platform.startswith("win") else "0.0.0.0"
        uvicorn.run(app, host=host, port=8000)