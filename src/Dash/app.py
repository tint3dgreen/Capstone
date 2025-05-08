# This is some example code that I found from the dash github.
# I will follow this as a tutorial to get the base set up
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import geopandas
import plotly.express as px



# Dashboard initialization
external_stylesheets = ['style.css']
app = Dash(external_stylesheets=external_stylesheets)


#These are the lines responsible for instantiating the graph

data = geopandas.read_file("../../data/processed/q1Map_in.geojson",index=True)
costs = geopandas.read_file("../../data/processed/costs_in_map.geojson",index=True)


app.layout = html.Div(className = 'title',children=[
    html.H1(children='Seattle Housing Dashboard', style={'textAlign':'center'}),

    html.Div(children='''
        This is an interactive dashboard to aid in finding a neighborhood that best aligns with your financial needs.
    ''', style={'textAlign': 'center'}),

    html.Center( className='lah',
        children=[
                html.Div(children=[
                    html.Center(children=["Select Your Budget (USD/Month)"]),
                    dcc.RangeSlider(0,3500,500, value=[1000,2500], id='RangeSlider'),
                    dcc.RadioItems(id='Mode_selector', options=['Rent',"Mortgage"], value='Rent')],
                    style={'padding':10, 'flex':1, 'max-width': '25%', 'margin':'10', 'align-self':'center'}),
                html.Div(children=
                    dcc.Graph(id='graph-output-container',style={'margin-right': 'auto','margin-left': 'auto'})
                         )
        ], style={'display': 'flex', 'flexDirection': 'row','margin-right': 'auto','margin-left': 'auto', 'justify-content': 'center'}
    )
])

def calc_vals(mode):
    if mode == 'Rent':
        min_val = 0
        max_val = 4000
        marks = {0:{'label': '$0'},
                 500:{'label': '$500'},
                 1000:{'label': '$1000'},
                 1500:{'label': '$1500'},
                 2000:{'label': '$2000'},
                 2500:{'label': '$2500'},
                 3000:{'label': '$3000'},
                 3500:{'label': '$3500'},
                 4000:{'label': '$3500+'}}
        return min_val, max_val, marks
    elif mode == 'Mortgage':
        min_val = 0
        max_val = 4500
        marks = {0: {'label': '$0'},
                 1000: {'label': '$1000'},
                 1500: {'label': '$1500'},
                 2000: {'label': '$2000'},
                 2500: {'label': '$2500'},
                 3000: {'label': '$3000'},
                 3500: {'label': '$3500'},
                 4000: {'label': '$4000'},
                 4500: {'label': '$4500+'}}
        return min_val, max_val, marks

# selects the specified column range depending on the mode
def get_data(mode,range):
    if mode == 'Rent':
        print(f"range: {range}")
        cols = ["Gross_Rent_Less_Than_$500","Gross_Rent_$500-$999","Gross_Rent_$1,000-$1,499","Gross_Rent_$1,500-$1,999","Gross_Rent_$2,000-$2,499","Gross_Rent_$2,500-$2,999","Gross_Rent_$3,000-$3,499","Gross_Rent_$3,500_or_more"][range[0]//500:range[1]//500]
        print(f"cols: {cols}")
        costs['ratio'] = costs[cols].sum(axis=1) / costs["Renter_housing_units_with_gross_rent"]
        return costs
    elif mode == 'Mortgage':

        # This code is to adjust for the discrepancy with the bin size in the mortgage price data.
        # The first bins is twice as large as the other bins, so the range needs to be adjusted since the distance between points is not always 500
        if (range[0] <= 500):
            range[1] = range[1]-500
        else:
            range[0] = range[0]-500
            range[1] = range[1]-500


        print(range[0]//500,range[1]//500)
        cols = ["Owner_Costs_Less_Than_$1,000","Owner_Costs_$1,000-$1,499","Owner_Costs_$1,500-$1,999","Owner_Costs_$2,000-$2,499","Owner_Costs_$2,500-$2,999","Owner_Costs_$3,000-$3,499","Owner_Costs_$3,500-$3,999",	"Owner_Costs_$4,000_or_more"][range[0]//500:range[1]//500]
        print(cols)
        costs['ratio'] = costs[cols].sum(axis=1) / costs["Owner_housing_units_with_a_mortgage"]
        return costs


@callback(
    [Output('graph-output-container', 'figure'),
     Output('RangeSlider', 'min'),Output('RangeSlider', 'max'),Output('RangeSlider', 'marks')],
    [Input('RangeSlider', 'value'),
    Input('Mode_selector', 'value')])
def output_graph(range,mode):
    # Select the data used

    min_val, max_val, marks = calc_vals(mode)
    dat = get_data(mode,range)
    fig = px.choropleth_mapbox(
        dat,
        geojson=data.geometry,
        color="ratio",
        locations=data.index,  # Column in gdf to use for coloring
        mapbox_style="carto-positron",
        center={"lat": data.geometry.centroid.y.mean(), "lon": data.geometry.centroid.x.mean()},
        opacity=0.5,
        zoom=10,
        range_color=(dat["ratio"].min(), dat["ratio"].max()),
        color_continuous_scale="rdylgn",
        labels={'ratio': 'Percentage of households in budget'},
        hover_data='L_HOOD'
    )
    fig.update_layout(height=800,width=650)
    return fig, min_val,max_val, marks

if __name__ == '__main__':
    app.run(debug=True)