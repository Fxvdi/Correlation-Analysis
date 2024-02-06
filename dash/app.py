# importing the required libraries
from dash import Dash, html, dcc
from graphs import *
# initialising the app
app = Dash(__name__)

# defining the layout of the app
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='./assets/styles.css'  # path to the css file
    ),
    # heading of the app
    html.H1("GDP vs. Organized Criminality"),
    # visualizations
    dcc.Graph(figure=bars("highest_gdp")),
    dcc.Graph(figure=bars("lowest_gdp")),
    dcc.Graph(figure=gdp_continent()),
    dcc.Graph(figure=gdp_globe()),
    dcc.Graph(figure=bars("highest_crime")),
    dcc.Graph(figure=bars("lowest_crime")),
    dcc.Graph(figure=criminality_map("crime")),
    dcc.Graph(figure=criminality_map("resilience")),
    dcc.Graph(figure=correlation_scatter()),
    dcc.Graph(figure=crime_scatter()),
    dcc.Graph(figure=correlation_matrix())
])

# running the app
if __name__ == '__main__':
    app.run(debug=True)
