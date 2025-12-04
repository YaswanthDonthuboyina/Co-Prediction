# Documentation Index

Welcome to the AirGuard CO Forecasting & Anomaly Detection System documentation. This comprehensive guide covers all aspects of the system from API usage to system architecture.

---

## 📚 Documentation Overview

### Quick Start
- **[README.md](../README.md)** - Project overview, setup instructions, and quick start guide

### Core Documentation

#### 1. **[API Usage Guide](API_USAGE_GUIDE.md)** 📡
Complete guide to using the AirGuard API, including:
- Endpoint documentation
- Request/response formats
- Code examples (Python, JavaScript, cURL)
- Field descriptions
- Best practices
- Interactive documentation (Swagger UI)

**Use this when:** You want to integrate the API into your application or make predictions.

---

#### 2. **[System Architecture](ARCHITECTURE.md)** 🏗️
Detailed system architecture documentation covering:
- High-level architecture overview
- Component diagrams
- Data flow diagrams
- Module descriptions
- Technology stack
- Deployment architecture
- Security considerations
- Scalability design

**Use this when:** You want to understand how the system works internally or plan to extend it.

---

#### 3. **[Model Performance Benchmarks](MODEL_PERFORMANCE.md)** 📊
Comprehensive model performance analysis including:
- Performance metrics (R², MAE, RMSE)
- Cross-validation results
- Model comparison with baselines
- OOD detection performance
- Feature importance analysis
- Computational performance
- Benchmark comparisons with literature
- Validation methodology

**Use this when:** You want to understand model accuracy, compare with other approaches, or validate results.

---

#### 4. **[Troubleshooting Guide](TROUBLESHOOTING.md)** 🔧
Solutions to common issues covering:
- Installation problems
- Training pipeline issues
- API errors
- Docker deployment issues
- Model performance problems
- Data issues
- Common error messages
- FAQ

**Use this when:** You encounter errors or unexpected behavior.

---

## 🗂️ Documentation Structure

```
docs/
├── README.md                    # This file - Documentation index
├── API_USAGE_GUIDE.md          # API usage and integration guide
├── ARCHITECTURE.md              # System architecture documentation
├── MODEL_PERFORMANCE.md         # Model benchmarks and metrics
├── TROUBLESHOOTING.md          # Common issues and solutions
└── images/                      # Architecture diagrams
    ├── architecture_diagram.png
    └── data_flow_diagram.png
```

---

## 🎯 Quick Navigation by Use Case

### I want to...

