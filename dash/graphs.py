# Description: This file contains the methods to create the graphs for the dashboard.
# It uses the pandas and plotly libraries to create the visualizations.
# The methods are then called in the app.py file to display the graphs in the dashboard.

# importing the required libraries
import pandas as pd
import plotly.express as px
import numpy as np

# reading the data
df = pd.read_excel("./data/merged_data.xlsx")
# renaming the columns
gdp_column = 'GDP, Per Capita GDP - US Dollars'
avg_gdp = 'Avg GDP'
crime = "Criminality"
#logarithmic transformation of the GDP
df['log_gdp'] = np.log(df[gdp_column])

# creating the bar chart
def create_barchart(data, color, c_range, y, x, round_values=True):
    """
    Erzeugt ein Balkendiagramm mit den übergebenen Daten.

    Parameters:
    data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    color (str): Die Farbpalette für das Diagramm.
    c_range (list): Der Farbbereich für das Diagramm.
    y (str): Die Spalte für die y-Achse im Diagramm.
    x (str): Die Spalte für die x-Achse im Diagramm.
    round_values (bool, optional): Gibt an, ob die Werte auf den Balken gerundet werden sollen. Standardmäßig True.

    Returns:
    plotly.graph_objects.Figure: Das erzeugte Balkendiagramm.
    """
    # create the bar chart
    fig = px.bar(data, x=x, y=y, color=y,  # axises and color
                 color_continuous_scale=color, range_color=c_range,  # color scale and range
                 template='plotly_dark')  # dark theme
    

    # Anzeigen der y-Werte über der Säule
    for i, wert in enumerate(data[y]):
        # Abfrage, ob die anzuzeigenden y-Werte gerundet werden sollen
        if round_values:
            text_value = str(round(wert))
        else:
            text_value = str(wert)
        # Beschriftung hinzufügen
        fig.add_annotation(x=data[x].iloc[i], y=wert,  # Position
                           text=text_value,  # Wert, welcher angezeigt werden soll
                           showarrow=False, font=dict(size=13), yshift=9)  # Schriftgröße und Abstand

    return fig


def world_map(color, scale, title):
    fig = px.choropleth(df,
                        locations='Code Value',  # Zuordnung der Länder nach ISO3
                        color=color,  # Farbskalierung
                        hover_name="Country",  # Name beim Hovern
                        color_continuous_scale=scale,  # Farbschmema
                        # Unnötige Hoverwerte entfernen
                        hover_data={
                                   gdp_column: True, "Criminality": False, "Code Value": False},
                        projection='natural earth',  # Typ der Weltkarte
                        title=title,  # Titel
                        template="plotly_dark")
    return fig


def gdp_globe():
    fig = px.choropleth(df,
                        locations='Code Value',  # Zuordnung der Länder nach ISO3
                        color="log_gdp",  # Farbskalierung
                        hover_name="Country",  # Name beim Hovern
                        color_continuous_scale="RdYlGn",  # Farbschmema
                        # Unnötige Hoverwerte entfernen
                        hover_data={gdp_column: True,
                                    "log_gdp": False, "Code Value": False},
                        projection='orthographic',  # Typ der Weltkarte
                        title='GDP per Capita by Country in USD$',  # Titel
                        template="plotly_dark")  # Design
    # Anpassen der Größe des Diagramms und der Legende
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="GDP per Capita",  # Titel der Farbskala
            # Anpassung der Werte des Achsenticks
            tickvals=np.log([100, 1000, 10000, 100000]),
            # Beschriftung des Achsenticks
            ticktext=["0.1k", "1k", "10k", "100k"]
        ))
    return fig


def gdp_continent():
    # Gruppierung der Länder nach Kontinent und zählen der Länder
    count_countries = df['Continent'].value_counts().reset_index()
    count_countries.columns = ['Continent', 'Anzahl Länder']

    # Gruppierung nach Kontinent und zusammzählen des GDP's
    count_gdp = df.groupby('Continent')[gdp_column].sum().reset_index()
    count_gdp.columns = ['Continent', 'Gesamt-GDP']

    # Merging der beidnen Dataframes nach Kontinent
    avg_continent_gdp = pd.merge(count_countries, count_gdp, on='Continent')

    # Neue Spalten mit dem durchschnitts GDP berechnen
    avg_continent_gdp['Avg GDP'] = round(
        avg_continent_gdp['Gesamt-GDP'] / avg_continent_gdp['Anzahl Länder'], 2)

    # Spalte als Variable
    avg_gdp = 'Avg GDP'

    # Aufrufen der Bar-Chart-Methode
    continent = create_barchart(avg_continent_gdp, 'viridis_r', [
        0, 50000], avg_gdp, 'Continent')

    # Titel ändern
    continent.update_layout(title="Average GDP by Continent")

    # Anzeigen des Diagramms
    return continent


