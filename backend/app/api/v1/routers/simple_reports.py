import os
from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/generate")
def generate_report(
    *,
    db: Session = Depends(get_db),
    report_type: str = Query(..., description="Type of report to generate: 'txt' or 'csv'"),
) -> Any:
    """
    Generate a report in TXT or CSV format.
    """
    try:
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if report_type.lower() == "txt":
            # Generate a simple text report
            filename = f"simple_report_{timestamp}.txt"
            filepath = os.path.join(reports_dir, filename)
            
            with open(filepath, "w") as f:
                f.write("Employee Productivity Report\n")
                f.write("==========================\n\n")
                f.write(f"Generated at: {datetime.now().isoformat()}\n\n")
                f.write("This is a sample report.\n")
                f.write("In a real implementation, this would contain actual data from the database.\n")
            
            return FileResponse(
                path=filepath,
                filename=filename,
                media_type="text/plain"
            )
        
        elif report_type.lower() == "csv":
            # Generate a simple CSV report
            filename = f"simple_report_{timestamp}.csv"
            filepath = os.path.join(reports_dir, filename)
            
            with open(filepath, "w") as f:
                f.write("name,department,salary,revenue,profit,roi\n")
                f.write("John Smith,Engineering,120000,250000,130000,1.08\n")
                f.write("Jane Doe,Engineering,110000,220000,110000,1.00\n")
                f.write("Mike Johnson,Engineering,95000,180000,85000,0.89\n")
                f.write("Sarah Williams,Marketing,90000,200000,110000,1.22\n")
            
            return FileResponse(
                path=filepath,
                filename=filename,
                media_type="text/csv"
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid report type: {report_type}. Use 'txt' or 'csv'.",
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}",
        )
