# API Usage Guide

## Table of Contents
- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Request Examples](#request-examples)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Code Examples](#code-examples)

---

## Overview

The AirGuard CO Prediction API provides real-time Carbon Monoxide (CO) level predictions based on air quality sensor readings. The API also includes Out-of-Distribution (OOD) detection to flag anomalous inputs.

**Key Features:**
- Real-time CO level predictions
- Anomaly detection for input data
- RESTful JSON API
- Interactive documentation (Swagger UI)
- Containerized deployment

---

## Base URL

### Production
```
https://co-prediction.onrender.com
```

### Local Development
```
http://127.0.0.1:8000
```

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

> **Note:** For production use, consider implementing API key authentication or OAuth2.

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Verify that the API is running.

**Response:**
```json
{
  "message": "Welcome to the CO Prediction API. Go to /docs for interactive documentation."
}
```

**Example:**
```bash
curl https://co-prediction.onrender.com/
```

---

### 2. Predict CO Level

**Endpoint:** `POST /predict`

**Description:** Predict CO concentration based on sensor readings.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "prediction_co_gt": 2.7635,
  "is_out_of_distribution": false,
  "model_version": "1.0.0"
}
```

---

## Request Examples

### Using cURL

#### Basic Prediction Request
```bash
curl -X POST "https://co-prediction.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

#### Testing OOD Detection
```bash
curl -X POST "https://co-prediction.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "DateTime": "2025-10-20T18:00:00",
    "PT08_S1_CO": 50000.0,
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
  }'
```

**Expected Response:**
```json
{
  "prediction_co_gt": 15.2341,
  "is_out_of_distribution": true,
  "model_version": "1.0.0"
}
```

---

## Response Format

### Success Response

**Status Code:** `200 OK`

**Body:**
```json
{
  "prediction_co_gt": 2.7635,
  "is_out_of_distribution": false,
  "model_version": "1.0.0"
}
```

**Fields:**
- `prediction_co_gt` (float): Predicted CO concentration in mg/m³
- `is_out_of_distribution` (boolean): 
  - `false`: Input data is within normal range
  - `true`: Input data is anomalous/unusual
- `model_version` (string): Version of the prediction model

---

## Error Handling

### Validation Error

**Status Code:** `422 Unprocessable Entity`

**Cause:** Invalid input data (missing fields, wrong data types)

**Example Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "PT08_S1_CO"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Internal Server Error

**Status Code:** `500 Internal Server Error`

**Cause:** Model loading failure or unexpected error

**Example Response:**
```json
{
  "error": "Prediction assets not loaded. Please run the training pipeline."
}
```

---

## Code Examples

### Python (using requests)

```python
import requests
from datetime import datetime

# API endpoint
url = "https://co-prediction.onrender.com/predict"

# Prepare sensor data
payload = {
    "DateTime": datetime.now().isoformat(),
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

# Make prediction request
response = requests.post(url, json=payload)

# Check response
if response.status_code == 200:
    result = response.json()
    print(f"Predicted CO Level: {result['prediction_co_gt']} mg/m³")
    print(f"Out of Distribution: {result['is_out_of_distribution']}")
    print(f"Model Version: {result['model_version']}")
    
    # Alert if OOD detected
    if result['is_out_of_distribution']:
        print("⚠️  WARNING: Anomalous sensor readings detected!")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### JavaScript (using fetch)

```javascript
// API endpoint
const url = "https://co-prediction.onrender.com/predict";

// Prepare sensor data
const payload = {
  DateTime: new Date().toISOString(),
  PT08_S1_CO: 1360.0,
  NMHC_GT: 150.0,
  C6H6_GT: 11.9,
  PT08_S2_NMHC: 1046.0,
  NOx_GT: 166.0,
  PT08_S3_NOx: 1056.0,
  NO2_GT: 113.0,
  PT08_S4_NO2: 1692.0,
  PT08_S5_O3: 1268.0,
  T: 13.6,
  RH: 48.9,
  AH: 0.7578
};

