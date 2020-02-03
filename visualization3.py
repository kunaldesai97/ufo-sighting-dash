import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px



# Import data and read .csv files to create Pandas DataFram
df = pd.DataFrame(columns = ['UFO_shape','country','latitude','longitude'])
path = '/home/arjun/Documents/SFU_Course_Work/Spring2020/cmpt733/blog/new_data.csv'
data = pd.read_csv(path)

# Import Styling External Sheets for HTML/CSS Web Layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Python Plots/Functions for Callbacks and Outputs:
def plot_1(country, shape):
    filtered_df = data[data.country.isin(country)]
    filtered_df = filtered_df[filtered_df.UFO_shape.isin(shape)]
    px.set_mapbox_access_token("pk.eyJ1IjoiamVkaXhuYXZpIiwiYSI6ImNrNXR4NXBheDAzbjAza241M3hmc2tocmQifQ.ifmNsmhq7kjoFWkf3jHgAg")
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color = "UFO_shape", text='description', zoom =1)
    fig.update_layout(
        title = 'Shape of UFO Sightings around the World<br>(Hover for shapes observed)',
        autosize=True,
        hovermode='closest',
        height=800,
        #showlegend = False
    )
    fig.update_layout(mapbox_style="carto-positron")
    
    return fig

def piechart(shape):
    fig = px.pie(data, values= ufo_count.values, names=ufo_count.index, 
             title='Shapes of UFOs', color_discrete_sequence = px.colors.sequential.Jet)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# Create Dash app. 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create Lists for app.callbacks, app.layout
available_indicators = data['UFO_shape'].unique()
country = data['country'].unique()
ufo_count = data['UFO_shape'].value_counts()

# Define Dash App Layout: app.layout using HTML tags.
app.layout = html.Div([
    

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
    html.Div(id='text-content'),
    dcc.Graph(id='UFO_map'),
    dcc.Graph(id ='shape_chart')
])

# Define to update Output: Graph - Map Scatter based on Inputs(Dropdown, Checklist)
@app.callback(
    [Output('UFO_map', 'figure'),
    Output('shape_chart','figure')],
    [Input('country-dropdown', 'value'),
    Input('shape-button', 'value')])

def update_figure(country, shape):
    XY = list(country)
    return (plot_1(XY,shape), piechart(shape))

@app.callback(
    Output('text-content','children'),
    [Input('UFO_map','hoverData')])

def update_text(hoverData):
    if hoverData is not None:
        text = hoverData['points'][0]['text']
        return html.H6(f'UFO Description: {text}')

if __name__ == '__main__':
    app.run_server(debug=True)