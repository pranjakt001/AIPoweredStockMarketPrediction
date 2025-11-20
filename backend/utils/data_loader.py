import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

class StockDataLoader:
    """Loads and preprocesses stock market data"""

    def __init__(self, ticker='^AXJO', start_date='2018-01-01', end_date=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.data = None

    def fetch_data(self):
        """Fetch stock data from Yahoo Finance"""
        try:
            logger.info(f"Fetching data for {self.ticker} from {self.start_date} to {self.end_date}")
            stock = yf.Ticker(self.ticker)
            df = stock.history(start=self.start_date, end=self.end_date)

            if df.empty:
                raise ValueError(f"No data found for ticker {self.ticker}")

            # Flatten MultiIndex columns if present
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]

            # Reset index to make Date a column
            df.reset_index(inplace=True)

            self.data = df
            logger.info(f"Successfully fetched {len(df)} rows of data")
            return df

        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise

    def calculate_returns(self, df=None):
        """Calculate daily returns"""
        if df is None:
            df = self.data

        df['Daily_Return'] = df['Close'].pct_change()
        return df

    def add_moving_averages(self, df=None, periods=[5, 10, 20, 50, 100, 200]):
        """Add Simple Moving Averages"""
        if df is None:
            df = self.data

        for period in periods:
            df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
            df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()

        return df

    def add_technical_indicators(self, df=None):
        """Add comprehensive technical indicators"""
        if df is None:
            df = self.data

        # RSI (Relative Strength Index)
        df = self._calculate_rsi(df, period=14)

        # MACD
        df = self._calculate_macd(df)

        # Bollinger Bands
        df = self._calculate_bollinger_bands(df)

        # ATR (Average True Range)
        df = self._calculate_atr(df)

        # Stochastic Oscillator
        df = self._calculate_stochastic(df)

        # On-Balance Volume
        df = self._calculate_obv(df)

        return df

    def _calculate_rsi(self, df, period=14):
        """Calculate RSI"""
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    def _calculate_macd(self, df, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        df['MACD'] = df['Close'].ewm(span=fast).mean() - df['Close'].ewm(span=slow).mean()
        df['MACD_Signal'] = df['MACD'].ewm(span=signal).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        return df

    def _calculate_bollinger_bands(self, df, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        df['BB_Middle'] = df['Close'].rolling(window=period).mean()
        bb_std = df['Close'].rolling(window=period).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * std_dev)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * std_dev)
        df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
        return df

    def _calculate_atr(self, df, period=14):
        """Calculate Average True Range"""
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(window=period).mean()
        return df

    def _calculate_stochastic(self, df, period=14):
        """Calculate Stochastic Oscillator"""
        low_min = df['Low'].rolling(window=period).min()
        high_max = df['High'].rolling(window=period).max()
        df['Stochastic_%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        df['Stochastic_%D'] = df['Stochastic_%K'].rolling(window=3).mean()
        return df

    def _calculate_obv(self, df):
        """Calculate On-Balance Volume"""
        obv = [0]
        for i in range(1, len(df)):
            if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
                obv.append(obv[-1] + df['Volume'].iloc[i])
            elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
                obv.append(obv[-1] - df['Volume'].iloc[i])
            else:
                obv.append(obv[-1])
        df['OBV'] = obv
        return df

    def prepare_features(self):
        """Prepare complete feature set"""
        if self.data is None:
            self.fetch_data()

        df = self.data.copy()
        df = self.calculate_returns(df)
        df = self.add_moving_averages(df)
        df = self.add_technical_indicators(df)

        # Add lagged features
        for lag in [1, 2, 3, 5, 10]:
            df[f'Close_Lag_{lag}'] = df['Close'].shift(lag)
            df[f'Return_Lag_{lag}'] = df['Daily_Return'].shift(lag)
            df[f'Volume_Lag_{lag}'] = df['Volume'].shift(lag)

        # Add target variable (next day's close)
        df['Target_Next_Close'] = df['Close'].shift(-1)
        df['Target_Direction'] = (df['Target_Next_Close'] > df['Close']).astype(int)

        # Drop NaN values
        df.dropna(inplace=True)

        self.data = df
        return df

    def get_latest_data(self, days=30):
        """Get latest n days of data for predictions"""
        if self.data is None:
            self.prepare_features()

        return self.data.tail(days)

    def save_data(self, filepath):
        """Save processed data to CSV"""
        if self.data is None:
            raise ValueError("No data to save. Run prepare_features() first.")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.data.to_csv(filepath, index=False)
        logger.info(f"Data saved to {filepath}")

    def load_data(self, filepath):
        """Load data from CSV"""
        self.data = pd.read_csv(filepath)
        if 'Date' in self.data.columns:
            self.data['Date'] = pd.to_datetime(self.data['Date'])
        logger.info(f"Data loaded from {filepath}")
        return self.data
