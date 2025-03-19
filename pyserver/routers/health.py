import os
from fastapi import APIRouter
from config import OUTPUT_DIRECTORY

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "output_directory": os.path.abspath(OUTPUT_DIRECTORY)
    }

@router.get("/storage")
async def storage_info():
    """Storage information endpoint"""
    try:
        # Get total number of batches
        batch_count = len([d for d in os.listdir(OUTPUT_DIRECTORY) 
                         if os.path.isdir(os.path.join(OUTPUT_DIRECTORY, d))])
        
        # Get total space used
        total_size = 0
        for dirpath, _, filenames in os.walk(OUTPUT_DIRECTORY):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        
        # Format size
        def format_size(size_bytes):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024 or unit == 'GB':
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024
                
        return {
            "status": "healthy",
            "storage_path": os.path.abspath(OUTPUT_DIRECTORY),
            "batch_count": batch_count,
            "total_storage_used": format_size(total_size)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }