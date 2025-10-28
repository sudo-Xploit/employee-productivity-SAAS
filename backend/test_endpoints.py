import requests
import os

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code}")
    print(response.json())
    print()

def test_db_connection():
    """Test the database connection"""
    response = requests.get(f"{BASE_URL}/test-db")
    print(f"Database connection: {response.status_code}")
    print(response.json())
    print()

def test_file_upload():
    """Test file upload functionality"""
    # Create a test file
    test_file_path = "test_upload.csv"
    with open(test_file_path, "w") as f:
        f.write("name,value\ntest,123")
    
    # Upload the file
    with open(test_file_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/test-upload",
            files={"file": ("test_upload.csv", f, "text/csv")}
        )
    
    print(f"File upload: {response.status_code}")
    print(response.json())
    print()
    
    # Clean up
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

def test_report_generation():
    """Test report generation"""
    response = requests.get(f"{BASE_URL}/test-report")
    print(f"Report generation: {response.status_code}")
    
    if response.status_code == 200:
        # Save the report
        with open("downloaded_test_report.txt", "wb") as f:
            f.write(response.content)
        print("Report downloaded successfully")
    else:
        print(response.json())
    print()

def main():
    """Run all tests"""
    print("=== Testing API Endpoints ===")
    test_root()
    test_db_connection()
    test_file_upload()
    test_report_generation()
    print("=== Tests Complete ===")

if __name__ == "__main__":
    main()
