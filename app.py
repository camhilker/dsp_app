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


#google analytics code
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-201960300-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'UA-201960300-1');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""



app.layout = html.Div(children=[
    html.H1(children='Double Sampling Plan Generator'),

    html.Br(),

    html.Div(
        [html.Div(
            [html.Div(
                ["Lot Size: ", 
                html.Br(), 
                dcc.Input(id='lot', value=1000, type='number'), 
                html.Br(),
                html.Br(),

                "Sample 1 Size (n1): ", 
                html.Br(), 
                dcc.Input(id='n1', value=32, type='number'), 
                html.Br(),
                html.Br(), 
                
                "Sample 1 Acceptance # (c1): ", 
                html.Br(), 
                dcc.Input(id='c1', value=2, type='number')], 

                style={'margin': 'auto', 'display':'table-cell'}),

            html.Div(
                ["Sample 2 Size (n2): ", 
                html.Br(), 
                dcc.Input(id='n2', value=32, type='number'), 
                html.Br(),
                html.Br(), 
                
                "Sample 2 Acceptance # (c2, total number of accepted failures): ", 
                html.Br(), 
                dcc.Input(id='c2', value=6, type='number'),
                html.Br(),
                html.P(id='err_2', hidden=True, 
                    children=['c2 must be greater than c1'])
                ],
                         
                style={'margin': 'auto', 'display':'table-cell'}),
            


            html.Div(
                ["Reject (r): ", 
                html.Br(), 
                dcc.Input(id='r', value=5, type='number'),
                html.Br(),
                html.P(id='err_1', hidden=True, 
                    children=['r must be greater than c1']),
                html.Br(),

                "AQL:  ", 
                html.Br(), 
                dcc.Input(id='aql_0', value=0.95, type='number'),
                html.Br(),
                html.Br(), 

                "RQL: ", 
                html.Br(), 
                dcc.Input(id='rql_0', value=0.9, type='number')], 
                         
                style={'margin': 'auto', 'display':'table-cell'})], 

            style={'margin': 'auto', 'display':'table-row'})],

    style={'margin': 'auto', 'width':'100%', 'display':'table'}),


    html.Div(dcc.Graph(id='subplots', responsive=False), 
                 
            style={'margin': 'auto', 'width':'50%', 'display':'table'}),
])

@app.callback(
    [Output(component_id='err_1', component_property='style'),
    Output(component_id='err_2', component_property='style'),
    Output(component_id='subplots', component_property='figure')],
    [Input(component_id='lot', component_property='value'),
    Input(component_id='n1', component_property='value'),
    Input(component_id='n2', component_property='value'),
    Input(component_id='c1', component_property='value'),
    Input(component_id='c2', component_property='value'),
    Input(component_id='r', component_property='value'),
    Input(component_id='aql_0', component_property='value'),
    Input(component_id='rql_0', component_property='value')])

#def make_perm(pass_tup, iter_vals, ss_1, ss_2, c_1):
#    big_array_list = [binom.pmf(i[0], ss_1, iter_vals)*binom.pmf(i[1], ss_2, iter_vals) for i in pass_tup]
#    big_array_list.append(binom.cdf(c_1, ss_1, iter_vals))
#    return sum(big_array_list)




def update_figure(lot, ss_1, ss_2, c_1, c_2, r, aql, rql):

    if None in (lot, ss_1, ss_2, c_1, c_2, r):
        raise dash.exceptions.PreventUpdate
    
    if c_2 <= c_1:
        return {'display':'none'}, {'display':'inline', 'color':'red'}, dash.no_update

    if r <= c_1:
        return {'display':'inline', 'color':'red'}, {'display':'none'}, dash.no_update

    else:



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

        fig.update_layout(height=600, width=1500, showlegend=False, template='plotly_white', hovermode='x unified')

        return {'display':'none'}, {'display':'none'}, fig


def make_perm(pass_tup, iter_vals, ss_1, ss_2, c_1):
    big_array_list = [binom.pmf(i[0], ss_1, iter_vals)*binom.pmf(i[1], ss_2, iter_vals) for i in pass_tup]
    big_array_list.append(binom.cdf(c_1, ss_1, iter_vals))
    return sum(big_array_list)


if __name__ == '__main__':
    app.run_server(debug=True)