def bars(type):

    if type == "highest_gdp":
        data = df.nlargest(10, gdp_column)
        fig = create_barchart(data, "viridis_r", [
                              0, 250000], gdp_column, 'Country')
        fig.update_layout(
            title=f"Top 10 Countries with the highest GDP Per Capita", yaxis_title="GDP per Capita in US$", coloraxis_colorbar_title='GDP per Capita in US$')
        return fig

    elif type == "lowest_gdp":
        data = df.nsmallest(10, gdp_column)
        fig = create_barchart(data, "solar", [300, 600], gdp_column, 'Country')
        fig.update_layout(
            title=f"Top 10 Countries with the lowest GDP Per Capita", yaxis_title="GDP per Capita in US$")
        return fig

    elif type == "highest_crime":
        highest_crime = df.nlargest(10, crime)
        fig = create_barchart(highest_crime, 'solar_r',
                              [6, 8], crime, 'Country', False)
        fig.update_layout(
            title="Top 10 Countries with the highest Organized Crime", yaxis_title="GDP per Capita in US$")
        return fig

    elif type == "lowest_crime":
        lowest_crime = df.nsmallest(10, crime)
        fig = create_barchart(lowest_crime, 'viridis',
                              [1, 3], crime, 'Country', False)
        fig.update_layout(
            title="Top 10 Countries with the lowest Organized Crime", yaxis_title="GDP per Capita in US$")
        return fig


def criminality_map(type):
    if type == "crime":
        fig = world_map("Criminality", "reds",
                              'Organized Crime by Country')
        return fig
    
    elif type == "resilience":
        fig = world_map(
            "Resilience", "teal", 'Resilience against Crime by Country')
        return fig

def correlation_scatter():
    fig = px.scatter(df,
                 y="Criminality",  # Definition y-Achse
                 x=gdp_column,  # Definition x-Achse
                 log_x=True,  # Logarithmische Werte von x
                 color="Continent",  # Farbe der Punkte nach Kontinente
                 hover_name="Country",  # Wert beim Hovern
                 title="Relation between Criminality and GDP",
                 template="plotly_dark")
    return fig

def crime_scatter():
    # Copy mit bestimmten Spalten erstellen
    crime_relation = df[["Code Value", "Criminality", "Resilience", "Country"]].copy()
    # Rang von Kriminalität (umgedreht, damit schlechter Rang auch schlecht ist)
    crime_relation['Crime_Rank'] = crime_relation['Criminality'].rank(ascending=True)
    # Rang von Resilience
    crime_relation['Resilience_Rank'] = crime_relation['Resilience'].rank(ascending=False)

    # Erstellung des Graphen
    fig = px.scatter(crime_relation,
                    y="Criminality",  # Definition y-Achse
                    x="Resilience",  # Definition x-Achse
                    hover_name="Country",  # Wert beim Hovern
                    title="Relation between Criminality and Resilience",
                    template="plotly_dark", # Dunkler Hintergrund
                    trendline="ols" # Trendlinie
                    )
    return fig

def correlation_matrix():
        # Auswahl der Spalten für die Korrelationsmatrix
    columns = ["Criminality", "Resilience", gdp_column]
    # Berechnung der Korrelation über den Spearman-Algorithmus gerundet auf zwei Nachkommastellen
    correlation_matrix = df[columns].corr(method="spearman").round(2)

    # Erstellung der Heatmap
    fig = px.imshow(correlation_matrix,
                    x=correlation_matrix.columns,
                    y=correlation_matrix.columns,
                    color_continuous_scale='RdBu',
                    range_color=[-1, 1],
                    title='Korrelationsmatrix',
                    text_auto='True',
                    template="plotly_dark")
    return fig
