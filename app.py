from datetime import date, timedelta
from dash import Dash, html, Input, Output, callback, dcc, dash_table
import dash_ag_grid as dag
import pandas as pd
import get_historical_data_by_ticker
import get_dividends
import get_dividends_historical_by_ticker
import calculate_dividend_summary
import configparser
import plotly.express as px

config = configparser.ConfigParser()
config.read('./conf/general.conf')
country = config.getint('INVESTING', 'COUNTRY')
filter_time = config.get('INVESTING', 'FILTER')
font_figure = config.get('FIGURE', 'FONT_FIGURE')
font_size = config.getint('FIGURE', 'FONT_SIZE_TITLE_FIGURE')
font_color = config.get('COLOR', 'FONT_COLOR')
time_delta_stocks = config.getfloat('TIME_DELTA_DAYS', 'HISTORICAL_DATA')
time_delta_dividends = config.getint('TIME_DELTA_DAYS', 'DIVIDENDS')
main_color = config.get('COLOR', 'MAIN_COLOR')
dark_gray = config.get('COLOR', 'DARK_GRAY')
light_gray = config.get('COLOR', 'LIGHT_GRAY')
END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=1825)
START_DATE = START_DATE.strftime('%m/%d/%Y')
END_DATE = END_DATE.strftime('%m/%d/%Y')

app = Dash(__name__)
style_header = {
    "backgroundColor": main_color,
    "color": "#FFFFFF",
    "padding": "10px",
    "border": "0",
}
style_cell = {
    "backgroundColor": "#FFFFFF",
    "color": "#000000",
    "fontSize": 16,
    "font-family": font_figure,
    "padding": "10px",
    "border": "thin solid #FFFFFF",
    'width': 120
}
style_data_conditional = [
    {"if": {"row_index": "odd"}, "backgroundColor": "#E8E8E8"}
]
style_table = {"borderRadius": "15px", "overflow": "hidden"}

