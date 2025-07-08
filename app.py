from datetime import date, timedelta
from dash import Dash, html, Input, Output, callback, dcc, dash_table
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

from config import AppConfig
from components import DividendComponents
import get_historical_data_by_ticker
import get_dividends
import get_dividends_historical_by_ticker
import calculate_dividend_summary

class DividendAnalysisApp:
    """Main application class for Dividend Analysis"""
    
    def __init__(self, config_path: str = './conf/general.conf'):
        self.config = AppConfig.from_file(config_path)
        self.components = DividendComponents(self.config)
        self.app = self._create_dash_app()
        self._setup_callbacks()
    
    def _create_dash_app(self) -> Dash:
        """Create and configure the Dash app"""
        app = Dash(__name__)
        app.layout = self._create_layout()
        return app
    
    def _create_layout(self) -> html.Div:
        """Create the app layout"""
        return html.Div([
            self.components.create_header(),
            self.components.create_footer(),
            html.Div([html.Div(id='dividends_grid', children=[])]),
            html.Div([dag.AgGrid(id="dividends_general_grid")], style={'display': 'none'}),
            html.Div([
                html.Footer(
                    "Info taken from investing.com", 
                    className="plotly-footnote",
                    style={
                        'text-align': 'left', 
                        'font-family': self.config.font_figure,
                        'margin-top': '5px', 
                        'fontSize': self.config.footer_size, 
                        'color': self.config.light_gray,
                        'margin-right': '10px'
                    }
                )
            ]),
            html.Div([html.Div(id='stocks', children=[])]),
            html.Div([html.Div(id='dividends_hist', children=[])]),
            html.Div(
                id="title-dividend_Payout",
                style={
                    'textAlign': 'center', 
                    'font-family': self.config.font_figure, 
                    'color': self.config.dark_gray
                }
            ),
            html.Div(
                style={
                    'color': 'black', 
                    "display": "flex", 
                    "justify-content": "center", 
                    "align-items": "center",
                    'padding': '15px', 
                    "height": "8vh", 
                    'font': self.config.font_figure
                }, 
                id='dividends_summary', 
                children=[]
            ),
            html.Div(
                style={
                    'display': 'flex', 
                    "textAlign": "center", 
                    'marginLeft': 'auto', 
                    'marginRight': 'auto',
                    'justifyContent': 'center', 
                    'alignItems': 'center', 
                    'font': self.config.font_figure
                }, 
                id="dividends_full"
            ),
            dcc.Store(id='store-data', data=[], storage_type='memory')
        ])
    
    def _setup_callbacks(self):
        """Setup all Dash callbacks"""
        self._setup_dividends_grid_callback()
        self._setup_store_data_callback()
        self._setup_historical_dividends_callback()
        self._setup_dividend_table_callback()
        self._setup_dividend_summary_callback()
        self._setup_dividend_title_callback()
        self._setup_stocks_callback()
    
    def _setup_dividends_grid_callback(self):
        @self.app.callback(
            Output('dividends_grid', 'children'),
            Input('dropdown_range', 'value')
        )
        def update_output(value):
            if value is not None:
                df = get_dividends.get_dividends_next_week(
                    country=self.config.country, 
                    filter_time=value
                )
                return self.components.create_dividends_grid(df.to_dict("records"))
            return []
    
    def _setup_store_data_callback(self):
        @self.app.callback(
            Output('store-data', 'data'),
            Input('dividends_general_grid', 'selectedRows')
        )
        def store_data(row):
            if row is not None:
                cell = row[0]['Company (Ticker)']
                ticker = cell[cell.find("(") + 1:cell.find(")")]
                dg = get_dividends_historical_by_ticker.get_historical_dividends(
                    ticker=ticker, 
                    time_delta=self.config.dividends_days
                )
                dg["date"] = pd.to_datetime(dg["date"])
                dg["YEAR"] = dg["date"].dt.year
                dg["date"] = dg["date"].dt.date
                dg.sort_values(by='date', ascending=False, inplace=True)
                dg['YEAR'] = dg['YEAR'].where(dg['YEAR'] != dg['YEAR'].shift(), '')
                return dg.to_dict('records')
            return []
    
    def _setup_historical_dividends_callback(self):
        @self.app.callback(
            Output("dividends_hist", "children"),
            Input("store-data", "data")
        )
        def display_historical_dividends_figure(data):
            if data is not None and len(data) > 0:
                dff = pd.DataFrame(data)
                # Check if required columns exist
                if 'date' in dff.columns and 'dividend' in dff.columns and len(dff) > 0:
                    fig_historical_dividends = px.line(dff, x='date', y='dividend', markers=True)
                    fig_historical_dividends.update_layout(
                        title=dict(
                            text=f"<b>Historical Dividends Information for [{dff['ticker'][0]}]</b>",
                            font=dict(
                                family=self.config.font_figure, 
                                size=self.config.font_size_title, 
                                color=self.config.dark_gray
                            ),
                            y=0.9,
                            x=0.5,
                            xanchor='center',
                            yanchor='top'
                        ),
                        yaxis_title='<b>Dividends US$</b>',
                        xaxis_title=""
                    )
                    fig_historical_dividends.add_annotation(
                        text='Info taken from yahoo_fin', 
                        xref='x domain',
                        showarrow=False,
                        font=dict(
                            family=self.config.font_figure, 
                            size=self.config.footer_size, 
                            color=self.config.light_gray
                        ),
                        yref='y domain', 
                        y=-0.12
                    )
                    return dcc.Graph(figure=fig_historical_dividends)
                else:
                    return html.Div("No dividend data available for this ticker", 
                                  style={'textAlign': 'center', 'color': 'red'})
            return []
    
    def _setup_dividend_table_callback(self):
        @self.app.callback(
            Output("dividends_full", "children"),
            Input("store-data", "data")
        )
        def display_dividend_table(data):
            if data is not None and len(data) > 0:
                try:
                    dff = pd.DataFrame(data)
                    # Check if required columns exist
                    if 'YEAR' in dff.columns and 'dividend' in dff.columns and 'date' in dff.columns:
                        columns = [{"name": i, "id": i} for i in dff[['YEAR', 'dividend', 'date']]]
                        styles = self.config.get_style_config()
                        return dash_table.DataTable(
                            data=dff.to_dict('records'), 
                            columns=columns, 
                            fill_width=False,
                            style_header=styles['style_header'],
                            style_cell=styles['style_cell'],
                            style_data_conditional=styles['style_data_conditional'],
                            style_data={'color': self.config.dark_gray},
                            style_table=styles['style_table']
                        )
                    else:
                        return html.Div("No dividend table data available", 
                                      style={'textAlign': 'center', 'color': 'red'})
                except Exception as e:
                    return html.Div(f"Error displaying dividend table: {str(e)}", 
                                  style={'textAlign': 'center', 'color': 'red'})
            return []
    
    def _setup_dividend_summary_callback(self):
        @self.app.callback(
            Output("dividends_summary", "children"),
            Input("store-data", "data")
        )
        def display_dividend_summary(data):
            if data is not None and len(data) > 0:
                try:
                    dg = calculate_dividend_summary.get_dividend_summary(
                        data=data, 
                        time_delta=self.config.dividends_days
                    )
                    if dg is not None and not dg.empty:
                        columns = [{"name": i, "id": i} for i in dg.columns]
                        dg_data = dg.to_dict('records')
                        return dash_table.DataTable(
                            data=dg_data, 
                            columns=columns, 
                            fill_width=False, 
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'text-align': 'center', 
                                "font-family": self.config.font_figure,
                                'backgroundColor': '#cccccc'  # Fixed color value
                            },
                            style_data={
                                'backgroundColor': '#E8E8E8', 
                                'color': self.config.dark_gray
                            },
                            style_header={
                                "backgroundColor": self.config.main_color, 
                                "color": "#FFFFFF", 
                                "padding": "0px",
                                "border": "0"
                            }
                        )
                    else:
                        return html.Div("No dividend summary available", 
                                      style={'textAlign': 'center', 'color': 'red'})
                except Exception as e:
                    return html.Div(f"Error calculating dividend summary: {str(e)}", 
                                  style={'textAlign': 'center', 'color': 'red'})
            return []
    
    def _setup_dividend_title_callback(self):
        @self.app.callback(
            Output("title-dividend_Payout", "children"),
            Input("dividends_general_grid", "selectedRows")
        )
        def display_dividend_payout_title(row):
            if row is not None:
                cell = row[0]['Company (Ticker)']
                ticker = cell[cell.find("(") + 1:cell.find(")")]
                return html.Div([
                    html.H2(
                        f"Dividend Payout History for [{ticker}]", 
                        className="plotly-title", 
                        style={'padding': '0px'}
                    ),
                    html.P(
                        'Info taken from yahoo_fin', 
                        className="plotly-footnote",
                        style={
                            'font-family': self.config.font_figure, 
                            'padding': '0px',
                            'margin-top': '0px', 
                            'fontSize': self.config.footer_size, 
                            'color': self.config.light_gray
                        }
                    )
                ])
            return []
    
    def _setup_stocks_callback(self):
        @self.app.callback(
            Output("stocks", "children"),
            Input("dividends_general_grid", "selectedRows")
        )
        def display_stocks_figure(row):
            if row is not None:
                cell = row[0]['Company (Ticker)']
                ticker = cell[cell.find("(") + 1:cell.find(")")]
                df = get_historical_data_by_ticker.get_historical_data(
                    ticker=ticker, 
                    start_date=self.config.start_date,
                    end_date=self.config.end_date, 
                    days_delta=int(self.config.historical_data_days)
                )
                fig_historical_data = px.line(df, x='date', y='close')
                fig_historical_data.update_layout(
                    title=dict(
                        text=f"<b>Stock Price (5 Years) for [{ticker}]</b>",
                        font=dict(
                            family=self.config.font_figure, 
                            size=self.config.font_size_title, 
                            color=self.config.dark_gray
                        ),
                        y=0.9,
                        x=0.5,
                        xanchor='center',
                        yanchor='top'
                    ),
                    yaxis_title='<b>Stock Price US$</b>',
                    xaxis_title=""
                )
                fig_historical_data.add_annotation(
                    text='Info taken from yahoo_fin', 
                    xref='x domain', 
                    showarrow=False,
                    font=dict(
                        family=self.config.font_figure, 
                        size=self.config.footer_size, 
                        color=self.config.light_gray
                    ), 
                    yref='y domain', 
                    y=-0.12
                )
                return dcc.Graph(figure=fig_historical_data)
            return []
    
    def run(self, debug: bool = True, host: str = '127.0.0.1', port: str = '8050'):
        """Run the application"""
        self.app.run(debug=debug, host=host, port=port)

# Main execution
if __name__ == '__main__':
    app = DividendAnalysisApp()
    app.run(debug=True)
