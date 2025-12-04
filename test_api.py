"""
Test script to verify the API is working correctly
"""
import requests
import json
from datetime import datetime

# API endpoint
url = "http://127.0.0.1:8000/predict"

# Test 1: Normal prediction
print("=" * 60)
print("TEST 1: Normal Prediction")
print("=" * 60)

payload = {
    "DateTime": "2025-10-20T18:00:00",
    "PT08_S1_CO": 1360.0,
    "NMHC_GT": 150.0,
    "C6H6_GT": 11.9,
    "PT08_S2_NMHC": 1046.0,
    "NOx_GT": 166.0,
    "PT08_S3_NOx": 1056.0,
    "NO2_GT": 113.0,
    "PT08_S4_NO2": 1692.0,
    "PT08_S5_O3": 1268.0,
    "T": 13.6,
    "RH": 48.9,
    "AH": 0.7578
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Predicted CO Level: {result['prediction_co_gt']} mg/m³")
        print(f"Out of Distribution: {result['is_out_of_distribution']}")
        print(f"Model Version: {result['model_version']}")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")

# Test 2: OOD Detection
print("\n" + "=" * 60)
print("TEST 2: Out-of-Distribution Detection")
print("=" * 60)

ood_payload = {
    "DateTime": "2025-10-20T18:00:00",
    "PT08_S1_CO": 50000.0,  # Extremely high value
    "NMHC_GT": 10000.0,
    "C6H6_GT": 500.0,
    "PT08_S2_NMHC": 50000.0,
    "NOx_GT": 5000.0,
    "PT08_S3_NOx": 50000.0,
    "NO2_GT": 5000.0,
    "PT08_S4_NO2": 50000.0,
    "PT08_S5_O3": 50000.0,
    "T": 100.0,
    "RH": 200.0,
    "AH": 50.0
}

try:
    response = requests.post(url, json=ood_payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Predicted CO Level: {result['prediction_co_gt']} mg/m³")
        print(f"Out of Distribution: {result['is_out_of_distribution']}")
        print(f"Model Version: {result['model_version']}")
        
        if result['is_out_of_distribution']:
            print("\n⚠️  WARNING: Anomalous sensor readings detected!")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")

# Test 3: Health check
print("\n" + "=" * 60)
print("TEST 3: Health Check")
print("=" * 60)

try:
    response = requests.get("http://127.0.0.1:8000/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Message: {result['message']}")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)
print("\n📚 Documentation is available at:")
print("  - API Guide: docs/API_USAGE_GUIDE.md")
print("  - Architecture: docs/ARCHITECTURE.md")
print("  - Performance: docs/MODEL_PERFORMANCE.md")
print("  - Troubleshooting: docs/TROUBLESHOOTING.md")
print("  - Swagger UI: http://127.0.0.1:8000/docs")