#### **Use the API**
1. Start with [API Usage Guide](API_USAGE_GUIDE.md)
2. Check [Swagger UI](https://co-prediction.onrender.com/docs) for interactive testing
3. Review code examples in the API guide

#### **Understand the System**
1. Read [README.md](../README.md) for overview
2. Study [System Architecture](ARCHITECTURE.md) for details
3. Review [Model Performance](MODEL_PERFORMANCE.md) for metrics

#### **Deploy the System**
1. Follow setup in [README.md](../README.md)
2. Check [Architecture - Deployment](ARCHITECTURE.md#deployment-architecture) section
3. Refer to [Troubleshooting](TROUBLESHOOTING.md) if issues arise

#### **Improve the Model**
1. Review [Model Performance](MODEL_PERFORMANCE.md) for current metrics
2. Check [Architecture - Module Descriptions](ARCHITECTURE.md#module-descriptions)
3. Examine training code in `src/train.py`

#### **Fix an Error**
1. Check [Troubleshooting Guide](TROUBLESHOOTING.md) first
2. Review [Common Error Messages](TROUBLESHOOTING.md#common-error-messages)
3. Check [FAQ](TROUBLESHOOTING.md#faq)

#### **Extend the System**
1. Understand [System Architecture](ARCHITECTURE.md)
2. Review [Module Descriptions](ARCHITECTURE.md#module-descriptions)
3. Check [Future Enhancements](ARCHITECTURE.md#future-architecture-enhancements)

---

## 📖 Reading Paths

### For Data Scientists

```
1. README.md (Overview)
   ↓
2. MODEL_PERFORMANCE.md (Metrics & Validation)
   ↓
3. ARCHITECTURE.md (Feature Engineering & Training)
   ↓
4. notebooks/co_prediction.ipynb (Exploratory Analysis)
```

### For Software Engineers

```
1. README.md (Overview)
   ↓
2. ARCHITECTURE.md (System Design)
   ↓
3. API_USAGE_GUIDE.md (API Specification)
   ↓
4. TROUBLESHOOTING.md (Operational Issues)
```

### For DevOps Engineers

```
1. README.md (Setup Instructions)
   ↓
2. ARCHITECTURE.md (Deployment Architecture)
   ↓
3. Dockerfile & compose.yaml (Container Configuration)
   ↓
4. TROUBLESHOOTING.md (Docker Issues)
```

### For API Consumers

```
1. API_USAGE_GUIDE.md (Complete API Documentation)
   ↓
2. Swagger UI (Interactive Testing)
   ↓
3. TROUBLESHOOTING.md (API Errors)
```

---

## 🔍 Key Concepts

### Out-of-Distribution (OOD) Detection
The system implements two types of OOD detection:
1. **Pre-processing OOD** (Training): Z-score based outlier removal
2. **Inference-time OOD** (Runtime): Isolation Forest anomaly detection

Learn more:
- [Architecture - OOD Detection](ARCHITECTURE.md#module-descriptions)
- [Model Performance - OOD Metrics](MODEL_PERFORMANCE.md#ood-detection-performance)

### Feature Engineering
The system creates 20 features from 13 raw sensor readings:
- Temporal features (hour, day, month, etc.)
- Cyclical encoding (sin/cos for hour)
- Interaction features (NOx×NO2, etc.)

Learn more:
- [Architecture - Feature Engineering Module](ARCHITECTURE.md#2-feature-engineering-module)
- [Model Performance - Feature Importance](MODEL_PERFORMANCE.md#feature-importance)

### Model Pipeline
Training: Data → Preprocessing → Feature Engineering → Outlier Removal → Scaling → Model Training  
Inference: Input → Feature Engineering → Scaling → OOD Detection → Prediction

Learn more:
- [Architecture - Data Flow](ARCHITECTURE.md#data-flow)
- [Model Performance - Training Configuration](MODEL_PERFORMANCE.md#training-configuration)

---

## 📊 Performance Summary

| Metric | Value |
|--------|-------|
| **R² Score** | 0.916 |
| **MAE** | 0.32 mg/m³ |
| **RMSE** | 0.42 mg/m³ |
| **OOD Accuracy** | 96% |
| **Inference Time** | ~15ms |

See [Model Performance](MODEL_PERFORMANCE.md) for complete benchmarks.

---

## 🔗 External Resources

### Official Links
- **GitHub Repository:** [YaswanthDonthuboyina/Co-Prediction](https://github.com/YaswanthDonthuboyina/Co-Prediction)
- **Production API:** [https://co-prediction.onrender.com](https://co-prediction.onrender.com)
- **API Documentation:** [https://co-prediction.onrender.com/docs](https://co-prediction.onrender.com/docs)

### Dataset
- **UCI Repository:** [Air Quality Data Set](https://archive.ics.uci.edu/ml/datasets/Air+Quality)

### Technologies
- **FastAPI:** [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **scikit-learn:** [https://scikit-learn.org](https://scikit-learn.org)
- **Docker:** [https://www.docker.com](https://www.docker.com)

---

## 🆘 Getting Help

### Documentation Issues
If you find errors or have suggestions for improving the documentation:
1. Open an issue on GitHub
2. Submit a pull request with corrections
3. Contact the repository owner

### Technical Support
For technical issues:
1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search existing GitHub issues
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)

---

## 📝 Documentation Standards

All documentation follows these standards:
- **Markdown format** for easy reading and version control
- **Code examples** are tested and working
- **Clear headings** for easy navigation
- **Tables** for structured information
- **Diagrams** for visual understanding
- **Links** for cross-referencing

---

## 🔄 Documentation Updates

| Document | Last Updated | Version |
|----------|--------------|---------|
| README.md | Dec 2025 | 1.0.0 |
| API_USAGE_GUIDE.md | Dec 2025 | 1.0.0 |
| ARCHITECTURE.md | Dec 2025 | 1.0.0 |
| MODEL_PERFORMANCE.md | Dec 2025 | 1.0.0 |
| TROUBLESHOOTING.md | Dec 2025 | 1.0.0 |

---

## 📋 Checklist for New Users

- [ ] Read [README.md](../README.md) for project overview
- [ ] Set up development environment (Python, dependencies)
- [ ] Download dataset from UCI repository
- [ ] Run training pipeline: `python src/train.py`
- [ ] Start API server: `uvicorn api.app:app --reload`
- [ ] Test API using [Swagger UI](http://127.0.0.1:8000/docs)
- [ ] Review [API Usage Guide](API_USAGE_GUIDE.md) for integration
- [ ] Check [Model Performance](MODEL_PERFORMANCE.md) to understand accuracy
- [ ] Bookmark [Troubleshooting Guide](TROUBLESHOOTING.md) for reference

---

## 🎓 Learning Path

### Beginner (New to the Project)
1. ✅ Read README.md
2. ✅ Follow setup instructions
3. ✅ Run the training pipeline
4. ✅ Test the API locally
5. ✅ Review API Usage Guide

### Intermediate (Understanding the System)
1. ✅ Study System Architecture
2. ✅ Review Model Performance metrics
3. ✅ Examine source code in `src/`
4. ✅ Explore Jupyter notebook
5. ✅ Test Docker deployment

### Advanced (Extending the System)
1. ✅ Understand complete architecture
2. ✅ Review feature engineering logic
3. ✅ Implement custom features
4. ✅ Optimize model hyperparameters
5. ✅ Add monitoring and logging
6. ✅ Implement CI/CD pipeline

---

## 💡 Best Practices

When using this documentation:

1. **Start with the README** - Get the big picture first
2. **Use the search function** - Most documentation is searchable
3. **Follow code examples** - They're tested and working
4. **Check diagrams** - Visual understanding is powerful
5. **Refer to troubleshooting** - Save time on common issues
6. **Keep documentation updated** - Document your changes

---

## 🌟 Contributing to Documentation

We welcome documentation improvements! To contribute:

1. **Fork the repository**
2. **Make your changes** to documentation files
3. **Test all code examples** to ensure they work
4. **Submit a pull request** with clear description
5. **Follow existing formatting** and style

---

**Last Updated:** December 2025  
**Documentation Version:** 1.0.0

---

*This documentation is maintained by the AirGuard development team. For questions or feedback, please open an issue on GitHub.*
