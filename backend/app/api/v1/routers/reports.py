import os
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission
from app.db.session import get_db
from app.models.user import User
from app.services import reports_service

router = APIRouter()


@router.get("/generate", response_class=FileResponse)
def generate_report(
    *,
    db: Session = Depends(get_db),
    report_type: str = Query(..., description="Type of report to generate: 'pdf' or 'excel'"),
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Generate a report in PDF or Excel format.
    """
    try:
        if report_type.lower() == "pdf":
            filename, filepath = reports_service.generate_pdf_report(db)
        elif report_type.lower() == "excel":
            filename, filepath = reports_service.generate_excel_report(db)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid report type: {report_type}. Use 'pdf' or 'excel'.",
            )
        
        # Check if file exists
        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate report file.",
            )
        
        # Return file
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/pdf" if report_type.lower() == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}",
        )
