import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from scripts.dashboard.plot import *
from scripts.data.filter_by_time import *
from scripts.data.filter_data import *
from scripts.data.es import get_all_results
from dotenv import dotenv_values

temp = dotenv_values(".env")

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

df = get_all_results()

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASHBOARD FOR CUSTOMER DATA'),
                                 html.P('Data visualization for customer data.'),
                                 html.P('Please select a page.'),  
                                ]),
                            ]),
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                    dcc.Tab(label='Metrics', value='metrics', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Movers and Shakers', value='movers-and-shakers', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Top Customer Data', value='top-customer-data', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Opportunities', value='opportunities', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='PFRs', value='pfrs', style=tab_style, selected_style=tab_selected_style),

                ], style=tabs_styles),
                html.Div(id='tabs-content-inline')
        ]
    )

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'metrics':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'movers-and-shaker':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'top-customer-data':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'opportunities':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'pfrs':
        return html.Div([
            html.H3('Tab content 5')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)