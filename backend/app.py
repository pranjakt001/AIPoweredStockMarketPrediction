from flask import Flask
from flask_cors import CORS
import logging
import os
from backend.api.routes import api_bp
from backend.config.config import config

def create_app(config_name='development'):
    """Application factory pattern"""

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Setup logging
    setup_logging(app)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'AI Powered Stock Market Prediction API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'initialize': 'POST /api/initialize',
                'train': 'POST /api/train',
                'predict': 'GET /api/predict?days=5',
                'current': 'GET /api/current',
                'historical': 'GET /api/historical?days=30',
                'indicators': 'GET /api/indicators',
                'models': 'GET /api/models',
                'refresh': 'POST /api/refresh'
            }
        }

    return app

def setup_logging(app):
    """Configure application logging"""
    log_level = app.config.get('LOG_LEVEL', 'INFO')

    # Create logs directory if it doesn't exist
    log_file = app.config.get('LOG_FILE')
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )

    app.logger.setLevel(getattr(logging, log_level))
    app.logger.info(f"Logging configured with level: {log_level}")

if __name__ == '__main__':
    # Create app
    app = create_app(os.getenv('FLASK_ENV', 'development'))

    # Run app
    host = app.config['API_HOST']
    port = app.config['API_PORT']
    debug = app.config['DEBUG']

    print(f"Starting Stock Market Prediction API on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
