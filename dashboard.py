# -*- coding: utf-8 -*-

import os
import pathlib
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

#Data for Tab-1
# Reading data for Map with Slider
df = pd.read_csv('ufo_data.csv')
df['year'] = df['Date_time'].apply(lambda x: int(re.findall(r'...\d\s', str(x))[0].strip()))
YEARS = range(df['year'].min(), df['year'].max() + 1, 4)

df = df[df['latitude'] != '33q.200088']

# Data for Stacked Bar Chart
df1 = df.groupby(['year', 'country'], sort=False).size().reset_index(name='Count')

us_data = df1[df1['country'] == 'us']
ca_data = df1[df1['country'] == 'ca']
au_data = df1[df1['country'] == 'au']
gb_data = df1[df1['country'] == 'gb']
year = df1['year'].to_list()
# Change the bar mode

#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.

#Data for Tab-2
# Import data and read .csv files to create Pandas DataFram
path = 'ufo_data.csv'
data_viz3 = pd.read_csv(path)
data_viz3.dropna()

available_indicators = data_viz3['UFO_shape'].unique()
country = data_viz3['country'].unique()
ufo_count = data_viz3['UFO_shape'].value_counts()

# Map with Slider
def MAP(selected_year):
    callback_df = df[df.year == selected_year]
    callback_df['latitude'] = callback_df['latitude'].astype(float)
    fig = px.scatter_mapbox(callback_df, lat='latitude', lon='longitude', text='description', zoom=1,
                            color_discrete_sequence=["crimson"])
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="darkgray", showland=True, landcolor="black",
                    showocean=True, oceancolor="darkslategrey", showlakes=True, lakecolor="darkslategrey",
                    showrivers=True, rivercolor="darkgray")
    fig.update_layout(mapbox_style="open-street-map", hovermode='closest', autosize=True,
                      margin=dict(t=0, b=0, l=0, r=0))
    fig.update_layout(paper_bgcolor="#F4F4F9", plot_bgcolor="#F4F4F9")
    return fig

# Python Plots/Functions for Callbacks and Outputs:
def plot_1(country, shape):
    filtered_df = data_viz3[data_viz3.country.isin(country)]
    filtered_df = filtered_df[filtered_df.UFO_shape.isin(shape)]
    # filtered_df['latitude'] = filtered_df['latitude'].astype(float)
    px.set_mapbox_access_token("pk.eyJ1IjoiamVkaXhuYXZpIiwiYSI6ImNrNXR4NXBheDAzbjAza241M3hmc2tocmQifQ.ifmNsmhq7kjoFWkf3jHgAg")
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color="UFO_shape", text='description', zoom=1)
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        height=800,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    fig.update_layout(mapbox_style="carto-positron")

    return fig


def piechart(shape):
    fig = px.pie(data_viz3, values=ufo_count.values, names=ufo_count.index,
                 title='Shapes of UFOs', color_discrete_sequence=px.colors.sequential.Jet)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


# Static bar Chart
fig1 = go.Figure(data=[
    go.Bar(name='us', x=year, y=us_data['Count']),
    go.Bar(name='ca', x=year, y=ca_data['Count']),
    go.Bar(name='au', x=year, y=au_data['Count']),
    go.Bar(name='gb', x=year, y=gb_data['Count'])
])

fig1.update_layout(yaxis=dict(title='UFO Sightings'), barmode='stack',
                   font=dict(family="Courier New, monospace",
                             size=22,
                             color="#7f7f7f"))

#Tab Styling

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#40e0d0',
    'color': 'blue',
    'padding': '6px'
}

app.layout = html.Div([html.Div(
    style={'background-image': 'url("assets/ufo1.jpg")'},
    id="root",
    children=[
    html.Div(
        id="header",
        children=[
            html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
            html.H4(children="UFO Sightings Across the Globe"),
            html.Br(),html.Br(),html.Br(),html.Br()

        ], style={'color': '#40e0d0', 'textAlign':'left'}
    ),
    dcc.Tabs(id="tabs", value='Tab1', children=[
        dcc.Tab(label='UFO Sightings',
                id='tab1',
                value='Tab1',
                style=tab_style,
                selected_style=tab_selected_style,
                children =[html.Div(
                id="app-container",
                children=[
                    html.Div(
                        id="left-column",
                        children=[
                               html.Div(
                                id="slider-container",
                                children=[
                                    html.P(
                                        id="slider-text",
                                        children="Drag the slider to change the year:",
                                    ),
                                    dcc.Slider(
                                        id="years-slider",
                                        min=min(YEARS),
                                        max=max(YEARS),
                                        value=min(YEARS),
                                        marks={
                                            str(year): {
                                                "label": str(year),
                                                "style": {"color": "#7fafdf"},
                                            }
                                            for year in YEARS
                                        },
                                    ),
                                ],
                            ),
                            html.Div(
                                id="map-container",
                                children=[
                                    html.P(
                                        "Number of UFO sightings \
                                        in year {0}".format(
                                            min(YEARS)
                                        ),
                                        id="map-title",
                                    ),
                                    html.Div(id='text-content'),
                                    # dcc.Graph(id='UFO_map'),
                                    dcc.Graph(
                                        id="UFO_map"
                                    ),
                                    html.P(
                                        "Shape of UFO's",
                                    id="map-title1",
                                    ),
                                    dcc.Graph(id='bar_chart', figure=fig1)
                                ], style={'color': '#40e0d0'},
                            ),
                        ],
                ),
            ],
        )]),
        dcc.Tab(label='UFO Shapes',
                id='tab2',
                value= 'Tab2',
                style=tab_style,
                selected_style=tab_selected_style,
                children=[html.Div([
    dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': i, 'value': i} for i in country],
                multi=True,
                value = list(['us'])
            ),
    dcc.Checklist(
                id='shape-button',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=list(['cylinder']),
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(id='text-content1'),
    dcc.Graph(id='UFO_map1'),
    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
    dcc.Graph(id ='shape_chart')])])
        ])
    ])])



# App layout
@app.callback(Output("map-title", "children"), [Input("years-slider", "value")])
def update_map_title(year):
    return "Number of UFO Sightings in the year {0}".format(
        year
    )
@app.callback(Output('UFO_map', 'figure'), [Input('years-slider', 'value')])
def update_figure(selected_year):
    return MAP(selected_year)
@app.callback(Output('text-content', 'children'), [Input('UFO_map', 'hoverData')])
def update_text_map1(hoverData):
    if hoverData is not None:
        text = hoverData['points'][0]['text']
        return html.H5('UFO Description: ' + text, style={'color': 'white', 'fontsize': 20})
@app.callback(
    [Output('UFO_map1', 'figure'),
    Output('shape_chart','figure')],
    [Input('country-dropdown', 'value'),
    Input('shape-button', 'value')])
def update_figure(country, shape):
    XY = list(country)
    return (plot_1(XY,shape), piechart(shape))
@app.callback(Output('text-content1','children'),[Input('UFO_map1','hoverData')])
def update_text_map2(hoverData1):
    if hoverData1 is not None:
        text = hoverData1['points'][0]['text']
        return html.H4('UFO Description: ',text,style={'color': 'red', 'fontSize': 18})

if __name__ == "__main__":
    app.run_server(debug=True)