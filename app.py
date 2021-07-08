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

    html.Div(["Sample 1 Size (n1): ", dcc.Input(id='n1', value=32, type='number')]),
    html.Div(["Sample 2 Size (n2): ", dcc.Input(id='n2', value=32, type='number')]),
    html.Div(["Sample 1 Acceptance # (c1): ", dcc.Input(id='c1', value=2, type='number')]),
    html.Div(["Sample 2 Acceptance # (c2): ", dcc.Input(id='c2', value=6, type='number')]),
    html.Div(["Reject (r): ", dcc.Input(id='r', value=5, type='number')]),
    html.Div(["AQL:  ", dcc.Input(id='aql_0', value=0.95, type='number')]),
    html.Div(["RQL: ", dcc.Input(id='rql_0', value=0.9, type='number')]),



    dcc.Graph(id='subplots', responsive=False)
])


@app.callback(
    Output(component_id='subplots', component_property='figure'),
    Input(component_id='n1', component_property='value'),
    Input(component_id='n2', component_property='value'),
    Input(component_id='c1', component_property='value'),
    Input(component_id='c2', component_property='value'),
    Input(component_id='r', component_property='value'),
    Input(component_id='aql_0', component_property='value'),
    Input(component_id='rql_0', component_property='value'))

#def make_perm(pass_tup, iter_vals, ss_1, ss_2, c_1):
#    big_array_list = [binom.pmf(i[0], ss_1, iter_vals)*binom.pmf(i[1], ss_2, iter_vals) for i in pass_tup]
#    big_array_list.append(binom.cdf(c_1, ss_1, iter_vals))
#    return sum(big_array_list)

def update_figure(ss_1, ss_2, c_1, c_2, r, aql, rql):
    
    def make_perm(pass_tup, iter_vals, ss_1, ss_2, c_1):
        big_array_list = [binom.pmf(i[0], ss_1, iter_vals)*binom.pmf(i[1], ss_2, iter_vals) for i in pass_tup]
        big_array_list.append(binom.cdf(c_1, ss_1, iter_vals))
        return sum(big_array_list)
    
    iter_vals=np.arange(0, 1, 0.0001)
    
    ph = [i for i in range(0, c_2-c_1)]
    pass_1 = [i for i in range(c_1+1, r)]
    pass_tup = [(i, j) for i in pass_1 for j in ph if i+j <= c_2]

    title_string = "Double sampling plan for n=" + str(ss_1) + " and c=" + str(c_1)
    #plot1_title = "Single Sampling (n=" + str(ss_1) + ", c=" + str(c_1) + ')'
    plot2_title = "Double Sampling (n=" + str(ss_1) + ", c=" + str(c_1) + ') and (n=' + str(ss_2) + ", c=" + str(c_2) + ")"

    fig = make_subplots(subplot_titles=(plot2_title, ' '), shared_yaxes=True, rows=1, cols=2)
    
    #fig = make_subplots(subplot_titles=(plot1_title, plot2_title), shared_yaxes=True, rows=1, cols=2)

    #fig.add_trace(
    #    go.Scatter(x=iter_vals, y=binom.cdf(c_1, sample_size_1, iter_vals), hovertemplate='Probability of Acceptance: %{y:%.2f}<extra></extra>'),
    #    row=1, col=1)

    fig.add_trace(
        go.Scatter(x=iter_vals, y=make_perm(pass_tup, iter_vals, ss_1, ss_2, c_1), hovertemplate='Probability of Acceptance: %{y:%.2f}<extra></extra>'),
        row=1, col=1)

    if type(aql) == float:
        fig.add_hline(y=aql, line_width=2, line_dash="dash", line_color="black")    
    if type(rql) == float:
        fig.add_hline(y=1-rql, line_width=2, line_dash="dash", line_color="black")
        
    fig.update_xaxes(title_text="Fraction Defective", row=1, col=1)
    fig.update_xaxes(title_text="Fraction Defective", row=1, col=2)
    fig.update_yaxes(title_text="Probability of Acceptance", row=1, col=1)

    fig.update_layout(height=600, width=1200, showlegend=False, template='plotly_white', hovermode='x unified')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
