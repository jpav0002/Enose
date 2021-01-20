import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import git

header = []
tyh = []

repo = git.cmd.Git('../')
repo.pull()

app = dash.Dash()

df = pd.read_csv(
    '../smartiago/Mean_Data.csv')

for col in df.columns:
    if (col != "Date") and (col != "Time") and (col != "NA") and (col != "NA.1"):
        if (col == "Temperature") or (col == "Humidity"):
            tyh.append(col)
        else:
            header.append(col)

df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')

app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[
                              html.H2('Enose Dashboard - Measurement'),
                              html.P('Control Panel for Sensors'),
                              html.P('Pick sensor you want to visualize'),

                              html.Div(
                                  dcc.Checklist(
                                      options=[{'label': 'SP-51-00', 'value': 'SP-51-00'}, {'label': 'SP-11-00', 'value': 'SP-11-00'}],
                                      value=['SP-51-00', 'SP-11-00'],
                                      style={'vertical-align': 'left'},
                                  )
                              )
                          ]),  # Define the left element

                 html.Div(className='eight columns div-for-charts bg-grey',
                          children=[
                              dcc.Graph(
                                  id='Sensor vs Time',
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
                                          xaxis={'title': 'Date', 'gridcolor':'gray'},
                                          yaxis={'title': 'Sensor Response','gridcolor':'gray'},
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
                                  id='Temp and Hum vs Time',
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
                                          xaxis={'title': 'Date', 'gridcolor':'gray'},
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

if __name__ == '__main__':
    app.run_server(debug=True)
