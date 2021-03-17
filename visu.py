import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
import plotly.express as px

import numpy as np

import dataprep as prep
import figures as figs

# Styling
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__, url_base_pathname="/vfl/", external_stylesheets=external_stylesheets
)
main_colors = {
    "background": "#201f25",
    "text": "#f8f9f1",
    "text_sub": "#6a8cb4",
    "accent": "#5BA6EC",
}
# source : https://coolors.co/ff595e-ffca3a-8ac926-1982c4-6a4c93
flag_colors = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"]

tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": f"1px solid {main_colors['text_sub']}",
    "padding": "6px",
    "color": main_colors["text"],
}

tab_selected_style = {
    "borderTop": f"1px solid {main_colors['accent']}",
    "borderBottom": f"1px solid {main_colors['background']}",
    "backgroundColor": main_colors["text_sub"],
    "color": "white",
    "padding": "6px",
    "fontWeight": "bold",
}

# Figures declaration
groups = prep.groups

apply_main_styles = lambda fig: fig.update_layout(
    plot_bgcolor=main_colors["background"],
    paper_bgcolor=main_colors["background"],
    font_color=main_colors["text"],
)

bar_rep = apply_main_styles(figs.bar_repartition())
map_rep = apply_main_styles(figs.map_repartition(f=lambda x: x / 100))

app.layout = dhc.Div(
    [
        dcc.Tabs(
            id="main-tabs",
            value="overview",
            children=[
                dcc.Tab(
                    label="Overview",
                    value="overview",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Questions explorer",
                    value="questions",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
            ],
            colors={
                "primary": main_colors["text_sub"],
                "text": main_colors["text"],
                "background": main_colors["background"],
            },
            style=tabs_styles,
        ),
        dhc.Div(id="main-tabs-content"),
    ]
)


@app.callback(Output("main-tabs-content", "children"), Input("main-tabs", "value"))
def main_tab_render(tab):
    if tab == "overview":
        ov = dhc.Div(
            style={"backgroundColor": main_colors["background"]},
            children=[
                dhc.H1(
                    "EU-FRA LGBT Survey from 2021",
                    style={"textAlign": "center", "color": main_colors["text"]},
                ),
                dhc.H2(
                    "Overview of the polled population",
                    style={"color": main_colors["text_sub"], "textAlign": "center"},
                ),
                dcc.Graph(
                    id="bar-rep",
                    figure=bar_rep,
                    style={"textAlign": "center", "color": main_colors["text"]},
                ),
                dcc.Graph(
                    id="map-rep",
                    figure=map_rep,
                    style={"textAlign": "center", "color": main_colors["text"]},
                ),
            ],
        )
        return ov
    elif tab == "questions":
        return dhc.Div("test", style=tab_style)


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, port=6969)
