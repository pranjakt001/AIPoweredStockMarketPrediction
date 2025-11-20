from flask import Blueprint, jsonify, request
from backend.services.prediction_service import PredictionService
import logging

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Global prediction service instance
prediction_service = PredictionService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Stock Market Prediction API',
        'version': '1.0.0'
    })

@api_bp.route('/initialize', methods=['POST'])
def initialize():
    """Initialize the prediction service"""
    try:
        data = request.get_json() or {}
        ticker = data.get('ticker', '^AXJO')
        start_date = data.get('start_date', '2018-01-01')

        prediction_service.initialize(ticker=ticker, start_date=start_date)

        return jsonify({
            'status': 'success',
            'message': 'Prediction service initialized',
            'ticker': ticker
        })
    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/train', methods=['POST'])
def train_models():
    """Train prediction models"""
    try:
        data = request.get_json() or {}
        train_ratio = data.get('train_ratio', 0.8)

        result = prediction_service.train_models(train_ratio=train_ratio)

        return jsonify({
            'status': 'success',
            'message': 'Models trained successfully',
            'details': result
        })
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/predict', methods=['GET'])
def predict():
    """Get stock price predictions"""
    try:
        days = request.args.get('days', default=5, type=int)

        if days < 1 or days > 30:
            return jsonify({
                'status': 'error',
                'message': 'Days must be between 1 and 30'
            }), 400

        predictions = prediction_service.predict_next_days(days=days)

        return jsonify({
            'status': 'success',
            'predictions': predictions
        })
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/current', methods=['GET'])
def get_current():
    """Get current stock price"""
    try:
        current_price = prediction_service.get_current_price()

        if current_price is None:
            return jsonify({
                'status': 'error',
                'message': 'No data available. Initialize the service first.'
            }), 404

        return jsonify({
            'status': 'success',
            'data': current_price
        })
    except Exception as e:
        logger.error(f"Error getting current price: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/historical', methods=['GET'])
def get_historical():
    """Get historical stock data"""
    try:
        days = request.args.get('days', default=30, type=int)

        if days < 1 or days > 365:
            return jsonify({
                'status': 'error',
                'message': 'Days must be between 1 and 365'
            }), 400

        historical_data = prediction_service.get_historical_data(days=days)

        if historical_data is None:
            return jsonify({
                'status': 'error',
                'message': 'No data available. Initialize the service first.'
            }), 404

        return jsonify({
            'status': 'success',
            'data': historical_data
        })
    except Exception as e:
        logger.error(f"Error getting historical data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/indicators', methods=['GET'])
def get_indicators():
    """Get technical indicators"""
    try:
        indicators = prediction_service.get_technical_indicators()

        if indicators is None:
            return jsonify({
                'status': 'error',
                'message': 'No data available. Initialize the service first.'
            }), 404

        return jsonify({
            'status': 'success',
            'indicators': indicators
        })
    except Exception as e:
        logger.error(f"Error getting indicators: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/models', methods=['GET'])
def get_models():
    """Get model performance"""
    try:
        performance = prediction_service.get_model_performance()

        return jsonify({
            'status': 'success',
            'models': performance
        })
    except Exception as e:
        logger.error(f"Error getting model performance: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/refresh', methods=['POST'])
def refresh_data():
    """Refresh stock data"""
    try:
        prediction_service.refresh_data()

        return jsonify({
            'status': 'success',
            'message': 'Data refreshed successfully'
        })
    except Exception as e:
        logger.error(f"Error refreshing data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
