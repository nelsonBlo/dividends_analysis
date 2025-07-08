import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_requests.historical_dividends_by_ticker_yahoo_fin import get_historical_dividends, get_historical_dividends_get
from api_requests.dividends_by_date_investing import get_dividends_next_week_post


class TestHistoricalDividends:
    """Test cases for historical dividends functions"""
    
    def test_get_historical_dividends_get_with_valid_ticker(self):
        """Test get_historical_dividends_get with a valid ticker"""
        with patch('api_requests.historical_dividends_by_ticker_yahoo_fin.yf') as mock_yf:
            # Mock the Ticker object
            mock_ticker = MagicMock()
            mock_dividends = pd.Series([0.5, 0.6, 0.7], 
                                     index=pd.to_datetime(['2023-01-01', '2023-04-01', '2023-07-01']))
            mock_ticker.dividends = mock_dividends
            mock_yf.Ticker.return_value = mock_ticker
            
            result = get_historical_dividends_get('AAPL')
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 3
            assert 'date' in result.columns
            assert 'dividend' in result.columns
            assert 'ticker' in result.columns
            assert result['ticker'].iloc[0] == 'AAPL'
    
    def test_get_historical_dividends_get_with_no_dividends(self):
        """Test get_historical_dividends_get when ticker has no dividends"""
        with patch('api_requests.historical_dividends_by_ticker_yahoo_fin.yf') as mock_yf:
            # Mock the Ticker object with empty dividends
            mock_ticker = MagicMock()
            mock_ticker.dividends = pd.Series(dtype=float)
            mock_yf.Ticker.return_value = mock_ticker
            
            result = get_historical_dividends_get('INVALID')
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0
            assert 'date' in result.columns
            assert 'dividend' in result.columns
            assert 'ticker' in result.columns
    
    def test_get_historical_dividends_wrapper(self):
        """Test the wrapper function get_historical_dividends"""
        with patch('api_requests.historical_dividends_by_ticker_yahoo_fin.get_historical_dividends_get') as mock_get:
            mock_get.return_value = pd.DataFrame({'date': [], 'dividend': [], 'ticker': []})
            
            result = get_historical_dividends('AAPL', 60)
            
            mock_get.assert_called_once_with('AAPL')
            assert isinstance(result, pd.DataFrame)


class TestDividendsByDateInvesting:
    """Test cases for Investing.com API functions"""
    
    def test_get_dividends_next_week_post_success(self):
        """Test successful API call to Investing.com"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"ticker": "AAPL", "company": "Apple Inc.", "dividend_date": "2023-07-15", "dividend_amount": 0.24}
            ],
            "rows_num": 1
        }
        
        with patch('api_requests.dividends_by_date_investing.requests.post', return_value=mock_response):
            result = get_dividends_next_week_post()
            
            assert isinstance(result, dict)
            assert "data" in result
            assert "rows_num" in result
            assert len(result["data"]) == 1
            assert result["data"][0]["ticker"] == "AAPL"
    
    def test_get_dividends_next_week_post_api_error(self):
        """Test API call when server returns error status"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        
        with patch('api_requests.dividends_by_date_investing.requests.post', return_value=mock_response):
            result = get_dividends_next_week_post()
            
            assert isinstance(result, dict)
            assert "data" in result
            assert result["data"] == []
    
    def test_get_dividends_next_week_post_json_error(self):
        """Test API call when response is not valid JSON"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("Invalid JSON")
        mock_response.text = "<html>Error page</html>"
        
        with patch('api_requests.dividends_by_date_investing.requests.post', return_value=mock_response):
            result = get_dividends_next_week_post()
            
            assert isinstance(result, dict)
            assert "data" in result
            assert result["data"] == []
    
    def test_get_dividends_next_week_post_request_error(self):
        """Test API call when request fails completely"""
        with patch('api_requests.dividends_by_date_investing.requests.post', side_effect=Exception("Network error")):
            result = get_dividends_next_week_post()
            
            assert isinstance(result, dict)
            assert "data" in result
            assert result["data"] == []


if __name__ == "__main__":
    pytest.main([__file__]) 