columnDefs = [
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

app.layout = html.Div(
    [
        html.Div([html.H2("Dividends Calendar for ",
                          style={'margin': '0', 'marginRight': '5px', 'margin-top': '10px', 'padding': '10px',
                                 'font-family': font_figure, "color": main_color}),
                  dcc.Dropdown(
                      id='dropdown_range',
                      options=[
                          {'label': 'Next Week', 'value': 'nextWeek'},
                          {'label': 'This Week', 'value': 'thisWeek'},
                          {'label': 'Tomorrow', 'value': 'tomorrow'}
                      ],
                      placeholder="Select an option",
                      style={'width': '200px', 'font-family': font_figure, "color": dark_gray, 'margin-top': '5px'},
                      className='my-dropdown',
                      persistence=True
                  )
                  ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            html.Footer("For reference purposes only - Developed by Nelson Bocanegra L.",
                        style={'font-family': font_figure, 'fontSize': 8, 'text-align': 'right', 'margin-top': '0px',
                               'margin-right': '0px', 'padding': 2}),
            html.Div(style={'clear': 'both'})]),
        html.Div([html.Div(id='dividends_grid', children=[]), ]),
        html.Div([dag.AgGrid(id="dividends_general_grid")], style={'display': 'none'}),
        html.Div([
            html.Footer("Info taken from investing.com", style={'text-align': 'left', 'font-family': font_figure,
                                                                'margin-top': '5px', 'fontSize': 8, 'color': light_gray,
                                                                'margin-right': '10px'})]),
        html.Div([html.Div(id='stocks', children=[]), ]),
        html.Div([html.Div(id='dividends_hist', children=[]), ]),
        html.Div(id="title-dividend_Payout",
                 style={'textAlign': 'center', 'font-family': font_figure, 'color': dark_gray}, ),
        html.Div(style={'color': 'black', "display": "flex", "justify-content": "center", "align-items": "center",
                        'padding': '15px', "height": "8vh", 'font': font_figure}, id='dividends_summary', children=[]),
        html.Div(style={"width": "15%", "textAlign": "center", 'marginLeft': 'auto', 'marginRight': 'auto',
                        'font': font_figure}, id="dividends_full"),

        dcc.Store(id='store-data', data=[], storage_type='memory')
    ]
)


@callback(
    Output('dividends_grid', 'children'),
    Input('dropdown_range', 'value')
)
def update_output(value):
    if value is not None:
        df = get_dividends.get_dividends_next_week(country=country, filter_time=value)
        return dag.AgGrid(
            id="dividends_general_grid",
            rowData=df.to_dict("records"),
            className="ag-theme-alpine",
            columnDefs=columnDefs,
            defaultColDef={"filter": True, "sortable": True},
            columnSize="sizeToFit",
            dashGridOptions={"rowSelection": "single"},
            columnSizeOptions={
                'defaultMinWidth': 90,
                'columnLimits': [{'key': 'Date', 'minWidth': 250},
                                 {'key': 'Company (Ticker)', 'minWidth': 500}]})


@callback(
    Output('store-data', 'data'),
    Input('dividends_general_grid', 'selectedRows')
)
def store_data(row):
    if row is not None:
        cell = row[0]['Company (Ticker)']
        ticker = cell[cell.find("(") + 1:cell.find(")")]
        dg = get_dividends_historical_by_ticker.get_historical_dividends(ticker=ticker, time_delta=time_delta_dividends)
        dg["date"] = pd.to_datetime(dg["date"])
        dg["YEAR"] = dg["date"].dt.year
        dg["date"] = dg["date"].dt.date
        dg.sort_values(by='date', ascending=False, inplace=True)
        dg['YEAR'] = dg['YEAR'].where(dg['YEAR'] != dg['YEAR'].shift(), '')
        return dg.to_dict('records')


@callback(
    Output("dividends_hist", "children"),
    Input("store-data", "data")
)
def display_historical_dividends_figure(data):
    if data is not None:
        dff = pd.DataFrame(data)
        fig_historical_dividends = px.line(dff, x='date', y='dividend', markers=True)
        fig_historical_dividends.update_layout(title=dict(
            text=f"<b>Historical Dividends Information for [{dff['ticker'][0]}]</b>",
            font=dict(family=font_figure, size=font_size, color=dark_gray),
            y=0.9,
            x=0.5,
            xanchor='center',
            yanchor='top'),
            yaxis_title='<b>Dividends US$</b>',
            xaxis_title=""
        )
        fig_historical_dividends.add_annotation(text='Info taken from yahoo_fin', xref='x domain',
                                                showarrow=False,
                                                font=dict(family=font_figure, size=8, color=light_gray),
                                                yref='y domain', y=-0.12)
        return dcc.Graph(figure=fig_historical_dividends)


@callback(
    Output("dividends_full", "children"),
    Input("store-data", "data")
)
def display_dividend_table(data):
    if data is not None:
        dff = pd.DataFrame(data)
        columns = [{"name": i, "id": i, } for i in dff[['YEAR', 'dividend', 'date']]]
        return dash_table.DataTable(data=dff.to_dict('records'), columns=columns, fill_width=False,
                                    style_header=style_header,
                                    style_cell=style_cell,
                                    style_data_conditional=style_data_conditional,
                                    style_data={'color': dark_gray},
                                    style_table=style_table)


@callback(
    Output("dividends_summary", "children"),
    Input("store-data", "data")
)
def display_dividend_summary(data):
    if data is not None:
        dg = calculate_dividend_summary.get_dividend_summary(data=data, time_delta=time_delta_dividends)
        columns = [{"name": i, "id": i, } for i in dg.columns]
        dg_data = dg.to_dict('records')
        return dash_table.DataTable(data=dg_data, columns=columns, fill_width=False, style_table={'overflowX': 'auto'},
                                    style_cell={'text-align': 'center', "font-family": font_figure,
                                                'backgroundColor': '#ccccc'},
                                    style_data={'backgroundColor': '#E8E8E8', 'color': dark_gray},
                                    style_header={"backgroundColor": main_color, "color": "#FFFFFF", "padding": "10px",
                                                  "border": "0"}
                                    )


@callback(
    Output("title-dividend_Payout", "children"),
    Input("dividends_general_grid", "selectedRows")
)
def display_dividend_payout_title(row):
    if row is not None:
        cell = row[0]['Company (Ticker)']
        ticker = cell[cell.find("(") + 1:cell.find(")")]
        return html.Div([
            html.H2(f"Dividend Payout History for [{ticker}]"),
            html.P('Info taken from yahoo_fin', style={'font-family': font_figure, 'padding': '0px',
                                                       'margin-top': '0px', 'fontSize': 8, 'color': light_gray})
        ])


@callback(
    Output("stocks", "children"),
    Input("dividends_general_grid", "selectedRows")
)
def display_stocks_figure(row):
    if row is not None:
        cell = row[0]['Company (Ticker)']
        ticker = cell[cell.find("(") + 1:cell.find(")")]
        df = get_historical_data_by_ticker.get_historical_data(ticker=ticker, start_date=START_DATE,
                                                               end_date=END_DATE, days_delta=time_delta_stocks)
        fig_historical_data = px.line(df, x='date', y='close')
        fig_historical_data.update_layout(title=dict(
            text=f"<b>Stock Price (5 Years) for [{ticker}]</b>",
            font=dict(family=font_figure, size=font_size, color=dark_gray),
            y=0.9,
            x=0.5,
            xanchor='center',
            yanchor='top'),
            yaxis_title='<b>Stock Price US$</b>',
            xaxis_title=""
        )
        fig_historical_data.add_annotation(
            text='Info taken from yahoo_fin', xref='x domain', showarrow=False,
            font=dict(family=font_figure, size=8, color=light_gray), yref='y domain', y=-0.12)
        return dcc.Graph(figure=fig_historical_data)


if __name__ == '__main__':
    app.run(debug=True)
