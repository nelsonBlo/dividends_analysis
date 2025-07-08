# Nuevo archivo: components.py
from dash import html, dcc, dash_table
import dash_ag_grid as dag
from typing import List, Dict, Any

class DividendComponents:
    """Component factory for Dividend Analysis App"""
    
    def __init__(self, config):
        self.config = config
        self.styles = config.get_style_config()
    
    def get_column_definitions(self) -> List[Dict[str, Any]]:
        """Get column definitions for the dividends grid"""
        return [
            {"field": "Date"},
            {"field": "Company (Ticker)", "resizable": True},
            {
                "field": "Ex-Dividend Date",
                "filter": "agDateColumnFilter",
                "valueGetter": {"function": "d3.timeParse('%b/%d/%Y')(params.data.Ex-Dividend Date)"},
                "valueFormatter": {"function": "params.data.date"},
            },
            {"field": "Dividend"},
            {"field": "Payment Date"},
            {"field": "Yield"}
        ]
    
    def create_header(self) -> html.Div:
        """Create the app header with dropdown"""
        return html.Div([
            html.H2("Dividends Calendar for ", 
                   className="plotly-title",
                   style={
                       'margin': '0', 
                       'marginRight': '5px', 
                       'margin-top': '10px', 
                       'padding': '10px',
                       'font-family': self.config.font_figure, 
                       "color": self.config.main_color
                   }),
            dcc.Dropdown(
                id='dropdown_range',
                options=[
                    {'label': 'Next Week', 'value': 'nextWeek'},
                    {'label': 'This Week', 'value': 'thisWeek'},
                    {'label': 'Tomorrow', 'value': 'tomorrow'}
                ],
                placeholder="Select an option",
                style={
                    'width': '200px', 
                    'font-family': self.config.font_figure, 
                    "color": self.config.dark_gray, 
                    'margin-top': '5px'
                },
                className='my-dropdown',
                persistence=True
            )
        ], style={'display': 'flex', 'align-items': 'center'})
    
    def create_footer(self) -> html.Div:
        """Create the app footer"""
        return html.Div([
            html.Footer(
                "For reference purposes only - Developed by Nelson Bocanegra L.",
                className="plotly-footnote",
                style={
                    'font-family': self.config.font_figure, 
                    'fontSize': self.config.footer_size, 
                    'text-align': 'right', 
                    'margin-top': '0px',
                    'margin-right': '0px', 
                    'padding': 2
                }
            ),
            html.Div(style={'clear': 'both'})
        ])
    
    def create_dividends_grid(self, df_data: List[Dict]) -> dag.AgGrid:
        """Create the dividends grid component"""
        return dag.AgGrid(
            id="dividends_general_grid",
            rowData=df_data,
            className="ag-theme-alpine",
            columnDefs=self.get_column_definitions(),
            defaultColDef={"filter": True, "sortable": True},
            columnSize="sizeToFit",
            dashGridOptions={"rowSelection": "single"},
            columnSizeOptions={
                'defaultMinWidth': 90,
                'columnLimits': [
                    {'key': 'Date', 'minWidth': 250},
                    {'key': 'Company (Ticker)', 'minWidth': 500}
                ]
            }
        )
