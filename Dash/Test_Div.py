import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import git

header = []
tyh = []

repo = git.cmd.Git('C:/Users/isr/OneDrive/Documentos/Enose')
repo.pull()

app = dash.Dash()

df = pd.read_csv(
    'C:/Users/isr/OneDrive/Documentos/Enose/smartiago/Mean_Data.csv')

for col in df.columns:
    if (col != "Date") and (col != "Time") and (col != "NA") and (col != "NA.1"):
        if (col == "Temperature") or (col == "Humidity"):
            tyh.append(col)
        else:
            header.append(col)

df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')

app.layout = html.Div([
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    html.Div(
                        children=dcc.Graph(
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
                                    xaxis={'title': 'Date'},
                                    yaxis={'title': 'Sensor Response'},
                                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                    legend={'x': 1, 'y': 1},
                                    hovermode='closest',
                                    height=350,
                                    width=1000,
                                )
                            }
                        ),
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id='TyH vs Time',
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
                                    xaxis={'title': 'Date'},
                                    yaxis={'title': 'Temperature and Humidity'},
                                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                    legend={'x': 1, 'y': 1},
                                    hovermode='closest',
                                    height=350,
                                    width=1000
                                )
                            }
                        ),
                    )

                ]
            ),
            html.Div(
                className="six columns",
                children=html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': 'SP-51-00', 'value': 'SP-51-00'},
                            {'label': 'SP-11-00', 'value': 'SP-11-00'}
                        ],
                        values=['SP-51-00', 'SP-11-00'],
                        style={'vertical-align': 'middle'},
                    ),
                    dcc.Graph(
                        id='right-bottom-graph',
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }],
                            'layout': {
                                'height': 400,
                                'margin': {'l': 10, 'b': 20, 't': 0, 'r': 0}
                            }
                        }
                    ),

                ])
            )
        ]
    )
])

app.css.append_css({'C:/Users/isr/iCloudDrive/Master/TFM/Dash/style.css'})

if __name__ == '__main__':
    app.run_server(debug=True)