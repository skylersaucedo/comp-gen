import requests
import json
from datetime import datetime
import time

# API endpoint
BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))

def test_search_endpoint():
    print("\n=== Testing Search Endpoint ===")
    # Sample search request
    search_payload = {
        "asset_description": "Carolina Excavation Volvo A40 1500 HPY",
        "max_results": 5
    }
    
    # Make the request
    response = requests.post(
        f"{BASE_URL}/api/search",
        json=search_payload
    )
    
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))

def test_recent_searches():
    print("\n=== Testing Recent Searches Endpoint ===")
    # Get recent searches (last 5)
    response = requests.get(
        f"{BASE_URL}/api/recent-searches",
        params={"limit": 5}
    )
    
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))

def test_error_handling():
    print("\n=== Testing Error Handling ===")
    # Test with invalid payload (missing required field)
    invalid_payload = {
        "max_results": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/search",
        json=invalid_payload
    )
    
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))

def test_rate_limiting():
    print("\n=== Testing Rate Limiting ===")
    # Make multiple requests in quick succession
    for i in range(3):
        response = requests.post(
            f"{BASE_URL}/api/search",
            json={
                "asset_description": f"Test request {i+1}",
                "max_results": 1
            }
        )
        print(f"Request {i+1} Status Code:", response.status_code)
        time.sleep(1)  # Wait 1 second between requests

if __name__ == "__main__":
    # Run all tests
    test_root_endpoint()
    test_search_endpoint()
    test_recent_searches()
    test_error_handling()
    test_rate_limiting() 