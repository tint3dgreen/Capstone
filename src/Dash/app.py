# This is some example code that I found from the dash github.
# I will follow this as a tutorial to get the base set up

from dash import Dash, html, dcc
import plotly.express as px
# The library used to display the maps is plotly graph_objects
import geopandas
import plotly.express as px
import pandas as pd
from matplotlib.pyplot import title

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

data = geopandas.read_file("../../data/processed/q1Map_in.geojson",index=True)
income_data = geopandas.read_file("../../data/processed/q2Map_in.geojson",index=True)

fig_map = px.choropleth_mapbox(
    data,
    geojson=data.geometry,
    color="Ratio_Under_35",
    locations=data.index,  # Column in gdf to use for coloring
    mapbox_style="carto-positron",
    center={"lat": data.geometry.centroid.y.mean(), "lon": data.geometry.centroid.x.mean()},
    opacity=0.5,
    zoom = 10,
    range_color=(data["Ratio_Under_35"].min(),data["Ratio_Under_35"].max()),
    color_continuous_scale="rdylgn",
    labels={'value': 'Value'}
)

fig_map_base = px.choropleth_mapbox(
    data,
    geojson=data.geometry,
    locations=data.index,  # Column in gdf to use for coloring
    mapbox_style="carto-positron",
    center={"lat": data.geometry.centroid.y.mean(), "lon": data.geometry.centroid.x.mean()},
    opacity=0.5,
    zoom = 10,
    range_color=(0,1),
    color_continuous_scale="Viridis",
    labels={'value': 'Value'}
)

#Graph of Mean Yearly Household Income by Neighborhood
fig_map_income = px.choropleth_mapbox(
    income_data,
    geojson=data.geometry,
    color="Mean_Yearly_Income",
    locations=data.index,  # Column in gdf to use for coloring
    mapbox_style="carto-positron",
    center={"lat": data.geometry.centroid.y.mean(), "lon": data.geometry.centroid.x.mean()},
    opacity=0.5,
    zoom = 10,
    range_color=(income_data["Mean_Yearly_Income"].min(),income_data["Mean_Yearly_Income"].max()),
    color_continuous_scale="rdylgn",
    labels={'value': 'Value'}
)

piechart = px.pie(
    income_data,
    values='Total_Households',
    names= income_data['L_HOOD']
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

fig_map.update_layout(height=600,width=400, margin={"r":0,"t":0,"l":0,"b":0}, title_text="Percent of Households with affordable rent")
fig_map_base.update_layout(height=600,width=400, margin={"r":0,"t":0,"l":0,"b":0})
fig_map_income.update_layout(height=600,width=400, margin={"r":0,"t":0,"l":0,"b":0}, title_text="Average Annual Income by Neighborhood")
piechart.update_layout(height=400,width=600, margin={"r":0,"t":0,"l":0,"b":0})


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    html.Div(children='''
        lah dee dah
    '''),

    dcc.Graph(
        id='example-graph2',
        figure=fig_map
    ),
    dcc.Graph(
        id='income_graph',
        figure=fig_map_income
    ),
    dcc.Graph(
        id='example-graph3',
        figure=fig_map_base
    ),
    dcc.Graph(
        id="pop_chart",
        figure=piechart
    )
])

if __name__ == '__main__':
    app.run(debug=True)