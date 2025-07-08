# Nuevo archivo: config.py
import configparser
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import date, timedelta

@dataclass
class AppConfig:
    """Configuration class for the Dividend Analysis App"""
    
    # Investing.com settings
    country: int = 5
    filter_time: str = 'nextWeek'
    url: str = 'https://www.investing.com'
    endpoint: str = '/dividends-calendar/Service/getCalendarFilteredData'
    
    # Figure settings
    font_figure: str = 'Verdana'
    font_size_title: int = 20
    
    # Font sizes
    title_size: int = 15
    footer_size: int = 11
    
    # Colors
    font_color: str = '#000000'
    main_color: str = '#636EFA'
    dark_gray: str = '#3f3f3f'
    light_gray: str = '#9f9f9f'
    
    # Time deltas
    historical_data_days: float = 1.0
    dividends_days: int = 60
    
    # Date ranges
    start_date: str = ""
    end_date: str = ""
    
    @classmethod
    def from_file(cls, config_path: str = './conf/general.conf') -> 'AppConfig':
        """Load configuration from file"""
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
            
            # Calculate dates
            end_date = date.today()
            start_date = end_date - timedelta(days=1825)  # 5 years
            
            return cls(
                country=config.getint('INVESTING', 'COUNTRY'),
                filter_time=config.get('INVESTING', 'FILTER'),
                url=config.get('INVESTING', 'URL'),
                endpoint=config.get('INVESTING', 'ENDPOINT'),
                font_figure=config.get('FIGURE', 'FONT_FIGURE'),
                font_size_title=config.getint('FIGURE', 'FONT_SIZE_TITLE_FIGURE'),
                title_size=config.getint('FONT_SIZE', 'TITLE_SIZE'),
                footer_size=config.getint('FONT_SIZE', 'FOOTER_SIZE'),
                font_color=config.get('COLOR', 'FONT_COLOR'),
                main_color=config.get('COLOR', 'MAIN_COLOR'),
                dark_gray=config.get('COLOR', 'DARK_GRAY'),
                light_gray=config.get('COLOR', 'LIGHT_GRAY'),
                historical_data_days=config.getfloat('TIME_DELTA_DAYS', 'HISTORICAL_DATA'),
                dividends_days=config.getint('TIME_DELTA_DAYS', 'DIVIDENDS'),
                start_date=start_date.strftime('%m/%d/%Y'),
                end_date=end_date.strftime('%m/%d/%Y')
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except configparser.Error as e:
            raise ValueError(f"Error parsing configuration file: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error loading configuration: {e}")
    
    def get_style_config(self) -> Dict[str, Any]:
        """Get style configuration for Dash components"""
        return {
            'style_header': {
                "backgroundColor": self.main_color,
                "color": "#FFFFFF",
                "padding": "10px",
                "border": "0",
            },
            'style_cell': {
                "backgroundColor": "#FFFFFF",
                "color": "#000000",
                "fontSize": 16,
                "font-family": self.font_figure,
                "padding": "10px",
                "border": "thin solid #FFFFFF",
                'width': 120
            },
            'style_data_conditional': [
                {"if": {"row_index": "odd"}, "backgroundColor": "#E8E8E8"}
            ],
            'style_table': {"borderRadius": "15px", "overflow": "hidden"}
        }
