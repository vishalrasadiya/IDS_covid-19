import numpy as np
import pandas as pd
import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import plotly.graph_objects as go


df_dash = pd.read_csv('E:/ads_covid-19/data/processed/SIR_calculated.csv',sep=';')

fig = go.Figure()
app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Actual and Simulated Number of Infected People
    '''),

    dcc.Markdown('''
    ##  Plot shows actual number of infected people and simulated number of infected people for different countries derived from SIR model.
    '''),

    dcc.Markdown('''
    ### Select the country:
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_dash.columns[1:187]],
        value=['Germany'], # Which is pre-selected
        multi=True
    ),


    dcc.Graph(figure=fig, id='SIR')
])



@app.callback(
    Output('SIR', 'figure'),
    [Input('country_drop_down', 'value')])
def update_figure(country_list):


    traces = []
    for each in country_list:

        df_plot=df_dash[[each, each+'_fitted']]

        traces.append(dict(x=df_plot.index,
                                y=df_plot[each],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )
        traces.append(dict(x=df_plot.index,
                                y=df_plot[each+'_fitted'],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each+'_simulated'
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1700,
                height=870,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=20,color="#7f7f7f"),
                        'titlefont': dict(size=25)

                      },

                yaxis={'type':"log", 'title':'Number of infected people (log-scale)',
                       'tickfont':dict(size=18,color="#7f7f7f"),
                       'titlefont': dict(size=25)
                      },

        )
    }

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)
