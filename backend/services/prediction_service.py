import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from backend.utils.data_loader import StockDataLoader
from backend.models.predictor import ARIMAPredictor, SARIMAPredictor, MLPredictor, EnsemblePredictor

logger = logging.getLogger(__name__)

class PredictionService:
    """Service for managing stock predictions"""

    def __init__(self):
        self.data_loader = None
        self.models = {}
        self.current_data = None

    def initialize(self, ticker='^AXJO', start_date='2018-01-01'):
        """Initialize the prediction service"""
        logger.info(f"Initializing prediction service for {ticker}")
        self.data_loader = StockDataLoader(ticker=ticker, start_date=start_date)
        self.current_data = self.data_loader.prepare_features()
        logger.info("Prediction service initialized successfully")

    def train_models(self, train_ratio=0.8):
        """Train all prediction models"""
        if self.current_data is None:
            raise ValueError("Data not loaded. Call initialize() first.")

        logger.info("Training prediction models...")

        # Split data
        split_idx = int(len(self.current_data) * train_ratio)
        train_data = self.current_data[:split_idx]
        test_data = self.current_data[split_idx:]

        # Train ARIMA model
        try:
            arima_model = ARIMAPredictor(order=(1, 1, 1))
            arima_model.train(train_data['Close'])
            self.models['arima'] = arima_model
            logger.info("ARIMA model trained successfully")
        except Exception as e:
            logger.error(f"Failed to train ARIMA: {str(e)}")

        # Train SARIMA model
        try:
            sarima_model = SARIMAPredictor(order=(1, 1, 1), seasonal_order=(1, 1, 1, 20))
            sarima_model.train(train_data['Close'])
            self.models['sarima'] = sarima_model
            logger.info("SARIMA model trained successfully")
        except Exception as e:
            logger.error(f"Failed to train SARIMA: {str(e)}")

        # Train ML model with features
        try:
            feature_cols = [col for col in train_data.columns
                          if col not in ['Date', 'Target_Next_Close', 'Target_Direction']
                          and not pd.isna(train_data[col]).all()]

            X_train = train_data[feature_cols].select_dtypes(include=[np.number])
            y_train = train_data['Target_Next_Close']

            # Remove any rows with NaN
            mask = ~(X_train.isna().any(axis=1) | y_train.isna())
            X_train = X_train[mask]
            y_train = y_train[mask]

            ml_model = MLPredictor(model_type='ridge')
            ml_model.train(X_train, y_train)
            self.models['ml'] = ml_model
            self.feature_cols = feature_cols
            logger.info("ML model trained successfully")
        except Exception as e:
            logger.error(f"Failed to train ML model: {str(e)}")

        return {
            'models_trained': list(self.models.keys()),
            'train_samples': len(train_data),
            'test_samples': len(test_data)
        }

    def predict_next_days(self, days=5):
        """Predict stock prices for next N days"""
        if not self.models:
            raise ValueError("Models not trained. Call train_models() first.")

        predictions = {}
        last_date = self.current_data['Date'].max()

        # Generate future dates
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        # Filter out weekends
        future_dates = [d for d in future_dates if d.weekday() < 5][:days]

        # ARIMA predictions
        if 'arima' in self.models:
            try:
                arima_pred = self.models['arima'].predict(steps=days)
                predictions['arima'] = {
                    'dates': [d.strftime('%Y-%m-%d') for d in future_dates],
                    'prices': arima_pred.tolist()
                }
            except Exception as e:
                logger.error(f"ARIMA prediction failed: {str(e)}")

        # SARIMA predictions
        if 'sarima' in self.models:
            try:
                sarima_pred = self.models['sarima'].predict(steps=days)
                predictions['sarima'] = {
                    'dates': [d.strftime('%Y-%m-%d') for d in future_dates],
                    'prices': sarima_pred.tolist()
                }
            except Exception as e:
                logger.error(f"SARIMA prediction failed: {str(e)}")

        # ML predictions (requires feature engineering for future dates)
        if 'ml' in self.models:
            try:
                # Use last known features as a simple baseline
                last_features = self.current_data[self.feature_cols].iloc[-1:].select_dtypes(include=[np.number])
                ml_pred = self.models['ml'].predict(last_features)
                predictions['ml'] = {
                    'dates': [future_dates[0].strftime('%Y-%m-%d')],
                    'prices': ml_pred.tolist()
                }
            except Exception as e:
                logger.error(f"ML prediction failed: {str(e)}")

        # Ensemble prediction (average of all models)
        if len(predictions) > 1:
            ensemble_prices = []
            for i in range(len(future_dates)):
                prices_at_i = []
                for model_name, pred_data in predictions.items():
                    if i < len(pred_data['prices']):
                        prices_at_i.append(pred_data['prices'][i])
                if prices_at_i:
                    ensemble_prices.append(np.mean(prices_at_i))

            predictions['ensemble'] = {
                'dates': [d.strftime('%Y-%m-%d') for d in future_dates[:len(ensemble_prices)]],
                'prices': ensemble_prices
            }

        return predictions

    def get_current_price(self):
        """Get the latest stock price"""
        if self.current_data is None:
            return None

        latest = self.current_data.iloc[-1]
        return {
            'date': latest['Date'].strftime('%Y-%m-%d') if isinstance(latest['Date'], pd.Timestamp) else str(latest['Date']),
            'close': float(latest['Close']),
            'high': float(latest['High']),
            'low': float(latest['Low']),
            'volume': int(latest['Volume'])
        }

    def get_historical_data(self, days=30):
        """Get historical stock data"""
        if self.current_data is None:
            return None

        recent_data = self.current_data.tail(days)

        return {
            'dates': [d.strftime('%Y-%m-%d') if isinstance(d, pd.Timestamp) else str(d)
                     for d in recent_data['Date']],
            'close': recent_data['Close'].tolist(),
            'high': recent_data['High'].tolist(),
            'low': recent_data['Low'].tolist(),
            'volume': recent_data['Volume'].tolist()
        }

    def get_technical_indicators(self):
        """Get latest technical indicators"""
        if self.current_data is None:
            return None

        latest = self.current_data.iloc[-1]

        indicators = {}
        for col in self.current_data.columns:
            if col in ['RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Lower', 'BB_Middle',
                      'ATR', 'Stochastic_%K', 'Stochastic_%D']:
                if col in latest and not pd.isna(latest[col]):
                    indicators[col] = float(latest[col])

        return indicators

    def get_model_performance(self):
        """Get performance metrics for trained models"""
        if not self.models:
            return {}

        performance = {}
        # This is a simplified version - in production, you'd evaluate on test set
        for model_name in self.models.keys():
            performance[model_name] = {
                'status': 'trained',
                'type': model_name.upper()
            }

        return performance

    def refresh_data(self):
        """Refresh stock data with latest information"""
        logger.info("Refreshing stock data...")
        self.current_data = self.data_loader.prepare_features()
        logger.info("Stock data refreshed successfully")
        return True
