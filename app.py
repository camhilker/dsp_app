import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
from scipy.stats import binom

import plotly.graph_objects as go
from plotly.subplots import make_subplots


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Double Sampling Plan Generator'),

    html.Br(),

    html.Div(["Sample 1 Size: ", dcc.Input(id='ss1', value=100, type='number')]),
    html.Div(["Sample 2 Size: ", dcc.Input(id='ss2', value=25, type='number')]),
    html.Div(["Sample 1 Allowable Failures: ", dcc.Input(id='f1', value=4, type='number')]),
    html.Div(["Sample 2 Allowable Failures: ", dcc.Input(id='f2', value=4, type='number')]),
    html.Div(["AQL:  ", dcc.Input(id='aql_0', value=0.95, type='number')]),
    html.Div(["RQL: ", dcc.Input(id='rql_0', value=0.9, type='number')]),



    dcc.Graph(id='subplots', responsive=False)
])


@app.callback(
    Output(component_id='subplots', component_property='figure'),
    Input(component_id='ss1', component_property='value'),
    Input(component_id='ss2', component_property='value'),
    Input(component_id='f1', component_property='value'),
    Input(component_id='f2', component_property='value'),
    Input(component_id='aql_0', component_property='value'),
    Input(component_id='rql_0', component_property='value'))

def update_figure(sample_size_1, sample_size_2, failures_1, failures_2, aql, rql):

    iter_vals=np.arange(0, 1, 0.0001)

    title_string = "Double sampling plan for n=" + str(sample_size_1) + " and c=" + str(failures_1)
    plot1_title = "First Sampling (n=" + str(sample_size_1) + " and c=" + str(failures_1) + ')'
    plot2_title = "Second Sampling (n=" + str(sample_size_2) + " and c=" + str(failures_2) + ')'


    fig = make_subplots(subplot_titles=(plot1_title, plot2_title), shared_yaxes=True, rows=1, cols=2)

    fig.add_trace(
        go.Scatter(x=iter_vals, y=binom.cdf(failures_1, sample_size_1, iter_vals), hovertemplate='Probability of Acceptance: %{y:%.2f}<extra></extra>'),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=iter_vals, y=binom.pmf(failures_2, sample_size_1, iter_vals)*
                   binom.pmf(0, sample_size_2, iter_vals), hovertemplate='Probability of Acceptance: %{y:%.2f}<extra></extra>'),
        row=1, col=2)


    fig.add_hline(y=aql, line_width=2, line_dash="dash", line_color="black")
    fig.add_hline(y=1-rql, line_width=2, line_dash="dash", line_color="black")

    fig.update_xaxes(title_text="Fraction Defective", row=1, col=1)
    fig.update_xaxes(title_text="Fraction Defective", row=1, col=2)
    fig.update_yaxes(title_text="Probability of Acceptance", row=1, col=1)

    fig.update_layout(height=600, width=1200, showlegend=False, template='plotly_white', hovermode='x unified')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
