# 🤖 AI Powered Stock Market Prediction System

A production-ready web application for predicting ASX200 stock market index prices using machine learning and time series analysis.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **Real-time Stock Data**: Fetches live ASX200 index data from Yahoo Finance
- **Multiple ML Models**:
  - ARIMA (AutoRegressive Integrated Moving Average)
  - SARIMA (Seasonal ARIMA)
  - Ridge Regression with Technical Indicators
  - Ensemble predictions combining all models
- **Technical Indicators**: RSI, MACD, Bollinger Bands, ATR, Stochastic Oscillator, and more
- **Interactive Dashboard**: Beautiful web interface with real-time charts
- **RESTful API**: Well-documented API endpoints for integration
- **Production Ready**: Docker support, logging, error handling, and deployment scripts

## 📊 Demo

The system provides:
- Historical price visualization (30 days)
- Multi-model price predictions (up to 30 days)
- Technical indicator analysis
- Model performance metrics

## 🏗️ Architecture

```
.
├── backend/                 # Flask API backend
│   ├── api/                # API routes and endpoints
│   ├── models/             # ML model classes
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   └── config/             # Configuration
├── frontend/               # Web dashboard
│   ├── index.html          # Main HTML page
│   ├── styles/             # CSS stylesheets
│   └── src/                # JavaScript application
├── data/                   # Data storage
│   ├── raw/                # Raw CSV data
│   ├── processed/          # Processed datasets
│   └── models/             # Saved ML models
├── notebooks/              # Jupyter notebooks for analysis
├── scripts/                # Utility scripts
└── tests/                  # Test suite
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- Virtual environment (recommended)
- Docker (optional, for containerized deployment)

### Installation

#### Option 1: Local Development

```bash
# Clone the repository
git clone <repository-url>
cd AIPoweredStockMarketPrediction

# Run the development server
./run_dev.sh
```

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Create necessary directories
4. Start the Flask development server

#### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p logs data/raw data/processed data/models

# Copy environment configuration
cp .env.example .env

# Run the application
export FLASK_APP=backend/app.py
flask run --host=0.0.0.0 --port=5000
```

#### Option 3: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost
# API: http://localhost/api
```

## 📱 Usage

### Web Dashboard

1. Open `http://localhost:5000` in your browser
2. Click **"Initialize System"** to load stock data
3. Click **"Train Models"** to train prediction models
4. Select forecast period and click **"Get Predictions"**

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Initialize System
```bash
POST /api/initialize
Content-Type: application/json

{
  "ticker": "^AXJO",
  "start_date": "2018-01-01"
}
```

#### Train Models
```bash
POST /api/train
Content-Type: application/json

{
  "train_ratio": 0.8
}
```

#### Get Predictions
```bash
GET /api/predict?days=5
```

#### Get Current Price
```bash
GET /api/current
```

#### Get Historical Data
```bash
GET /api/historical?days=30
```

#### Get Technical Indicators
```bash
GET /api/indicators
```

#### Refresh Data
```bash
POST /api/refresh
```

## 🔧 Configuration

Edit `.env` file to customize settings:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False

# Stock Configuration
DEFAULT_TICKER=^AXJO
START_DATE=2018-01-01

# Model Configuration
TRAIN_TEST_SPLIT=0.8
RANDOM_STATE=42
```

## 📊 Models

### ARIMA (1,1,1)
- Best for univariate time series
- MAPE: ~0.81%
- Captures trend and momentum

### SARIMA (1,1,1)(1,1,1,20)
- Accounts for seasonality
- MAPE: ~2.41%
- Monthly seasonal patterns

### Ridge Regression
- Uses 50+ technical indicators
- R² Score: 0.931
- Feature-rich predictions

### Ensemble
- Combines all models
- Weighted average predictions
- Improved robustness

## 🛠️ Development

### Project Structure

```python
# Backend package structure
backend/
├── __init__.py
├── app.py              # Flask application factory
├── api/
│   ├── __init__.py
│   └── routes.py       # API endpoints
├── models/
│   ├── __init__.py
│   └── predictor.py    # ML models
├── services/
│   ├── __init__.py
│   └── prediction_service.py
└── utils/
    ├── __init__.py
    └── data_loader.py  # Data fetching and preprocessing
```

### Running Tests

```bash
pytest tests/
pytest --cov=backend tests/
```

### Code Quality

```bash
# Format code
black backend/

# Lint code
flake8 backend/
```

## 📈 Technical Indicators

The system calculates:

- **Trend**: SMA (5,10,20,50,100,200), EMA (5,10,20,50,100,200)
- **Momentum**: RSI (14), MACD (12,26,9), Stochastic Oscillator
- **Volatility**: ATR (14), Bollinger Bands (20,2)
- **Volume**: OBV, Volume ROC, Money Flow Index
- **Lagged Features**: 1,2,3,5,10-day lags

## 🔄 Data Pipeline

### Automated Updates

```bash
# Update stock data
python scripts/update_data.py

# Retrain models
python scripts/train_models.py
```

### Cron Job Setup

```bash
# Edit crontab
crontab -e

# Add daily updates at 6 PM
0 18 * * 1-5 cd /path/to/project && python scripts/update_data.py
0 19 * * 1-5 cd /path/to/project && python scripts/train_models.py
```

## 📦 Dependencies

Core dependencies:
- **Flask** - Web framework
- **pandas** - Data manipulation
- **scikit-learn** - Machine learning
- **statsmodels** - Time series analysis
- **yfinance** - Stock data fetching
- **Chart.js** - Visualization

See `requirements.txt` for complete list.

## 🐳 Docker Deployment

### Production Deployment

```bash
# Build image
docker build -t stock-prediction .

# Run container
docker run -d -p 5000:5000 stock-prediction

# Or use Docker Compose
docker-compose up -d
```

### Environment Variables

```bash
docker run -d \
  -e FLASK_ENV=production \
  -e API_PORT=5000 \
  -p 5000:5000 \
  stock-prediction
```

## 📝 API Documentation

Full API documentation available at `/api/health` endpoint response.

Example response:
```json
{
  "status": "healthy",
  "service": "Stock Market Prediction API",
  "version": "1.0.0"
}
```

## ⚠️ Disclaimer

**This application is for educational and research purposes only.**

- Not financial advice
- Past performance doesn't guarantee future results
- Always consult financial professionals before trading
- Use predictions at your own risk

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Yahoo Finance for stock data
- ASX for market data
- Open source community

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🚀 Roadmap

- [ ] Add more stock indices (S&P 500, NASDAQ, etc.)
- [ ] Implement LSTM/GRU deep learning models
- [ ] Add sentiment analysis from news
- [ ] Real-time WebSocket updates
- [ ] User authentication and portfolio tracking
- [ ] Mobile app

---

**Built with ❤️ using Python, Flask, and Machine Learning**
