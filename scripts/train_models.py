#!/usr/bin/env python3
"""
Model Training Script
Trains all prediction models and saves them to disk
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.prediction_service import PredictionService
from backend.config.config import Config
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def train_all_models():
    """Train all prediction models"""
    try:
        logger.info("Starting model training...")

        # Initialize service
        service = PredictionService()
        service.initialize(
            ticker=Config.DEFAULT_TICKER,
            start_date=Config.START_DATE
        )

        # Train models
        logger.info("Training models...")
        result = service.train_models(train_ratio=Config.TRAIN_TEST_SPLIT)

        logger.info("Training completed successfully!")
        logger.info(f"Models trained: {result['models_trained']}")
        logger.info(f"Training samples: {result['train_samples']}")
        logger.info(f"Test samples: {result['test_samples']}")

        # Save models
        logger.info("Saving models...")
        for model_name, model in service.models.items():
            model_path = os.path.join(
                Config.MODELS_DIR,
                f'{model_name}_model_{datetime.now().strftime("%Y%m%d")}.pkl'
            )
            try:
                model.save_model(model_path)
                logger.info(f"Saved {model_name} model to {model_path}")
            except Exception as e:
                logger.warning(f"Could not save {model_name} model: {str(e)}")

        return True

    except Exception as e:
        logger.error(f"Error training models: {str(e)}")
        return False

if __name__ == '__main__':
    success = train_all_models()
    sys.exit(0 if success else 1)
