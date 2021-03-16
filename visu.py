import dash
import dash_core_components as dcc
import dash_html_components as dhc
import plotly.express as px

import dataprep as prep

# Styling
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__, url_base_pathname="/vfl/", external_stylesheets=external_stylesheets
)
colors = {"background": "#201f25", "text": "#f8f9f1"}

# Figures declaration
groups = prep.groups

country_counts = prep.open_data()["counts"]

fig = px.bar(
    country_counts,
    y="CountryName",
    x=groups,
)
fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
)

app.layout = dhc.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        dhc.H1(
            "EU-FRA LGBT Survey from 2021",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dhc.Div("Subtitle"),
        dcc.Graph(
            id="Polled countries repartition",
            figure=fig,
            style={"textAlign": "center", "color": colors["text"]},
        ),
    ],
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, port=6969)
