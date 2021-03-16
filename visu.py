import dash
import dash_core_components as dcc
import dash_html_components as dhc
import plotly.express as px

import dataprep as prep

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

groups = prep.groups

country_counts = prep.open_data()["counts"]

fig = px.bar(
    country_counts,
    y="CountryName",
    x=groups,
)

app.layout = dhc.Div(
    [
        dhc.H1("EU-FRA LGBT Survey from 2021"),
        dhc.Div("Subtitle"),
        dcc.Graph(id="Polled countries repartition", figure=fig),
    ]
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
