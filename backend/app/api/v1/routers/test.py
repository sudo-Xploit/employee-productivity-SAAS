from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
import os
from datetime import datetime
from typing import Dict, Any

from app.db.session import get_db

router = APIRouter()


@router.get("/")
def test_root():
    """Test root endpoint"""
    return {"message": "Test endpoint is working"}


@router.get("/db")
def test_db(db: Session = Depends(get_db)):
    """Test database connection"""
    try:
        # Just try to use the session
        result = db.execute("SELECT 1").scalar()
        return {"status": "success", "message": "Database connection successful", "result": result}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}


@router.post("/upload")
async def test_upload(file: UploadFile = File(...)):
    """Test file upload functionality"""
    try:
        content = await file.read()
        return {
            "status": "success",
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        }
    except Exception as e:
        return {"status": "error", "message": f"Upload failed: {str(e)}"}


@router.get("/report")
def test_report():
    """Test report generation by creating a simple text file"""
    try:
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Create a simple text file as a test report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(reports_dir, f"test_report_{timestamp}.txt")
        
        with open(filepath, "w") as f:
            f.write("This is a test report\n")
            f.write(f"Generated at: {datetime.now().isoformat()}\n")
            f.write("Test report content goes here.\n")
        
        return FileResponse(
            path=filepath,
            filename=f"test_report_{timestamp}.txt",
            media_type="text/plain"
        )
    except Exception as e:
        return {"status": "error", "message": f"Report generation failed: {str(e)}"}
