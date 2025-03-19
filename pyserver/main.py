from fastapi import FastAPI
import uvicorn

from routers import converter, health

app = FastAPI(
    title="DICOM to PNG Converter API",
    description="API for converting DICOM medical images to PNG format",
    version="1.0.0"
)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)