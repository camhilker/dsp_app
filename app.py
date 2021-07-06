import dash
import dash_core_components as dcc
import dash_html_components as html

import numpy as np
from scipy.stats import binom

import plotly.graph_objects as go
from plotly.subplots import make_subplots


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

sample_size_1 = 100
sample_size_2 = 32
failures_1 = 5
failures_2 = 5

aql=0.95
rql=0.90
iter_vals=np.arange(0, 1, 0.0001)


fig = make_subplots(subplot_titles=(plot1_title, plot2_title), shared_yaxes=True, rows=1, cols=2)

fig.add_trace(
    go.Scatter(x=iter_vals, y=binom.cdf(failures_1, sample_size_1, iter_vals)),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=iter_vals, y=binom.pmf(failures_2, sample_size_1, iter_vals)*
               binom.pmf(0, sample_size_2, iter_vals)),
    row=1, col=2
)
fig.add_hline(y=aql, line_width=2, line_dash="dash", line_color="black")
fig.add_hline(y=1-rql, line_width=2, line_dash="dash", line_color="black")

fig.update_xaxes(title_text="Fraction Defective", row=1, col=1)
fig.update_xaxes(title_text="Fraction Defective", row=1, col=2)

fig.update_yaxes(title_text="Probability of Acceptance", row=1, col=1)

fig.update_layout(height=600, width=800, title_text=title_string, showlegend=False, template='plotly_white')

app.layout = html.Div(children=[
    html.H1(children='Double Sampling Plan App'),

    html.Div(children='''
        when I was a young boy my father took me into the city to see a marching band. He said son when you grow up will you be the savior of the broken the beaten and the damned?
    '''),

    dcc.Graph(
        id='subplots',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)