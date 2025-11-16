#!/usr/bin/env python3
"""
Data Update Script
Fetches latest stock market data and updates the database
Can be run as a cron job for automated updates
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.data_loader import StockDataLoader
from backend.config.config import Config
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_stock_data():
    """Update stock market data"""
    try:
        logger.info("Starting data update...")

        # Initialize data loader
        loader = StockDataLoader(
            ticker=Config.DEFAULT_TICKER,
            start_date=Config.START_DATE
        )

        # Fetch and prepare data
        logger.info("Fetching data from Yahoo Finance...")
        loader.prepare_features()

        # Save to processed directory
        output_path = os.path.join(
            Config.PROCESSED_DATA_DIR,
            f'asx200_data_{datetime.now().strftime("%Y%m%d")}.csv'
        )

        loader.save_data(output_path)

        logger.info(f"Data updated successfully! Saved to {output_path}")
        logger.info(f"Total records: {len(loader.data)}")

        return True

    except Exception as e:
        logger.error(f"Error updating data: {str(e)}")
        return False

if __name__ == '__main__':
    success = update_stock_data()
    sys.exit(0 if success else 1)
