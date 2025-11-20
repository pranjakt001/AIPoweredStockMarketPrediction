import os
from datetime import datetime

class Config:
    """Application configuration"""

    # Base directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    MODELS_DIR = os.path.join(DATA_DIR, 'models')

    # API Configuration
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # Stock market configuration
    DEFAULT_TICKER = '^AXJO'  # ASX200 Index
    START_DATE = '2018-01-01'
    END_DATE = datetime.now().strftime('%Y-%m-%d')

    # Model configuration
    TRAIN_TEST_SPLIT = 0.8
    RANDOM_STATE = 42

    # Feature engineering parameters
    SMA_PERIODS = [5, 10, 20, 50, 100, 200]
    EMA_PERIODS = [5, 10, 20, 50, 100, 200]
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    ATR_PERIOD = 14
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2

    # ARIMA/SARIMA parameters
    ARIMA_ORDER = (1, 1, 1)
    SARIMA_SEASONAL_ORDER = (1, 1, 1, 20)  # Monthly seasonality

    # API rate limiting
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per hour')

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Cache settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
