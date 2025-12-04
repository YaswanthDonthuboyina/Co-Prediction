# Troubleshooting Guide

## Table of Contents
- [Installation Issues](#installation-issues)
- [Training Pipeline Issues](#training-pipeline-issues)
- [API Issues](#api-issues)
- [Docker Issues](#docker-issues)
- [Model Performance Issues](#model-performance-issues)
- [Data Issues](#data-issues)
- [Common Error Messages](#common-error-messages)
- [FAQ](#faq)

---

## Installation Issues

### Problem: `pip install` fails with dependency conflicts

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solutions:**

1. **Use a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. **Install with specific versions:**
```bash
pip install pandas==2.0.0 numpy==1.24.0 scikit-learn==1.3.0
```

3. **Clear pip cache:**
```bash
pip cache purge
pip install -r requirements.txt
```

---

### Problem: `openpyxl` not found when loading Excel file

**Symptoms:**
```
ImportError: Missing optional dependency 'openpyxl'. Use pip or conda to install openpyxl.
```

**Solution:**
```bash
pip install openpyxl
```

---

### Problem: Python version incompatibility

**Symptoms:**
```
ERROR: This package requires Python >=3.8
```

**Solution:**
1. Check your Python version:
```bash
python --version
```

2. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

3. Use the correct Python version:
```bash
python3.10 -m venv venv
```

---

## Training Pipeline Issues

### Problem: Dataset file not found

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'AirQualityUCI.xlsx'
```

**Solutions:**

1. **Download the dataset:**
   - Visit [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Air+Quality)
   - Download the Air Quality Data Set
   - Extract and place `AirQualityUCI.xlsx` in the project root

2. **Verify file location:**
```bash
# On Windows
dir AirQualityUCI.xlsx

# On Linux/Mac
ls -la AirQualityUCI.xlsx
```

3. **Check file path in code:**
   - Ensure you're running the script from the project root
   - Update `DATA_FILE_PATH` in `src/train.py` if needed

---

### Problem: Training script fails with memory error

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. **Reduce data size:**
```python
# In src/train.py, add after loading data:
data = data.sample(frac=0.5, random_state=42)  # Use 50% of data
```

2. **Reduce model complexity:**
```python
# In src/train.py, modify model parameters:
model = GradientBoostingRegressor(
    n_estimators=100,  # Reduced from 200
    max_depth=3,       # Reduced from 4
    random_state=42
)
```

3. **Close other applications to free up RAM**

---

### Problem: Training completes but models are not saved

**Symptoms:**
- No error messages
- `models/` directory is empty

**Solutions:**

1. **Check directory permissions:**
```bash
# On Windows
icacls models

# On Linux/Mac
ls -ld models
chmod 755 models
```

2. **Manually create models directory:**
```bash
mkdir models
```

3. **Check disk space:**
```bash
# On Windows
dir

# On Linux/Mac
df -h
```

---

### Problem: High number of outliers removed

**Symptoms:**
```
Removed 2500 outliers. Data shape is now (6000, 20).
```

**Solutions:**

1. **Adjust Z-score threshold:**
```python
# In src/train.py, line 52:
outlier_mask = (np.abs(z_scores) > 4).any(axis=1)  # Changed from 3 to 4
```

2. **Use IQR method instead:**
```python
# Replace Z-score outlier detection with:
Q1 = features_for_outlier_detection.quantile(0.25)
Q3 = features_for_outlier_detection.quantile(0.75)
IQR = Q3 - Q1
outlier_mask = ((features_for_outlier_detection < (Q1 - 1.5 * IQR)) | 
                (features_for_outlier_detection > (Q3 + 1.5 * IQR))).any(axis=1)
```

---

## API Issues

### Problem: API fails to start

**Symptoms:**
```
Error loading assets: [Errno 2] No such file or directory: 'models/co_predictor_model.joblib'
```

**Solution:**
1. **Train the model first:**
```bash
python src/train.py
```

2. **Verify models exist:**
```bash
ls models/
# Should show: co_predictor_model.joblib, scaler.joblib, ood_detector.joblib
```

---

### Problem: API returns 422 Validation Error

**Symptoms:**
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

**Solutions:**

1. **Check all required fields are present:**
```python
required_fields = [
    "DateTime", "PT08_S1_CO", "NMHC_GT", "C6H6_GT", 
    "PT08_S2_NMHC", "NOx_GT", "PT08_S3_NOx", "NO2_GT",
    "PT08_S4_NO2", "PT08_S5_O3", "T", "RH", "AH"
]
```

2. **Verify data types:**
   - All sensor values should be `float`
   - DateTime should be ISO 8601 string: `"2025-10-20T18:00:00"`

3. **Use the example payload from docs:**
```bash
curl -X GET "http://127.0.0.1:8000/docs"
# Copy the example from the Swagger UI
```

---

### Problem: API is slow or times out

**Symptoms:**
- Requests take >5 seconds
- Connection timeout errors

**Solutions:**

1. **Check if models are loaded:**
```python
# In src/predict.py, models are loaded at import time
# Restart the API server to reload models
```

2. **Optimize feature engineering:**
```python
# Cache feature engineering results if making multiple predictions
```

3. **Use async endpoints (advanced):**
```python
# In api/app.py:
@app.post("/predict")
async def predict_co_level(input_data: PredictionInput):
    # ... existing code
```

---

### Problem: CORS errors when calling API from browser

**Symptoms:**
```
Access to fetch at 'http://127.0.0.1:8000/predict' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:**

1. **Add CORS middleware to API:**
```python
# In api/app.py, add:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Docker Issues

### Problem: Docker build fails

**Symptoms:**
```
ERROR [stage-0 3/5] RUN --mount=type=cache,target=/root/.cache/pip
```

**Solutions:**

1. **Update Docker to latest version**

2. **Use legacy builder:**
```bash
DOCKER_BUILDKIT=0 docker build -t co-predictor-api .
```

3. **Check Dockerfile syntax:**
```bash
docker build --no-cache -t co-predictor-api .
```

---

### Problem: Docker container exits immediately

**Symptoms:**
```
docker ps
# Container not running
```

**Solutions:**

1. **Check container logs:**
```bash
docker logs <container_id>
```

2. **Run in interactive mode:**
```bash
docker run -it co-predictor-api /bin/bash
```

3. **Verify models are included in image:**
```bash
docker run co-predictor-api ls -la models/
```

---

### Problem: Cannot access API in Docker container

**Symptoms:**
- Container is running
- Cannot access `http://localhost:8000`

**Solutions:**

1. **Check port mapping:**
```bash
docker run -p 8000:8000 co-predictor-api
```

2. **Verify container is listening on 0.0.0.0:**
```bash
# In Dockerfile, CMD should include:
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Check firewall settings:**
```bash
# On Windows, allow port 8000 in Windows Firewall
```

---

## Model Performance Issues

### Problem: Low R² score (<0.8)

**Symptoms:**
```
R-squared (R²): 0.6543
```

**Solutions:**

1. **Check data quality:**
```python
# In src/data_preprocessing.py, verify:
print(data.isna().sum())  # Should be 0
print(data.describe())     # Check for unrealistic values
```

2. **Increase model complexity:**
```python
model = GradientBoostingRegressor(
    n_estimators=300,      # Increased from 200
    learning_rate=0.05,    # Decreased from 0.1
    max_depth=5,           # Increased from 4
    subsample=0.8,
    random_state=42
)
```

3. **Add more features:**
```python
# In src/feature_engineering.py, add:
df['Temp_RH'] = df['T'] * df['RH']
df['NOx_Temp'] = df['NOx(GT)'] * df['T']
```

---

### Problem: High OOD detection rate (>20%)

**Symptoms:**
```
Out of 100 predictions, 35 flagged as OOD
```

**Solutions:**

1. **Adjust contamination parameter:**
```python
# In src/train.py, line 77:
ood_detector = IsolationForest(
    contamination=0.1,  # Increased from 0.05
    n_estimators=300,
    random_state=42
)
```

2. **Retrain OOD detector on more diverse data:**
```python
# Include validation set in OOD training
X_combined = np.vstack([X_train_scaled, X_test_scaled])
ood_detector.fit(X_combined)
```

3. **Check input data distribution:**
```python
# Verify input data matches training data distribution
import matplotlib.pyplot as plt
plt.hist(input_data['PT08_S1_CO'])
plt.show()
```

---

### Problem: Predictions are always the same value

**Symptoms:**
```
All predictions return: 2.5
```

**Solutions:**

1. **Check if scaler is fitted correctly:**
```python
# In src/train.py, verify:
print(scaler.mean_)
print(scaler.scale_)
```

2. **Verify feature engineering is working:**
```python
# In src/predict.py, add debug prints:
print(featured_df.head())
print(aligned_df.head())
```

3. **Retrain the model:**
```bash
rm -rf models/*
python src/train.py
```

---

## Data Issues

### Problem: Missing values in dataset

**Symptoms:**
```
ValueError: Input contains NaN, infinity or a value too large
```

**Solutions:**

1. **Check interpolation:**
```python
# In src/data_preprocessing.py, verify:
print(f"NaN count before interpolation: {data.isna().sum().sum()}")
data = data.interpolate(method='linear', limit_direction='both')
print(f"NaN count after interpolation: {data.isna().sum().sum()}")
```

2. **Use forward/backward fill:**
```python
data.fillna(method='ffill', inplace=True)
data.fillna(method='bfill', inplace=True)
```

---

### Problem: DateTime parsing errors

**Symptoms:**
```
ValueError: time data '10/03/2004 18.00.00' does not match format
```

**Solutions:**

1. **Check DateTime format:**
```python
# In src/data_preprocessing.py, add:
print(data['Date'].head())
print(data['Time'].head())
```

2. **Use flexible parsing:**
```python
data['DateTime'] = pd.to_datetime(
    data['Date'].astype(str) + " " + data['Time'], 
    format='%d/%m/%Y %H.%M.%S',
    errors='coerce'
)
```

---

## Common Error Messages

### `ModuleNotFoundError: No module named 'src'`

**Cause:** Running script from wrong directory

**Solution:**
```bash
# Always run from project root
cd /path/to/project
python src/train.py
```

---

### `KeyError: 'PT08.S1(CO)'`

**Cause:** Column name mismatch between training and prediction

**Solution:**
1. Check column names in `api/app.py` rename_map
2. Verify feature engineering produces consistent column names

---

### `ValueError: X has 20 features, but StandardScaler is expecting 18 features`

**Cause:** Feature mismatch between training and inference

**Solution:**
1. Ensure feature engineering is identical in train and predict
2. Retrain the model:
```bash
python src/train.py
```

---

### `RuntimeError: Model file is corrupted`

**Cause:** Incomplete model save or version mismatch

**Solution:**
```bash
# Delete and retrain
rm models/*.joblib
python src/train.py
```

---

## FAQ

### Q: How often should I retrain the model?

**A:** Retrain when:
- OOD detection rate increases significantly (>15%)
- New sensor locations are added
- Seasonal changes occur (quarterly recommended)
- Model performance degrades (R² drops >5%)

---

### Q: Can I use this model for different locations?

**A:** 
- **Same city/region:** Yes, with fine-tuning
- **Different climate:** Requires retraining with local data
- **Different sensors:** Requires full retraining

---

### Q: What does the OOD flag mean?

**A:** 
- `is_out_of_distribution: true` means:
  - Input data is unusual compared to training data
  - Prediction may be unreliable
  - Check sensor calibration
  - Possible sensor malfunction

---

### Q: How accurate are the predictions?

**A:**
- **R² Score:** 0.916 (91.6% variance explained)
- **MAE:** ~0.3 mg/m³
- **RMSE:** ~0.4 mg/m³
- See [MODEL_PERFORMANCE.md](MODEL_PERFORMANCE.md) for details

---

### Q: Can I add more features?

**A:** Yes, modify `src/feature_engineering.py`:
```python
def create_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    # Add your custom features here
    df['custom_feature'] = df['T'] * df['RH'] / 100
    return df
```

Then retrain the model.

---

### Q: How do I update the model in production?

**A:**
1. Train new model locally
2. Test thoroughly
3. Update model version in `src/predict.py`
4. Replace model files in production
5. Restart API server
6. Monitor predictions for anomalies

---

### Q: What if the API is down?

**A:**
1. Check Render dashboard: https://dashboard.render.com
2. View logs for errors
3. Restart service if needed
4. Use local deployment as backup:
```bash
uvicorn api.app:app --reload
```

---

## Getting Help

If you encounter issues not covered here:

1. **Check logs:**
```bash
# API logs
docker logs <container_id>

# Training logs
python src/train.py 2>&1 | tee training.log
```

2. **Enable debug mode:**
```python
# In api/app.py:
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **Create GitHub issue:**
   - Include error message
   - Include steps to reproduce
   - Include Python version and OS

4. **Contact:**
   - GitHub: [YaswanthDonthuboyina/Co-Prediction](https://github.com/YaswanthDonthuboyina/Co-Prediction)

---

**Last Updated:** December 2025  
**Version:** 1.0.0
