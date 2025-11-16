# API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently, no authentication is required. In production, implement JWT or API key authentication.

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Stock Market Prediction API",
  "version": "1.0.0"
}
```

### 2. Initialize System

Initialize the prediction service with stock data.

**Endpoint:** `POST /initialize`

**Request Body:**
```json
{
  "ticker": "^AXJO",
  "start_date": "2018-01-01"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Prediction service initialized",
  "ticker": "^AXJO"
}
```

### 3. Train Models

Train all prediction models.

**Endpoint:** `POST /train`

**Request Body:**
```json
{
  "train_ratio": 0.8
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Models trained successfully",
  "details": {
    "models_trained": ["arima", "sarima", "ml"],
    "train_samples": 1012,
    "test_samples": 254
  }
}
```

### 4. Get Predictions

Get stock price predictions for future days.

**Endpoint:** `GET /predict?days=5`

**Query Parameters:**
- `days` (integer, 1-30): Number of days to predict

**Response:**
```json
{
  "status": "success",
  "predictions": {
    "arima": {
      "dates": ["2025-11-17", "2025-11-18", ...],
      "prices": [8234.56, 8245.12, ...]
    },
    "sarima": {
      "dates": ["2025-11-17", "2025-11-18", ...],
      "prices": [8230.45, 8242.33, ...]
    },
    "ml": {
      "dates": ["2025-11-17"],
      "prices": [8238.90]
    },
    "ensemble": {
      "dates": ["2025-11-17", "2025-11-18", ...],
      "prices": [8234.64, 8243.81, ...]
    }
  }
}
```

### 5. Get Current Price

Get the latest stock price data.

**Endpoint:** `GET /current`

**Response:**
```json
{
  "status": "success",
  "data": {
    "date": "2025-11-16",
    "close": 8234.56,
    "high": 8256.78,
    "low": 8210.34,
    "volume": 12345678
  }
}
```

### 6. Get Historical Data

Get historical stock price data.

**Endpoint:** `GET /historical?days=30`

**Query Parameters:**
- `days` (integer, 1-365): Number of days of history

**Response:**
```json
{
  "status": "success",
  "data": {
    "dates": ["2025-10-17", "2025-10-18", ...],
    "close": [8100.45, 8120.67, ...],
    "high": [8125.34, 8145.23, ...],
    "low": [8075.12, 8095.45, ...],
    "volume": [10234567, 11345678, ...]
  }
}
```

### 7. Get Technical Indicators

Get latest technical indicator values.

**Endpoint:** `GET /indicators`

**Response:**
```json
{
  "status": "success",
  "indicators": {
    "RSI": 65.43,
    "MACD": 12.34,
    "MACD_Signal": 10.23,
    "BB_Upper": 8300.45,
    "BB_Lower": 8150.23,
    "BB_Middle": 8225.34,
    "ATR": 45.67,
    "Stochastic_%K": 72.34,
    "Stochastic_%D": 68.91
  }
}
```

### 8. Get Model Performance

Get information about trained models.

**Endpoint:** `GET /models`

**Response:**
```json
{
  "status": "success",
  "models": {
    "arima": {
      "status": "trained",
      "type": "ARIMA"
    },
    "sarima": {
      "status": "trained",
      "type": "SARIMA"
    },
    "ml": {
      "status": "trained",
      "type": "ML"
    }
  }
}
```

### 9. Refresh Data

Refresh stock data with latest information.

**Endpoint:** `POST /refresh`

**Response:**
```json
{
  "status": "success",
  "message": "Data refreshed successfully"
}
```

## Error Responses

All errors return appropriate HTTP status codes and JSON:

```json
{
  "status": "error",
  "message": "Error description here"
}
```

**Common Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (data not available)
- `500` - Internal Server Error

## Rate Limiting

Default: 100 requests per hour per IP

## CORS

CORS is enabled for all origins in development. Configure `CORS_ORIGINS` in `.env` for production.

## Examples

### Python

```python
import requests

# Initialize
response = requests.post('http://localhost:5000/api/initialize', json={
    'ticker': '^AXJO',
    'start_date': '2018-01-01'
})
print(response.json())

# Train models
response = requests.post('http://localhost:5000/api/train', json={
    'train_ratio': 0.8
})
print(response.json())

# Get predictions
response = requests.get('http://localhost:5000/api/predict?days=5')
print(response.json())
```

### cURL

```bash
# Initialize
curl -X POST http://localhost:5000/api/initialize \
  -H "Content-Type: application/json" \
  -d '{"ticker":"^AXJO","start_date":"2018-01-01"}'

# Get predictions
curl http://localhost:5000/api/predict?days=5

# Get current price
curl http://localhost:5000/api/current
```

### JavaScript

```javascript
// Initialize
const response = await fetch('http://localhost:5000/api/initialize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ticker: '^AXJO',
    start_date: '2018-01-01'
  })
});
const data = await response.json();
console.log(data);
```

## Workflow

Typical workflow for using the API:

1. **Initialize** - Load stock data
2. **Train** - Train prediction models
3. **Predict** - Get future predictions
4. **Refresh** - Update with latest data (optional)
5. **Retrain** - Retrain models with new data (optional)

## Notes

- First call to `/initialize` may take 10-30 seconds
- Training models may take 1-2 minutes
- Data is cached in memory for performance
- Use `/refresh` to update data without restarting server