// Make prediction request
fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => {
  console.log(`Predicted CO Level: ${data.prediction_co_gt} mg/m³`);
  console.log(`Out of Distribution: ${data.is_out_of_distribution}`);
  console.log(`Model Version: ${data.model_version}`);
  
  if (data.is_out_of_distribution) {
    console.warn("⚠️  WARNING: Anomalous sensor readings detected!");
  }
})
.catch(error => console.error('Error:', error));
```

### Python (Batch Predictions)

```python
import requests
import pandas as pd
from datetime import datetime

url = "https://co-prediction.onrender.com/predict"

# Load sensor data from CSV
sensor_data = pd.read_csv("sensor_readings.csv")

# Make predictions for each row
results = []
for _, row in sensor_data.iterrows():
    payload = {
        "DateTime": row['DateTime'],
        "PT08_S1_CO": row['PT08_S1_CO'],
        "NMHC_GT": row['NMHC_GT'],
        "C6H6_GT": row['C6H6_GT'],
        "PT08_S2_NMHC": row['PT08_S2_NMHC'],
        "NOx_GT": row['NOx_GT'],
        "PT08_S3_NOx": row['PT08_S3_NOx'],
        "NO2_GT": row['NO2_GT'],
        "PT08_S4_NO2": row['PT08_S4_NO2'],
        "PT08_S5_O3": row['PT08_S5_O3'],
        "T": row['T'],
        "RH": row['RH'],
        "AH": row['AH']
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        results.append(response.json())
    else:
        results.append({"error": response.status_code})

# Convert to DataFrame
predictions_df = pd.DataFrame(results)
print(predictions_df.head())

# Count OOD detections
ood_count = predictions_df['is_out_of_distribution'].sum()
print(f"\nTotal OOD detections: {ood_count} out of {len(predictions_df)}")
```

---

## Input Field Descriptions

| Field | Description | Unit | Typical Range |
|-------|-------------|------|---------------|
| `DateTime` | Timestamp of measurement | ISO 8601 format | Any valid datetime |
| `PT08_S1_CO` | Tin oxide CO sensor reading | - | 800-2000 |
| `NMHC_GT` | Non-Metanic Hydrocarbons | µg/m³ | 50-300 |
| `C6H6_GT` | Benzene concentration | µg/m³ | 2-30 |
| `PT08_S2_NMHC` | Titania NMHC sensor | - | 700-1500 |
| `NOx_GT` | Nitrogen Oxides | ppb | 50-400 |
| `PT08_S3_NOx` | Tungsten oxide NOx sensor | - | 600-1500 |
| `NO2_GT` | Nitrogen Dioxide | µg/m³ | 50-300 |
| `PT08_S4_NO2` | Tungsten oxide NO2 sensor | - | 1000-2500 |
| `PT08_S5_O3` | Indium oxide O3 sensor | - | 700-2000 |
| `T` | Temperature | °C | -5 to 45 |
| `RH` | Relative Humidity | % | 10-90 |
| `AH` | Absolute Humidity | g/m³ | 0.2-2.0 |

---

## Interactive Documentation

Visit the Swagger UI for interactive API testing:

**Production:** [https://co-prediction.onrender.com/docs](https://co-prediction.onrender.com/docs)

**Local:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The Swagger UI allows you to:
- Test API endpoints directly in your browser
- View detailed request/response schemas
- Download OpenAPI specification
- Generate client code

---

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing:
- Rate limiting per IP address
- API key-based quotas
- Request throttling

---

## Best Practices

1. **Always check the `is_out_of_distribution` flag**
   - If `true`, the prediction may be unreliable
   - Investigate sensor readings for potential issues

2. **Use ISO 8601 format for DateTime**
   - Example: `2025-10-20T18:00:00`
   - Include timezone if needed: `2025-10-20T18:00:00Z`

3. **Validate sensor readings before sending**
   - Check for negative values
   - Ensure values are within reasonable ranges
   - Handle missing data appropriately

4. **Implement error handling**
   - Always check HTTP status codes
   - Handle network timeouts
   - Retry failed requests with exponential backoff

5. **Monitor API performance**
   - Track response times
   - Log prediction results
   - Monitor OOD detection rates

---

## Support

For issues or questions:
- GitHub: [https://github.com/YaswanthDonthuboyina/Co-Prediction](https://github.com/YaswanthDonthuboyina/Co-Prediction)
- Email: Contact repository owner

---

**Last Updated:** December 2025  
**API Version:** 1.0.0
