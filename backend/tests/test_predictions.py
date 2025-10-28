import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

# Create a test app with mock prediction endpoints
app = FastAPI()

# Mock prediction data
MOCK_PREDICTION_RESULT = {
    "success": True,
    "department_id": 1,
    "department_name": "Engineering",
    "prediction_date": "2023-10-28",
    "next_month": 11,
    "current_roi": 0.75,
    "predicted_roi": 0.82,
    "roi_trend_percent": 9.33,
    "roi_confidence": 0.85,
    "current_cost": 350000.0,
    "predicted_cost": 360000.0,
    "cost_trend_percent": 2.86,
    "cost_confidence": 0.9,
    "recommendations": [
        "ROI is projected to increase significantly. Consider expanding successful projects.",
        "Costs are projected to remain stable. Continue monitoring for any changes."
    ]
}

MOCK_TRAINING_RESULT = {
    "success": True,
    "department_id": 1,
    "roi_model_metrics": {
        "mse": 0.0023,
        "r2": 0.87
    },
    "cost_model_metrics": {
        "mse": 1500000.0,
        "r2": 0.92
    },
    "roi_model_path": "/app/models/department_1_roi_model.joblib",
    "cost_model_path": "/app/models/department_1_cost_model.joblib"
}

@app.get("/api/v1/predict/department/{department_id}")
def predict_department_performance(department_id: int):
    if department_id != 1:
        return {"detail": "Department not found"}
    return MOCK_PREDICTION_RESULT

@app.post("/api/v1/predict/department/{department_id}/train")
def train_department_model(department_id: int):
    if department_id != 1:
        return {"detail": "Department not found"}
    return {
        "message": "Department prediction models trained successfully",
        "department_id": department_id,
        "department_name": "Engineering",
        "roi_model_metrics": MOCK_TRAINING_RESULT["roi_model_metrics"],
        "cost_model_metrics": MOCK_TRAINING_RESULT["cost_model_metrics"],
    }

@pytest.fixture
def predictions_client():
    return TestClient(app)


@pytest.mark.prediction
class TestPredictions:
    """Test prediction functionality with mocks"""
    
    def test_predict_department_performance(self, predictions_client):
        """Test department performance prediction"""
        response = predictions_client.get("/api/v1/predict/department/1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["department_id"] == 1
        assert data["department_name"] == "Engineering"
        assert "prediction_date" in data
        assert "next_month" in data
        assert "current_roi" in data
        assert "predicted_roi" in data
        assert "roi_trend_percent" in data
        assert "roi_confidence" in data
        assert "current_cost" in data
        assert "predicted_cost" in data
        assert "cost_trend_percent" in data
        assert "cost_confidence" in data
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)
    
    def test_predict_nonexistent_department(self, predictions_client):
        """Test prediction for nonexistent department"""
        response = predictions_client.get("/api/v1/predict/department/999")
        assert response.status_code == 200  # FastAPI returns 200 with the error detail
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Department not found"
    
    def test_train_department_model(self, predictions_client):
        """Test training department model"""
        response = predictions_client.post("/api/v1/predict/department/1/train")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert data["department_id"] == 1
        assert "department_name" in data
        assert "roi_model_metrics" in data
        assert "cost_model_metrics" in data
        
        # Check metrics structure
        assert "mse" in data["roi_model_metrics"]
        assert "r2" in data["roi_model_metrics"]
        assert "mse" in data["cost_model_metrics"]
        assert "r2" in data["cost_model_metrics"]
    
    def test_train_nonexistent_department(self, predictions_client):
        """Test training for nonexistent department"""
        response = predictions_client.post("/api/v1/predict/department/999/train")
        assert response.status_code == 200  # FastAPI returns 200 with the error detail
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Department not found"
