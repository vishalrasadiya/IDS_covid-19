import numpy as np
import pandas as pd
import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import random
import plotly.graph_objects as go


df_dash = pd.read_csv('E:/ads_covid-19/IDS_covid-19/data/processed/SIR_calculated.csv',sep=';')

color_list = []

for i in range(int((df_dash.shape[1]-1)/2)):
    random_color = '#%02x%02x%02x' % (random.randint(0, 255),random.randint(0, 255), random.randint(0, 255))
    color_list.append(random_color)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = go.Figure()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background'],}, children = [

    dcc.Markdown('''
        #  Data Science Project @ TU_KL on COVID-19 Data - Part 2
        ''',
        style={
            "border":"2px silver solid",
            'textAlign': 'center',
            'color': colors['text']
    }),

    dcc.Markdown('''
        ##  Plot shows actual number of infected people and simulated number of infected people\
            derived from SIR model for different countries.
        ''',
        style = {
            "border":"2px silver solid",
            'backgroundColor': colors['background'],
            'position' : 'fixed',
            'left' : 7,
            'top' : 83,
            'width' : 500,
            'height' : 1161,
            'textAlign': 'left',
            'border':'2px silver solid',
            'color': colors['text']

    }),

    dcc.Markdown('''
        ### Select the country below:
        ''',
        style={
                'textAlign': 'left',
                'color': colors['text'],
                'position':'fixed',
                'top':350,
                'left': 7,
                'width' :500,
    }),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_dash.columns[1:187]],
        value=['Germany'], # Which is pre-selected
        multi=True,
        style={
                'position': 'fixed',
                'left' : 7,
                'top' : 425,
                'textAlign': 'left',
                'color': colors['text'],
                'background-color': '#ededdf',
                'font-size' : 'large',
                'height': 100,
                'width': 500,
    }),


    dcc.Graph(
        figure=fig,
        id='SIR',
        style = {
            "border":"2px silver solid",
            'backgroundColor': colors['background'],
            'height' : 1161,
            'textAlign': 'center',
            'align' : 'right',
            'position' : 'fixed',
            'left' : 507,
            'top' : 83,
            'width' : '80%',
            'color': colors['text']

    })
])



@app.callback(
    Output('SIR', 'figure'),
    [Input('country_drop_down', 'value')])
def update_figure(country_list):


    traces = []
    for pos, each in enumerate(country_list):

        traces.append(dict(x=df_dash.Date,
                                y=df_dash[each],
                                mode='lines',
                                opacity=0.9,
                                name=each,
                                line = dict(color = color_list[pos])
                        )
                )
        traces.append(dict(x=df_dash.Date,
                                y=df_dash[each+'_fitted'],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each+'_simulated',
                                line = dict(color = color_list[pos])
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1800,
                height=1000,
                plot_bgcolor = colors['background'],
                paper_bgcolor = colors['background'],
                xaxis={'title':'Timeline',
                        'tickangle':-25,
                        'nticks':20,
                        'tickfont':dict(size=18,color=colors['text']),
                        'titlefont': dict(size=22, color=colors['text']),
                      },

                yaxis={'type':"log", 'title':'Number of infected people (log-scale)',
                       'tickfont':dict(size=18,color=colors['text']),
                       'titlefont': dict(size=22, color=colors['text'])
                      },
                title={'text': "Real and Simulated Number of Infected People",
                       'y':0.95,
                       'x':0.5,
                       'xanchor': 'center',
                       'yanchor': 'top',
                       'font': dict(size=22, color=colors['text'])
                      }

            )

}

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)
