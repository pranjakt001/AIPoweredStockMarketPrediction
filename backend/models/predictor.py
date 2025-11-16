import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
import logging

logger = logging.getLogger(__name__)

class StockPredictor:
    """Base class for stock prediction models"""

    def __init__(self, model_type='arima'):
        self.model_type = model_type
        self.model = None
        self.is_fitted = False

    def train(self, data):
        """Train the model"""
        raise NotImplementedError

    def predict(self, steps=1):
        """Make predictions"""
        raise NotImplementedError

    def evaluate(self, y_true, y_pred):
        """Evaluate model performance"""
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        metrics = {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'mape': float(mape),
            'r2': float(r2)
        }

        return metrics

    def save_model(self, filepath):
        """Save model to disk"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before saving")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """Load model from disk"""
        self.model = joblib.load(filepath)
        self.is_fitted = True
        logger.info(f"Model loaded from {filepath}")


class ARIMAPredictor(StockPredictor):
    """ARIMA model for time series prediction"""

    def __init__(self, order=(1, 1, 1)):
        super().__init__(model_type='arima')
        self.order = order

    def train(self, data):
        """Train ARIMA model"""
        try:
            logger.info(f"Training ARIMA model with order {self.order}")
            self.model = ARIMA(data, order=self.order)
            self.model = self.model.fit()
            self.is_fitted = True
            logger.info("ARIMA model training completed")
            return self.model
        except Exception as e:
            logger.error(f"Error training ARIMA model: {str(e)}")
            raise

    def predict(self, steps=1):
        """Predict future values"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before prediction")

        forecast = self.model.forecast(steps=steps)
        return forecast


class SARIMAPredictor(StockPredictor):
    """SARIMA model for time series prediction with seasonality"""

    def __init__(self, order=(1, 1, 1), seasonal_order=(1, 1, 1, 20)):
        super().__init__(model_type='sarima')
        self.order = order
        self.seasonal_order = seasonal_order

    def train(self, data):
        """Train SARIMA model"""
        try:
            logger.info(f"Training SARIMA model with order {self.order}, seasonal {self.seasonal_order}")
            self.model = SARIMAX(data, order=self.order, seasonal_order=self.seasonal_order)
            self.model = self.model.fit(disp=False)
            self.is_fitted = True
            logger.info("SARIMA model training completed")
            return self.model
        except Exception as e:
            logger.error(f"Error training SARIMA model: {str(e)}")
            raise

    def predict(self, steps=1):
        """Predict future values"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before prediction")

        forecast = self.model.forecast(steps=steps)
        return forecast


class MLPredictor(StockPredictor):
    """Machine Learning based predictor using regression models"""

    def __init__(self, model_type='linear'):
        super().__init__(model_type=model_type)
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'ridge':
            self.model = Ridge(alpha=1.0)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def train(self, X_train, y_train):
        """Train ML model"""
        try:
            logger.info(f"Training {self.model_type} regression model")
            self.model.fit(X_train, y_train)
            self.is_fitted = True
            logger.info("ML model training completed")
            return self.model
        except Exception as e:
            logger.error(f"Error training ML model: {str(e)}")
            raise

    def predict(self, X):
        """Make predictions"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before prediction")

        predictions = self.model.predict(X)
        return predictions


class EnsemblePredictor:
    """Ensemble of multiple models for better predictions"""

    def __init__(self):
        self.models = {}
        self.weights = {}

    def add_model(self, name, model, weight=1.0):
        """Add a model to the ensemble"""
        self.models[name] = model
        self.weights[name] = weight

    def predict(self, *args, **kwargs):
        """Make ensemble predictions"""
        predictions = []
        total_weight = sum(self.weights.values())

        for name, model in self.models.items():
            pred = model.predict(*args, **kwargs)
            weight = self.weights[name] / total_weight
            predictions.append(pred * weight)

        ensemble_prediction = np.sum(predictions, axis=0)
        return ensemble_prediction

    def get_individual_predictions(self, *args, **kwargs):
        """Get predictions from all individual models"""
        results = {}
        for name, model in self.models.items():
            results[name] = model.predict(*args, **kwargs)
        return results
