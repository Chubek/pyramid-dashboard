import dash
from dash_bootstrap_components._components.Col import Col
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

temp = dotenv_values(".env")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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

list_choices = [{"label": l, "value": l} for l in get_all_indices()]
list_choices_time = [{"label": l, "value": l} for l in ["Daily", "Weekly", "Monthly"]]
list_choices_period = {
    "Daily":  [{"label": l, "value": int(l)} for l in ["30", "90", "180", "360"]],
    "Weekly":  [{"label": l, "value": int(l)} for l in ["4", "12", "24", "52"]],
    "Monthly":  [{"label": l, "value": int(l)} for l in ["3", "6", "9", "12", "15", "18", "24"]],
}

list_choices_metrics = [{"label": l, "value": int(l)} for l in [col for col in list(df.columns) if "Metric" in Col]]

df = get_all_results(index_name=list_choices[0]["value"])

card_dropdown = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Product", id="card-bar-title"),
            dcc.Dropdown(
                id='metrics-dropdown',
                options=list_choices,
                value=list_choices[0]["value"]
            ),
        ]
    )
)

card_period = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Period", id="card-bar-title"),
            dcc.Dropdown(
                id='period-dropdown',
                options=list_choices_period["Daily"],
                value=list_choices_period["Daily"][0]
            ),
        ]
    )
)

card_dropdown_date = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Time Range", id="card-bar-title"),
            dcc.Dropdown(
                id='time-dropdown',
                options=list_choices_time,
                value=list_choices_time[0]["value"]
            ),
        ]
    )
)

card_dropdown_date = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Start and End Date", id="card-bar-title"),
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                initial_visible_month=return_date(df.iloc[0][temp['DATE_TIME_COLUMN']]),
                end_date=return_date(df.iloc[0][temp['DATE_TIME_COLUMN']])
    ),
        ]
    )
)
card_dropdown_bar = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Metric for Bar Chart", id="bar-metric-title"),
            dcc.Dropdown(
                id='bar-dropdown',
                options=list_choices_metrics,
                value=list_choices_metrics[0]["value"]
            ),
        ]
    )
)
card_bar = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Bar Chart", id="card-bar-title"),
            dcc.Graph(
                    id='bar-chart',
                    figure=construct_bar_chart(df, temp['DATE_TIME_COLUMN'], "Metric A", "group", "Customer Name - Metric A Plot")
    )
        ]
    )
)
card_dropdown_line = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Metric for Line Chart", id="line-metric-title"),
            dcc.Dropdown(
                id='line-dropdown',
                options=list_choices_metrics,
                value=list_choices_metrics[0]["value"]
            ),
        ]
    )
)

card_line = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Line Chart", id="card-line-title"),
            dcc.Graph(
                    id='line-chart',
                    figure=construct_line_chart(df, temp['DATE_TIME_COLUMN'], "Metric A", "Customer Name - Metric A Plot")
    )
        ]
    )
)

card_dropdown_scatter_x = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Metric for Scatter Chart X", id="xsx-metric-title"),
            dcc.Dropdown(
                id='sxs-dropdown',
                options=list_choices_metrics,
                value=list_choices_metrics[0]["value"]
            ),
        ]
    )
)
card_dropdown_scatter_y = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Metric for Scatter Chart X", id="ysy-metric-title"),
            dcc.Dropdown(
                id='sys-dropdown',
                options=list_choices_metrics,
                value=list_choices_metrics[0]["value"]
            ),
        ]
    )
)
card_scatter = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Scatter Chart", id="card-scatter-title"),
            dcc.Graph(
                    id='scatter-chart',
                    figure=construct_scatter_chart(df, "Metric C", "Metric A", "Metric C - Metric A Plot")
    )
        ]
    )
)

card_dropdown_hist = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Pick a Metric for Histogram", id="hist-metric-title"),
            dcc.Dropdown(
                id='hist-dropdown',
                options=list_choices_metrics,
                value=list_choices_metrics[0]["value"]
            ),
        ]
    )
)


card_histogram = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Histogram", id="card-histogram-title"),
            dcc.Graph(
                    id='hist-chart',
                    figure=construct_histogram(df, "Metric A", "Metric A Histogram")
    )
        ]
    )
)

card_table= dbc.Card(
    dbc.CardBody(
        [
            html.H4("Data Table", id="card-table-title"),
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
        dbc.Row([
            dbc.Col(
                    card_table,
                    width={"size": 12, "order": 1, "offset": 1},
                ),
            dbc.Col(
                    card_dropdown,
                    width={"size": 6, "order": 1, "offset": 1},
                ),
                
                 ]    
                        
        ),
        dbc.Row(
            [
                dbc.Col(
                    card_bar,
                    width={"size": 8, "order": "last", "offset": 1},
                ),
                dbc.Col(
                    card_line,
                    width={"size": 8, "order": 1, "offset": 1},
                )
            ]
        ),
        dbc.Row([
            dbc.Col(
                card_histogram,
                width={"size": 8, "offset": 1},
            ),
                dbc.Col(
                    card_scatter,
                    width={"size": 8, "offset": 1},
                ),
        ]),
    ]
)
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
    Output('bar-chart', "figure"),
    Input('bar-dropdown', "value"))
def change_bar_chart(value):
    return construct_bar_chart(df, temp['DATE_TIME_COLUMN'], value, "group", f"Customer Name - {value} Plot")

@app.callback(
    Output('line-chart', "figure"),
    Input('line-dropdown', "value"))
def change_line_chart(value):
    return construct_line_chart(df, temp['DATE_TIME_COLUMN'], value, f"Customer Name - {value} Plot")

@app.callback(
    Output('line-chart', "figure"),
    [Input('sxs-dropdown', "value"),
    Input('sys-dropdown', "value")])
def change_scattere_chart(value_x, value_y):
    return construct_scatter_chart(df, value_x, value_y, f"{value_x} - {value_y} Plot")

@app.callback(
    Output('hist-chart', "figure"),
    Input('hist-dropdown', "value"))
def change_line_chart(value):
    return construct_histogram(df, value, f"{value} Histogram")

@app.callback(
    Output('table-filtering', "data"),
    Input('table-filtering', "page_current"),
    Input('table-filtering', "page_size"),
    Input('table-filtering', "filter_query"))
def update_table(page_current,page_size, filter):
    print(filter)
    global df
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
    ].to_dict('records')


@app.callback(
    Output('period-dropdown', 'value'),
    Output('period-dropdown', 'options'),
    Output('table-filtering', "data"),
    Output('table-filtering', "page_current"),
    Output('table-filtering', "filter_query"),
    [Input('metrics-dropdown', 'value')])
def update_output(value):
    return get_all_results(value), 0, "", list_choices_period[value], list_choices_period[value][0]

@app.callback(
    Output('table-filtering', "data"),
    Output('table-filtering', "page_current"),
    Output('table-filtering', "filter_query"),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('time-dropdown', 'value'),
    Input('period-dropdown', 'value')])
def update_table(start_date, end_date, dropdown, period):
    global df
    if dropdown == "Daily":
        df_filt = filter_daily(df, start_date, period)
        df = df_filt
    elif dropdown == "Weekly":
        df_filt = filter_weekly(df, start_date, period)
        df = df_filt
    elif dropdown == "Monthly":
        df_filt = filter_monthly(df, start_date, period)
        df = df_filt
    else:
        df_filt = df
    return df_filt, 0, ""


if __name__ == '__main__':
    app.run_server(debug=True)