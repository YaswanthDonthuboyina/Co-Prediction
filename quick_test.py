import requests

# Test normal prediction
print("Testing API...")
response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={
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
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
