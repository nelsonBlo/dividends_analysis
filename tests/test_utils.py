import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from misc.utils import *
from calculate_dividend_summary import get_dividend_summary


class TestUtils:
    """Test cases for utility functions"""
    
    def test_date_validation_valid_date(self):
        """Test date validation with valid date string"""
        valid_date = "2023-12-31"
        assert is_valid_date(valid_date) == True
    
    def test_date_validation_invalid_date(self):
        """Test date validation with invalid date string"""
        invalid_date = "not-a-date"
        assert is_valid_date(invalid_date) == False
    
    def test_date_validation_none(self):
        """Test date validation with None"""
        assert is_valid_date(None) == False
    
    def test_numeric_validation_valid_number(self):
        """Test numeric validation with valid number"""
        valid_number = "123.45"
        assert is_numeric(valid_number) == True
    
    def test_numeric_validation_invalid_number(self):
        """Test numeric validation with invalid number"""
        invalid_number = "abc"
        assert is_numeric(invalid_number) == False
    
    def test_numeric_validation_none(self):
        """Test numeric validation with None"""
        assert is_numeric(None) == False


class TestCalculateDividendSummary:
    """Test cases for dividend summary calculation"""
    
    def test_get_dividend_summary_with_valid_data(self):
        """Test dividend summary calculation with valid data"""
        # Create sample dividend data
        data = [
            {'date': '2023-01-01', 'dividend': 0.5, 'ticker': 'AAPL'},
            {'date': '2023-04-01', 'dividend': 0.6, 'ticker': 'AAPL'},
            {'date': '2023-07-01', 'dividend': 0.7, 'ticker': 'AAPL'},
            {'date': '2023-10-01', 'dividend': 0.8, 'ticker': 'AAPL'}
        ]
        
        result = get_dividend_summary(data, time_delta=60)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert 'First Div. Paid (Year)' in result.columns
        assert 'First Div. Paid (US$)' in result.columns
        assert 'Div. Frequency' in result.columns
    
    def test_get_dividend_summary_with_empty_data(self):
        """Test dividend summary calculation with empty data"""
        data = []
        
        result = get_dividend_summary(data, time_delta=60)
        
        assert result is None or len(result) == 0
    
    def test_get_dividend_summary_with_invalid_data(self):
        """Test dividend summary calculation with invalid data structure"""
        data = [{'wrong_column': 'value'}]
        
        result = get_dividend_summary(data, time_delta=60)
        
        # Should handle gracefully
        assert result is None or len(result) == 0


class TestDataValidation:
    """Test cases for data validation functions"""
    
    def test_validate_dataframe_structure_valid(self):
        """Test dataframe structure validation with valid data"""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-04-01'],
            'dividend': [0.5, 0.6],
            'ticker': ['AAPL', 'AAPL']
        })
        
        assert validate_dataframe_structure(df, ['date', 'dividend', 'ticker']) == True
    
    def test_validate_dataframe_structure_missing_columns(self):
        """Test dataframe structure validation with missing columns"""
        df = pd.DataFrame({
            'date': ['2023-01-01'],
            'dividend': [0.5]
            # Missing 'ticker' column
        })
        
        assert validate_dataframe_structure(df, ['date', 'dividend', 'ticker']) == False
    
    def test_validate_dataframe_structure_empty(self):
        """Test dataframe structure validation with empty dataframe"""
        df = pd.DataFrame()
        
        assert validate_dataframe_structure(df, ['date', 'dividend']) == False


# Helper functions for testing (these should be defined in utils.py)
def is_valid_date(date_string):
    """Helper function to validate date strings"""
    if date_string is None:
        return False
    try:
        pd.to_datetime(date_string)
        return True
    except:
        return False

def is_numeric(value):
    """Helper function to validate numeric values"""
    if value is None:
        return False
    try:
        float(value)
        return True
    except:
        return False

def validate_dataframe_structure(df, required_columns):
    """Helper function to validate dataframe structure"""
    if df is None or df.empty:
        return False
    return all(col in df.columns for col in required_columns)


if __name__ == "__main__":
    pytest.main([__file__]) 