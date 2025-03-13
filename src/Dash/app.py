# This is some example code that I found from the dash github.
# I will follow this as a tutorial to get the base set up

from dash import Dash, html, dcc
import plotly.express as px
# The library used to display the maps is plotly graph_objects
import geopandas
import plotly.express as px
import pandas as pd

app = Dash()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

#These are the lines responsible for instantiating the graph

data = geopandas.read_file("../../data/raw/Neighborhood_Map_Atlas_Districts.geojson")

fig_map = px.choropleth_mapbox(
    data,
    geojson=data.geometry,
    locations=data.index,  # Column in gdf to use for coloring
    mapbox_style="carto-positron",
    center={"lat": data.geometry.centroid.y.mean(), "lon": data.geometry.centroid.x.mean()},
    opacity=0.5,
    zoom = 10,
    labels={'value': 'Value'}
)

fig_map.update_geos(
    resolution=50,
    scope = 'usa',
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue"
)

fig_map.update_layout(height=600,width=400, margin={"r":0,"t":0,"l":0,"b":0})


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph2',
        figure=fig_map
    )
])

if __name__ == '__main__':
    app.run(debug=True)