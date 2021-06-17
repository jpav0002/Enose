import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dataConverter
import plotly.graph_objs as go
import git
import dash_functions
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

header = []
tyh = []

repo = git.cmd.Git('../')
repo.pull()

#dataConverter.preprocess()

app = dash.Dash()

#df = pd.read_csv('../smartiago_v2/Mean_Data.csv')
#df = pd.read_csv('./Data_processed/processed.csv')
df = pd.read_csv('../smartiago/Mean_Data.csv')

for col in df.columns:
    if (col != "Date") and (col != "Time") and (col != "NA") and (col != "NA.1"):
        if ("Temperature" in col) or ("Humidity" in  col):
            tyh.append(col)
        else:
            header.append(col)

df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')

app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns columns div-user-controls',
                          children=[
                              html.H1('Enose Dashboard - Measurement'),

                              html.Div(className='six columns controls-1',
                                       children=[
                                           html.P('Control Panel for Sensors'),
                                           html.Div(
                                               className='div-for-checklist-sensor',
                                               children=[
                                                   dcc.Checklist(
                                                       id='sensor_selector',
                                                       options=dash_functions.get_options(header), value=header,
                                                       style={'horizontal-align': 'right'},
                                                   ),
                                               ]),
                                           html.Div(
                                               className='div-for-checklist-sensor',
                                               children=[
                                                   dcc.RadioItems(
                                                       id='select_op',
                                                       options=[
                                                           {'label': 'Select All', 'value': 'sel_all'},
                                                           {'label': 'Clear All', 'value': 'clear_all'},
                                                       ],
                                                       style={'horizontal-align': 'right'},
                                                       labelStyle={'display': 'inline-block'},
                                                       value="sel_all"
                                                   )
                                               ]
                                           ),
                                           html.Div(className='div-for-dates',
                                                    children=[
                                                        html.P('Select dates'),
                                                        dcc.DatePickerRange(
                                                            id='date-picker',
                                                            display_format='DD/MM/YY',
                                                            min_date_allowed=df['DateTime'].iloc[0]-timedelta(hours=24),
                                                            max_date_allowed=df['DateTime'].iloc[-1]+timedelta(hours=24),
                                                            start_date=df['DateTime'].iloc[0],
                                                            end_date=df['DateTime'].iloc[-1],
                                                            style={'display': 'inline-block',
                                                                   'border-collapse': 'separate'},
                                                        ),
                                                    ]),
                                       ]),

                              html.Div(className='four columns',
                                       children=[
                                           html.P('Environmental Variables'),
                                           html.Div(
                                               className='div-for-checklist_sensor',
                                               children=[
                                                   dcc.Checklist(
                                                       id='env_selector',
                                                       options=dash_functions.get_options(tyh),
                                                       value=tyh,
                                                       style={'horizontal-align': 'right', 'backgroundColor': 'rgb(30,30,30)'},
                                                   )
                                               ]),
                                       ]),
                          ]),

                 html.Div(className='eight columns div-for-charts bg-grey',
                          children=[
                              dcc.Graph(
                                  id='Sensor_vs_Time',
                                  figure={
                                      'data': [
                                          go.Scatter(
                                              x=df['DateTime'],
                                              y=df[i],
                                              text=df[i],
                                              mode='markers',
                                              opacity=0.8,
                                              marker={
                                                  'size': 5,
                                                  'line': {'width': 0.5, 'color': 'white'}
                                              },
                                              name=i
                                          ) for i in header
                                      ],
                                      'layout': go.Layout(
                                          xaxis={'title': 'Date', 'gridcolor': 'gray'},
                                          yaxis={'title': 'Sensor Response', 'gridcolor': 'gray'},
                                          margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                          legend={'x': 1, 'y': 1},
                                          hovermode='closest',
                                          height=350,
                                          width=920,
                                          template='plotly_dark',
                                          plot_bgcolor='rgba(0,0,0,0)',
                                          paper_bgcolor='rgba(0,0,0,0)'
                                      )
                                  }
                              ),
                              dcc.Graph(
                                  id='Temp_and_Hum_vs_Time',
                                  figure={
                                      'data': [
                                          go.Scatter(
                                              x=df['DateTime'],
                                              y=df[i],
                                              text=df[i],
                                              mode='markers',
                                              opacity=0.8,
                                              marker={
                                                  'size': 5,
                                                  'line': {'width': 0.5, 'color': 'white'}
                                              },
                                              name=i
                                          ) for i in tyh
                                      ],
                                      'layout': go.Layout(
                                          xaxis={'title': 'Date', 'gridcolor': 'gray'},
                                          yaxis={'title': 'Temperature and Humidity', 'gridcolor': 'gray'},
                                          margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                          legend={'x': 1, 'y': 1},
                                          hovermode='closest',
                                          height=350,
                                          width=920,
                                          template='plotly_dark',
                                          plot_bgcolor='rgba(0,0,0,0)',
                                          paper_bgcolor='rgba(0,0,0,0)',
                                      )
                                  }
                              ),
                          ])  # Define the right element
             ])
])


@app.callback(Output('sensor_selector', 'value'),
              [Input('select_op', 'value')])
def deactivate_all(option):
    if option == "sel_all":
        value = header
    else:
        value = []
    return value


@app.callback([Output('Temp_and_Hum_vs_Time', 'figure'),
               Output('Sensor_vs_Time', 'figure')],
              [Input('env_selector', 'value'),
               Input('sensor_selector', 'value'),
               Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date')])
def update_graphs(env_var, sensor_var, start, end):

    af_start = df["DateTime"] >= pd.to_datetime(start)
    bf_end = df["DateTime"] <= pd.to_datetime(end)+timedelta(hours=24)
    print(pd.to_datetime(end))
    between = af_start & bf_end
    filtered = df.loc[between]

    figure_env = {
        'data': [
            go.Scatter(
                x=filtered['DateTime'],
                y=filtered[i],
                text=filtered[i],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in env_var
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date', 'gridcolor': 'gray'},
            yaxis={'title': 'Sensor Response', 'gridcolor': 'gray'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            height=350,
            width=920,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
    }

    figure_sensor = {
        'data': [
            go.Scatter(
                x=filtered['DateTime'],
                y=filtered[i],
                text=filtered[i],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in sensor_var
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date', 'gridcolor': 'gray'},
            yaxis={'title': 'Sensor Response', 'gridcolor': 'gray', 'range':[0,5]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            height=350,
            width=920,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
    }
    return figure_env, figure_sensor


if __name__ == '__main__':
    app.run_server(debug=True)
