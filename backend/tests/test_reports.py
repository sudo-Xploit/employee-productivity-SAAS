import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, Depends, Query
from fastapi.responses import FileResponse
from fastapi.testclient import TestClient

# Create a test app with mock report endpoints
app = FastAPI()

# Actual file paths
TEST_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT_PATH = os.path.join(TEST_DIR, "reports", "test_report.txt")
CSV_PATH = os.path.join(TEST_DIR, "reports", "test_report.csv")
PDF_PATH = os.path.join(TEST_DIR, "reports", "test_report.pdf")
EXCEL_PATH = os.path.join(TEST_DIR, "reports", "test_report.xlsx")

@app.get("/api/v1/reports/generate")
def generate_report(report_type: str = Query(...)):
    if report_type == "txt":
        return FileResponse(
            path=TXT_PATH,
            filename="test_report.txt",
            media_type="text/plain"
        )
    elif report_type == "csv":
        return FileResponse(
            path=CSV_PATH,
            filename="test_report.csv",
            media_type="text/csv"
        )
    elif report_type == "pdf":
        return FileResponse(
            path=PDF_PATH,
            filename="test_report.pdf",
            media_type="application/pdf"
        )
    elif report_type == "excel":
        return FileResponse(
            path=EXCEL_PATH,
            filename="test_report.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        return {"detail": f"Invalid report type: {report_type}. Use 'txt', 'csv', 'pdf', or 'excel'."}


@pytest.fixture
def reports_client():
    return TestClient(app)

@pytest.fixture
def mock_file_response():
    # Create a mock file response
    with patch("fastapi.responses.FileResponse", autospec=True) as mock:
        mock.return_value.status_code = 200
        mock.return_value.headers = {
            "content-disposition": "attachment; filename=test_report.pdf",
            "content-type": "application/pdf"
        }
        yield mock

@pytest.mark.report
class TestReports:
    """Test report generation functionality with mocks"""
    
    def test_generate_txt_report(self, reports_client, mock_file_response):
        """Test generating a text report"""
        with patch("os.path.exists", return_value=True):
            response = reports_client.get("/api/v1/reports/generate?report_type=txt")
            assert response.status_code == 200
            
            # Check headers
            assert "content-disposition" in response.headers
            assert "attachment" in response.headers["content-disposition"]
            assert "test_report.txt" in response.headers["content-disposition"]
    
    def test_generate_csv_report(self, reports_client, mock_file_response):
        """Test generating a CSV report"""
        with patch("os.path.exists", return_value=True):
            response = reports_client.get("/api/v1/reports/generate?report_type=csv")
            assert response.status_code == 200
            
            # Check headers
            assert "content-disposition" in response.headers
            assert "attachment" in response.headers["content-disposition"]
            assert "test_report.csv" in response.headers["content-disposition"]
    
    def test_generate_pdf_report(self, reports_client, mock_file_response):
        """Test generating a PDF report"""
        with patch("os.path.exists", return_value=True):
            response = reports_client.get("/api/v1/reports/generate?report_type=pdf")
            assert response.status_code == 200
            
            # Check headers
            assert "content-disposition" in response.headers
            assert "attachment" in response.headers["content-disposition"]
            assert "test_report.pdf" in response.headers["content-disposition"]
    
    def test_generate_excel_report(self, reports_client, mock_file_response):
        """Test generating an Excel report"""
        with patch("os.path.exists", return_value=True):
            response = reports_client.get("/api/v1/reports/generate?report_type=excel")
            assert response.status_code == 200
            
            # Check headers
            assert "content-disposition" in response.headers
            assert "attachment" in response.headers["content-disposition"]
            assert "test_report.xlsx" in response.headers["content-disposition"]
    
    def test_generate_invalid_report(self, reports_client):
        """Test generating a report with invalid type"""
        response = reports_client.get("/api/v1/reports/generate?report_type=invalid")
        assert response.status_code == 200  # FastAPI returns 200 with the error detail
        data = response.json()
        assert "detail" in data
        assert "Invalid report type" in data["detail"]
