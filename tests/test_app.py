import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os
import configparser

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import DividendAnalysisApp


class TestDividendAnalysisApp:
    """Test cases for the main application"""
    
    def test_app_initialization(self):
        """Test that the app initializes correctly"""
        app = DividendAnalysisApp()
        
        assert app is not None
        assert hasattr(app, 'app')
        assert hasattr(app, 'config')
    
    def test_create_layout(self):
        """Test that the layout is created correctly"""
        app = DividendAnalysisApp()
        layout = app._create_layout()
        
        assert layout is not None
        # Check that key components are present
        assert hasattr(layout, 'children')
    
    def test_config_loading(self):
        """Test that configuration is loaded correctly"""
        app = DividendAnalysisApp()
        
        assert app.config is not None
        assert hasattr(app.config, 'font_figure')
        assert hasattr(app.config, 'main_color')
        assert hasattr(app.config, 'dividends_days')
    
    def test_config_with_invalid_path(self):
        """Test app initialization with invalid config path"""
        with pytest.raises((FileNotFoundError, ValueError)):
            DividendAnalysisApp(config_path='./nonexistent.conf')


class TestAppStructure:
    """Test cases for app structure and components"""
    
    @pytest.fixture
    def app_instance(self):
        """Create an app instance for testing"""
        return DividendAnalysisApp()
    
    def test_app_has_required_methods(self, app_instance):
        """Test that the app has all required methods"""
        assert hasattr(app_instance, '_create_dash_app')
        assert hasattr(app_instance, '_create_layout')
        assert hasattr(app_instance, '_setup_callbacks')
        assert hasattr(app_instance, 'run')
    
    def test_app_has_required_attributes(self, app_instance):
        """Test that the app has all required attributes"""
        assert hasattr(app_instance, 'app')
        assert hasattr(app_instance, 'config')
    
    def test_config_has_required_attributes(self, app_instance):
        """Test that the config has all required attributes"""
        config = app_instance.config
        required_attrs = [
            'font_figure', 'main_color', 'dark_gray', 'light_gray',
            'dividends_days', 'historical_data_days', 'start_date', 'end_date'
        ]
        
        for attr in required_attrs:
            assert hasattr(config, attr), f"Config missing attribute: {attr}"


class TestAppErrorHandling:
    """Test cases for error handling in the app"""
    
    def test_app_initialization_with_missing_config(self):
        """Test app initialization with missing config file"""
        with pytest.raises((FileNotFoundError, ValueError)):
            DividendAnalysisApp(config_path='./missing.conf')
    
    def test_app_initialization_with_invalid_config(self):
        """Test app initialization with invalid config file"""
        # Create a temporary invalid config file
        with open('./temp_invalid.conf', 'w') as f:
            f.write("Invalid config content")
        
        try:
            with pytest.raises((ValueError, configparser.Error)):
                DividendAnalysisApp(config_path='./temp_invalid.conf')
        finally:
            # Clean up
            import os
            if os.path.exists('./temp_invalid.conf'):
                os.remove('./temp_invalid.conf')


if __name__ == "__main__":
    pytest.main([__file__]) 