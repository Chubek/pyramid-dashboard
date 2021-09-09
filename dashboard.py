import dash
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from scripts.dashboard.plot import *
from scripts.data.filter_by_time import *
from scripts.data.filter_data import *
from scripts.data.es import get_all_indices, get_all_results
from scripts.util.format_date import *
from dotenv import dotenv_values
import dash_table
from datetime import date
from flask import Flask
from metrics_dict import metrics_dict

temp = dotenv_values(".env")

server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)
app.config.suppress_callback_exceptions = True

TABLE_STYLE = {'overflowX': 'scroll', 'height': 500}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f4f9f2",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'overflowX': 'hidden'
}

list_choices = [{"label": l, "value": l} for l in get_all_indices() if not "customerdata" in l]
metrics = metrics_dict[list_choices[0]["value"]]
list_choices_time = [{"label": l, "value": l} for l in ["Daily", "Weekly", "Monthly", "All Time"]]
list_choices_period = {
    "Daily":  [{"label": l, "value": int(l)} for l in ["30", "90", "180", "360"]],
    "Weekly":  [{"label": l, "value": int(l)} for l in ["4", "12", "24", "52"]],
    "Monthly":  [{"label": l, "value": int(l)} for l in ["3", "6", "9", "12", "15", "18", "24"]],
    "All Time": [{"label": "∞", "value": "∞"}]
}
df = get_all_results(index_name=list_choices[0]["value"])

#list_choices_metrics = [{"label": l, "value": l} for l in [col for col in list(df.columns) if "metric" in col]]


card_dropdown = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Product", id="card-bar-title"),
            dcc.Dropdown(
                id='product-dropdown',
                options=list_choices,
                value=list_choices[0]["value"],
                clearable=False
            ),
        ]
    )
)

card_dropdown_date = dbc.Card(
    dbc.Card(
        [
            html.H4("Pick a Number of Day from Today", id="card-bar-title"),
            dcc.Slider(
                    id='day-slider',
                    min=0,
                    max=1000,
                    step=1,
                    value=100,
                    marks={
                         100: {'label': '100 Days', 'style': {'color': '#77b0b1'}},
                         200: {'label': '200 Days', 'style': {'color': '#87b0b1'}},
                         300: {'label': '300 Days', 'style': {'color': '#77a0b1'}},
                         400: {'label': '400 Days', 'style': {'color': '#77b2b1'}},
                         500: {'label': '500 Days', 'style': {'color': '#7750b1'}},
                         600: {'label': '600 Days', 'style': {'color': '#77e0b1'}},
                         700: {'label': '700 Days', 'style': {'color': '#7db0b1'}},
                        800: {'label': '800 Days', 'style': {'color': '#8db0b1'}},
                         900: {'label': '900 Days', 'style': {'color': '#7db0b2'}},

       
                 },
    ),
        ], style={'width':'100vh'}
    )
)


def construct_all_charts(metrics, df):
    line_charts = []
    bar_charts = []
    histograms = []

    for metric in metrics:    
        bar_charts.append(dbc.Card(
        dbc.CardBody(
            [
                html.H4("Bar Chart", id="card-bar-title"),
                dcc.Graph(
                    id='bar-chart',
                    figure=construct_bar_chart(df, temp['DATE_TIME_COLUMN'], metric, "group", f"{metric} - Time Line Plot")
                )
            ]
        )
    ))
    
        line_charts.append(dbc.Card(
            dbc.CardBody(
            [
                html.H4("Line Chart", id="card-line-title"),
                dcc.Graph(
                    id='line-chart',
                    figure=construct_line_chart(df, temp['DATE_TIME_COLUMN'], metric, f"{metric} - Time Line Plot")
        )
                ]
            )
        ))

        histograms.append(dbc.Card(
            dbc.CardBody(
            [
                html.H4("Histogram", id="card-histogram-title"),
                dcc.Graph(
                    id='hist-chart',
                    figure=construct_histogram(df, metric, f"{metric} Histogram")
        )   
            ]
        )
        ))

    return line_charts, bar_charts, histograms

def construct_children(metrics, df):
    line_charts, bar_charts, histograms = construct_all_charts(metrics, df)

    cards_bar = []
    cards_line = []
    cards_hist = []

    for line_chart in line_charts:
        cards_line.append(dbc.Col(line_chart))

    for bar_chart in bar_charts:
        cards_bar.append(dbc.Col(bar_chart))

    for hist in histograms:
        cards_hist.append(dbc.Col(hist))

    return [dbc.Col([*cards_bar, *cards_line, *cards_hist])]

card_table= dbc.Card(
    dbc.CardBody(
        [
            html.H4(f"Data Table for {list_choices[0]['value']}", id="card-table-title"),
            dash_table.DataTable(
                id='table-filtering',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                page_current=0,
                page_size=int(temp['PAGE_SIZE']),
                page_action='custom',

                filter_action='custom',
                filter_query='',
                style_table=TABLE_STYLE
            )
        ]
    )
)


sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Metrics", href="/metrics", active="exact"),
                dbc.NavLink("Movers and Shakers", href="/movers-and-shakers", active="exact"),
                dbc.NavLink("Top Customer Data", href="/top-customer-data", active="exact"),
                dbc.NavLink("Opportunities", href="/opportunities", active="exact"),
                dbc.NavLink("PFRs", href="/pfrs", active="exact"),


            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.H1("This is the Home Page of this Dashboard!")
    if pathname == '/metrics':
        return html.Div(
    [
         
         dbc.Row(
                    card_dropdown,
                ),
                dbc.Row(
                    card_dropdown_date, 
                ),
                dbc.Row(
                    card_table
                ),
               
    
    

            html.Div(
                id="plots-div",
                children=construct_children(metrics, df)
            )
    ])
    elif pathname == '/movers-and-shaker':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif pathname == '/top-customer-data':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif pathname == '/opportunities':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif pathname == '/pfrs':
        return html.Div([
            html.H3('Tab content 5')
        ])

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@app.callback(
    Output('table-filtering', "data"),
    Output('plots-div', 'children'),
    Output('card-table-title', 'children'),
    Input('table-filtering', "page_current"),
    Input('table-filtering', "page_size"),
    Input('table-filtering', "filter_query"),
    Input('day-slider', 'value'),
    Input('product-dropdown', 'value'))
def update_table(page_current,page_size, filter, days, product):
    ctx = dash.callback_context
    global df
    metrics = metrics_dict[product]
    print(ctx.triggered)
    if not ctx.triggered:
        input_id = 'No clicks yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == "table-filtering":
        filtering_expressions = filter.split(' && ')
        dff = df
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        return dff.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records'), construct_children(metrics, dff), f"Data Table for {product}"
    elif input_id == "product-dropdown":
        metrics = metrics_dict[product]
        df = get_all_results(product)
        return df.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records'), construct_children(metrics, df), f"Data Table for {product}"
    elif input_id =="day-slider":        
        df_filt = filter_daily(df, datetime.today(), days)
        df = df_filt
    
        
        return df_filt.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records'), construct_children(metrics, df_filt), f"Data Table for {product}"
    else:
        return df.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records'), construct_children(metrics, df), f"Data Table for {product}"



if __name__ == '__main__':
    #app.run_server(debug=True)
    server.run()