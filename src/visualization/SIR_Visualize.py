import numpy as np
import pandas as pd
import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import random
import plotly.graph_objects as go


df_dash = pd.read_csv('E:/ads_covid-19/data/processed/SIR_calculated.csv',sep=';')

color_list = []
for i in range(int((df_dash.shape[1]-1)/2)):
    random_color = '#%02x%02x%02x' % (random.randint(0, 255),random.randint(0, 255), random.randint(0, 255))
    color_list.append(random_color)

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
    for pos, each in enumerate(country_list):

        df_plot=df_dash[[each, each+'_fitted']]

        traces.append(dict(x=df_plot.index,
                                y=df_plot[each],
                                mode='lines',
                                opacity=0.9,
                                name=each,
                                line = dict(color = color_list[pos])
                        )
                )
        traces.append(dict(x=df_plot.index,
                                y=df_plot[each+'_fitted'],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each+'_simulated',
                                line = dict(color = color_list[pos])
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
