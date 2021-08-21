import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from scripts.dashboard.plot import *
from scripts.data.filter_by_time import *
from scripts.data.filter_data import *
from scripts.data.es import get_all_results
from dotenv import dotenv_values
import dash_table


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

df = get_all_results(index_name=temp['INDEX_NAME'])

card_bar = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Bar Chart", id="card-bar-title"),
            dcc.Graph(
                    id='bar-chart',
                    figure=construct_bar_chart(df, "Customer Name", "Metric A", "Metric C", "group", "Customer Name - Metric A Plot")
    )
        ]
    )
)


card_line = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Line Chart", id="card-line-title"),
            dcc.Graph(
                    id='line-chart',
                    figure=construct_line_chart(df, "Customer Name", "Metric A", "Metric C", "Customer Name - Metric A Plot")
    )
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

card_histogram = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Histogram", id="card-histogram-title"),
            dcc.Graph(
                    id='scatter-chart',
                    figure=construct_histogram(df, "Metric C", "Metric C Histogram")
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
        dbc.Row( 
            dbc.Col(
                   card_table,
                    width={"size": 12, "order": 1, "offset": 1},
                )     
                        
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
    Output('table-filtering', "data"),
    Input('table-filtering', "page_current"),
    Input('table-filtering', "page_size"),
    Input('table-filtering', "filter_query"))
def update_table(page_current,page_size, filter):
    print(filter)
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


if __name__ == '__main__':
    app.run_server(debug=True)