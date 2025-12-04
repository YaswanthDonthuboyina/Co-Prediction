# System Architecture

## Table of Contents
- [Overview](#overview)
- [High-Level Architecture](#high-level-architecture)
- [Component Diagram](#component-diagram)
- [Data Flow](#data-flow)
- [Module Descriptions](#module-descriptions)
- [Technology Stack](#technology-stack)
- [Deployment Architecture](#deployment-architecture)
- [Security Architecture](#security-architecture)

---

## Overview

AirGuard is an end-to-end machine learning system for predicting Carbon Monoxide (CO) levels from air quality sensor data. The system follows a modular architecture with clear separation between data processing, model training, and inference components.

### Design Principles

1. **Modularity:** Each component has a single, well-defined responsibility
2. **Reusability:** Shared preprocessing and feature engineering across train/predict
3. **Scalability:** Stateless API design for horizontal scaling
4. **Maintainability:** Clear code structure with comprehensive documentation
5. **Reproducibility:** Fixed random seeds and versioned dependencies

---

## High-Level Architecture

![Architecture Diagram](../docs/images/architecture_diagram.png)

### System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AirGuard System                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      │
│  │   Data       │      │   Training   │      │  Inference   │      │
│  │  Pipeline    │─────▶│   Pipeline   │─────▶│   Service    │      │
│  └──────────────┘      └──────────────┘      └──────────────┘      │
│         │                      │                      │              │
│         │                      │                      │              │
│         ▼                      ▼                      ▼              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      │
│  │  Cleaned     │      │   Trained    │      │     API      │      │
│  │   Data       │      │   Models     │      │  Endpoints   │      │
│  └──────────────┘      └──────────────┘      └──────────────┘      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Diagram

### Directory Structure

```
AirGuard/
│
├── src/                          # Core application code
│   ├── data_preprocessing.py    # Data cleaning & validation
│   ├── feature_engineering.py   # Feature creation & transformation
│   ├── train.py                 # Model training pipeline
│   └── predict.py               # Prediction service
│
├── api/                          # API layer
│   └── app.py                   # FastAPI application
│
├── models/                       # Persisted model artifacts
│   ├── co_predictor_model.joblib    # Trained GB model
│   ├── scaler.joblib                # StandardScaler
│   └── ood_detector.joblib          # Isolation Forest
│
├── notebooks/                    # Exploratory analysis
│   └── co_prediction.ipynb      # Model development notebook
│
├── docs/                         # Documentation
│   ├── API_USAGE_GUIDE.md
│   ├── TROUBLESHOOTING.md
│   ├── MODEL_PERFORMANCE.md
│   └── ARCHITECTURE.md
│
├── tests/                        # Unit tests (to be implemented)
│
├── Dockerfile                    # Container definition
├── compose.yaml                  # Docker Compose config
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview
```

---

## Data Flow

![Data Flow Diagram](../docs/images/data_flow_diagram.png)

### Training Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRAINING PIPELINE                             │
└─────────────────────────────────────────────────────────────────────┘

1. DATA INGESTION
   ┌──────────────────┐
   │ AirQualityUCI    │
   │    .xlsx         │
   └────────┬─────────┘
            │
            ▼
2. DATA PREPROCESSING (data_preprocessing.py)
   ┌──────────────────────────────────────┐
   │ • Replace -200 with NaN              │
   │ • Create DateTime index              │
   │ • Linear interpolation               │
   │ • Forward/backward fill              │
   └────────┬─────────────────────────────┘
            │
            ▼
3. FEATURE ENGINEERING (feature_engineering.py)
   ┌──────────────────────────────────────┐
   │ • Temporal features (hour, day, etc) │
   │ • Cyclical encoding (sin/cos)        │
   │ • Interaction features               │
   └────────┬─────────────────────────────┘
            │
            ▼
4. OUTLIER REMOVAL (train.py)
   ┌──────────────────────────────────────┐
   │ • Z-score calculation                │
   │ • Remove |Z| > 3                     │
   │ • 467 samples removed (5%)           │
   └────────┬─────────────────────────────┘
            │
            ▼
5. TRAIN/TEST SPLIT
   ┌──────────────────────────────────────┐
   │ • 80% Training (7,112 samples)       │
   │ • 20% Testing (1,778 samples)        │
   │ • Stratified by time                 │
   └────────┬─────────────────────────────┘
            │
            ▼
6. FEATURE SCALING
   ┌──────────────────────────────────────┐
   │ • StandardScaler (Z-score)           │
   │ • Fit on training set only           │
   │ • Transform train & test             │
   └────────┬─────────────────────────────┘
            │
            ├──────────────┬──────────────┬──────────────┐
            ▼              ▼              ▼              ▼
7. MODEL TRAINING (Parallel)
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │  Gradient   │  │  Standard   │  │  Isolation  │
   │  Boosting   │  │   Scaler    │  │   Forest    │
   │   Model     │  │             │  │ OOD Detector│
   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
          │                │                │
          ▼                ▼                ▼
8. MODEL PERSISTENCE
   ┌──────────────────────────────────────┐
   │ models/                              │
   │ ├── co_predictor_model.joblib        │
   │ ├── scaler.joblib                    │
   │ └── ood_detector.joblib              │
   └──────────────────────────────────────┘
```

### Inference Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                       INFERENCE PIPELINE                             │
└─────────────────────────────────────────────────────────────────────┘

1. API REQUEST
   ┌──────────────────┐
   │  POST /predict   │
   │  JSON Payload    │
   └────────┬─────────┘
            │
            ▼
2. INPUT VALIDATION (Pydantic)
   ┌──────────────────────────────────────┐
   │ • Check required fields              │
   │ • Validate data types                │
   │ • Parse DateTime                     │
   └────────┬─────────────────────────────┘
            │
            ▼
3. FEATURE ENGINEERING (predict.py)
   ┌──────────────────────────────────────┐
   │ • Same transformations as training   │
   │ • Temporal features                  │
   │ • Cyclical encoding                  │
   │ • Interaction features               │
   └────────┬─────────────────────────────┘
            │
            ▼
4. FEATURE ALIGNMENT
   ┌──────────────────────────────────────┐
   │ • Reindex to match training features │
   │ • Ensure correct column order        │
   │ • Fill missing with 0                │
   └────────┬─────────────────────────────┘
            │
            ▼
5. FEATURE SCALING
   ┌──────────────────────────────────────┐
   │ • Load saved scaler                  │
   │ • Transform input features           │
   └────────┬─────────────────────────────┘
            │
            ├──────────────┬──────────────┐
            ▼              ▼              │
6. PARALLEL PROCESSING                    │
   ┌─────────────┐  ┌─────────────┐      │
   │     OOD     │  │ Prediction  │      │
   │  Detection  │  │   (GB Model)│      │
   │ (Isolation  │  │             │      │
   │   Forest)   │  │             │      │
   └──────┬──────┘  └──────┬──────┘      │
          │                │              │
          ▼                ▼              │
7. RESPONSE ASSEMBLY
   ┌──────────────────────────────────────┐
   │ {                                    │
   │   "prediction_co_gt": 2.7635,        │
   │   "is_out_of_distribution": false,   │
   │   "model_version": "1.0.0"           │
   │ }                                    │
   └────────┬─────────────────────────────┘
            │
            ▼
8. JSON RESPONSE
   ┌──────────────────┐
   │  HTTP 200 OK     │
   │  JSON Response   │
   └──────────────────┘
```

---

## Module Descriptions

### 1. Data Preprocessing Module

**File:** `src/data_preprocessing.py`

**Responsibilities:**
- Load raw data from Excel/CSV
- Handle missing values (-200 sentinel values)
- Create DateTime index
- Interpolate missing data
- Validate data quality

**Key Functions:**
```python
def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Loads and cleans the Air Quality dataset.
    
    Returns:
        Cleaned DataFrame with DateTime index
    """
```

**Input:** `AirQualityUCI.xlsx` (9,357 rows × 15 columns)  
**Output:** Cleaned DataFrame (9,357 rows × 13 columns)

---

### 2. Feature Engineering Module

**File:** `src/feature_engineering.py`

**Responsibilities:**
- Create temporal features (hour, day, month, etc.)
- Encode cyclical features (sin/cos for hour)
- Generate interaction features
- Ensure feature consistency

**Key Functions:**
```python
def create_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers features for the air quality dataset.
    
    Returns:
        DataFrame with additional engineered features
    """
```

**Input:** 13 raw features  
**Output:** 20 total features (13 raw + 7 engineered)

---

### 3. Training Module

**File:** `src/train.py`

**Responsibilities:**
- Orchestrate entire training pipeline
- Remove outliers using Z-score
- Split data into train/test sets
- Fit scaler, model, and OOD detector
- Persist trained artifacts
- Evaluate model performance

**Key Components:**
```python
def main():
    """
    Main training pipeline:
    1. Load & clean data
    2. Engineer features
    3. Remove outliers
    4. Train/test split
    5. Fit scaler
    6. Train OOD detector
    7. Train prediction model
    8. Evaluate & save
    """
```

**Outputs:**
- `models/co_predictor_model.joblib` (485 KB)
- `models/scaler.joblib` (2 KB)
- `models/ood_detector.joblib` (4.4 MB)

---

### 4. Prediction Module

**File:** `src/predict.py`

**Responsibilities:**
- Load trained models at startup
- Process incoming prediction requests
- Apply feature engineering
- Detect out-of-distribution inputs
- Generate predictions
- Return structured responses

**Key Functions:**
```python
def make_prediction(*, input_data: dict) -> dict:
    """
    Makes a prediction using trained models.
    
    Args:
        input_data: Dictionary with sensor readings
        
    Returns:
        Dictionary with prediction and OOD flag
    """
```

**Performance:** ~5ms per prediction

---

### 5. API Module

**File:** `api/app.py`

**Responsibilities:**
- Expose REST API endpoints
- Validate input data (Pydantic)
- Handle HTTP requests/responses
- Map API field names to internal names
- Error handling and logging

**Endpoints:**
```python
GET  /           # Health check
POST /predict    # CO prediction
GET  /docs       # Swagger UI
```

**Framework:** FastAPI  
**Server:** Uvicorn (ASGI)

---

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Language** | Python | 3.10+ | Core implementation |
| **ML Framework** | scikit-learn | 1.3.0 | Model training & inference |
| **Data Processing** | pandas | 2.0.0 | Data manipulation |
| **Numerical Computing** | numpy | 1.24.0 | Array operations |
| **Statistical Analysis** | scipy | 1.11.0 | Statistical functions |
| **API Framework** | FastAPI | 0.104+ | REST API |
| **ASGI Server** | Uvicorn | 0.24+ | Production server |
| **Serialization** | joblib | 1.3+ | Model persistence |
| **Excel Support** | openpyxl | 3.1+ | Excel file reading |

### Development Tools

| Tool | Purpose |
|------|---------|
| **Docker** | Containerization |
| **Git** | Version control |
| **Jupyter** | Exploratory analysis |
| **pytest** | Unit testing (planned) |

---

## Deployment Architecture

### Local Development

```
┌─────────────────────────────────────────┐
│         Developer Machine               │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Python Virtual Environment       │ │
│  │                                   │ │
│  │  ┌─────────────┐  ┌────────────┐ │ │
│  │  │   Uvicorn   │  │   Models   │ │ │
│  │  │   Server    │  │   (local)  │ │ │
│  │  └──────┬──────┘  └────────────┘ │ │
│  │         │                         │ │
│  └─────────┼─────────────────────────┘ │
│            │                           │
│            ▼                           │
│    http://127.0.0.1:8000              │
└─────────────────────────────────────────┘
```

**Start Command:**
```bash
uvicorn api.app:app --reload
```

---

### Docker Deployment

```
┌─────────────────────────────────────────┐
│         Docker Container                │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Python 3.13 Slim Image           │ │
│  │                                   │ │
│  │  ┌─────────────┐  ┌────────────┐ │ │
│  │  │   Uvicorn   │  │   Models   │ │ │
│  │  │   Server    │  │ (bundled)  │ │ │
│  │  └──────┬──────┘  └────────────┘ │ │
│  │         │                         │ │
│  └─────────┼─────────────────────────┘ │
│            │                           │
│            ▼                           │
│    Port 8000 (exposed)                │
└─────────────────────────────────────────┘
         │
         ▼
Host Port 8000
```

**Build & Run:**
```bash
docker build -t co-predictor-api .
docker run -p 8000:8000 co-predictor-api
```

---

### Production Deployment (Render)

```
┌─────────────────────────────────────────────────────────────┐
│                    Render Platform                          │
│                                                             │
│  ┌───────────────┐      ┌──────────────────────────────┐  │
│  │  Load         │      │   Docker Container           │  │
│  │  Balancer     │─────▶│                              │  │
│  │  (HTTPS)      │      │  ┌────────────────────────┐  │  │
│  └───────────────┘      │  │  AirGuard API          │  │  │
│                         │  │  (Uvicorn)             │  │  │
│                         │  └────────────────────────┘  │  │
│                         │                              │  │
│                         │  ┌────────────────────────┐  │  │
│                         │  │  Persisted Models      │  │  │
│                         │  │  (in container)        │  │  │
│                         │  └────────────────────────┘  │  │
│                         └──────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
            https://co-prediction.onrender.com
```

**Features:**
- Automatic HTTPS/SSL
- Auto-scaling (horizontal)
- Health checks
- Automatic restarts
- CDN integration

---

## Security Architecture

### Current Security Measures

1. **Container Isolation:**
   - Non-root user in Docker container
   - Minimal base image (Python slim)
   - No unnecessary packages

2. **Input Validation:**
   - Pydantic schema validation
   - Type checking
   - DateTime parsing with error handling

3. **Error Handling:**
   - No sensitive information in error messages
   - Graceful degradation
   - Proper HTTP status codes

### Recommended Security Enhancements

1. **Authentication:**
```python
# Add API key authentication
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/predict")
async def predict(api_key: str = Depends(api_key_header)):
    # Validate API key
    pass
```

2. **Rate Limiting:**
```python
# Add rate limiting
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("100/minute")
async def predict():
    pass
```

3. **Input Sanitization:**
```python
# Add range validation
class PredictionInput(BaseModel):
    PT08_S1_CO: float = Field(gt=0, lt=10000)
    T: float = Field(gt=-50, lt=100)
    # ... etc
```

---

## Scalability Considerations

### Horizontal Scaling

```
                    ┌──────────────┐
                    │ Load Balancer│
                    └───────┬──────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  API Instance │   │  API Instance │   │  API Instance │
│      #1       │   │      #2       │   │      #3       │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Stateless Design Benefits:**
- Each instance is independent
- Models loaded in memory (no shared state)
- Easy to add/remove instances
- No session management needed

### Performance Optimization

1. **Model Loading:**
   - Load models once at startup (current)
   - Consider model caching service for large deployments

2. **Batch Predictions:**
   - Add batch endpoint for multiple predictions
   - Vectorize operations for efficiency

3. **Async Processing:**
   - Use async/await for I/O operations
   - Queue system for long-running tasks

---

## Monitoring Architecture

### Recommended Monitoring Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  FastAPI   │─▶│ Prometheus │─▶│  Grafana   │           │
│  │    App     │  │  Metrics   │  │ Dashboard  │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│         │                                                   │
│         ▼                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Logging   │─▶│ Centralized│─▶│   Alerts   │           │
│  │  (Python)  │  │    Logs    │  │  (Email/   │           │
│  │            │  │            │  │   Slack)   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

**Key Metrics to Monitor:**
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- OOD detection rate
- Model prediction distribution
- Resource usage (CPU, memory)

---

## Data Architecture

### Training Data Flow

```
UCI Repository
     │
     ▼
AirQualityUCI.xlsx (1.3 MB)
     │
     ▼
Data Preprocessing
     │
     ▼
Feature Engineering
     │
     ▼
Cleaned Dataset (in-memory)
     │
     ├──▶ Training Set (80%)
     │         │
     │         ▼
     │    Model Training
     │         │
     │         ▼
     │    Saved Models (models/)
     │
     └──▶ Test Set (20%)
               │
               ▼
          Evaluation
```

### Inference Data Flow

```
Client Request (JSON)
     │
     ▼
API Validation
     │
     ▼
Feature Engineering
     │
     ▼
Scaling (in-memory)
     │
     ├──▶ OOD Detection
     │         │
     │         ▼
     │    OOD Flag
     │
     └──▶ Prediction
               │
               ▼
          Response (JSON)
```

---

## Disaster Recovery

### Backup Strategy

1. **Model Artifacts:**
   - Stored in Git repository
   - Bundled in Docker image
   - Backed up to cloud storage (recommended)

2. **Training Data:**
   - Original dataset in repository
   - Versioned with Git LFS (recommended)

3. **Code:**
   - Version controlled in GitHub
   - Automated backups via Git

### Recovery Procedures

**Scenario 1: API Failure**
```bash
# Restart container
docker restart <container_id>

# Or rebuild and redeploy
docker build -t co-predictor-api .
docker run -p 8000:8000 co-predictor-api
```

**Scenario 2: Model Corruption**
```bash
# Retrain from scratch
python src/train.py

# Verify models
ls -lh models/
```

**Scenario 3: Complete System Failure**
```bash
# Clone repository
git clone https://github.com/YaswanthDonthuboyina/Co-Prediction.git

# Rebuild environment
pip install -r requirements.txt

# Retrain models
python src/train.py

# Redeploy
docker build -t co-predictor-api .
docker run -p 8000:8000 co-predictor-api
```

---

## Future Architecture Enhancements

### Phase 1: Operational Improvements
- [ ] Add comprehensive logging
- [ ] Implement monitoring dashboard
- [ ] Add health check endpoints
- [ ] Implement graceful shutdown

### Phase 2: Performance Enhancements
- [ ] Add batch prediction endpoint
- [ ] Implement model caching
- [ ] Add async processing
- [ ] Optimize feature engineering

### Phase 3: Advanced Features
- [ ] Model versioning system
- [ ] A/B testing framework
- [ ] Online learning pipeline
- [ ] Multi-model ensemble

### Phase 4: Enterprise Features
- [ ] Authentication & authorization
- [ ] Rate limiting & quotas
- [ ] Audit logging
- [ ] Data encryption at rest

---

## Conclusion

The AirGuard system follows a clean, modular architecture that separates concerns and enables easy maintenance and scaling. The stateless API design allows for horizontal scaling, while the containerized deployment ensures consistency across environments.

**Key Architectural Strengths:**
- ✅ Clear separation of concerns
- ✅ Reusable components
- ✅ Stateless design for scalability
- ✅ Container-based deployment
- ✅ Comprehensive error handling

**Recommended Next Steps:**
1. Implement comprehensive testing
2. Add monitoring and logging
3. Enhance security measures
4. Implement CI/CD pipeline

---

**Last Updated:** December 2025  
**Architecture Version:** 1.0.0
