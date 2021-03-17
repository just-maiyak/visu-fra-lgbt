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
app.config.suppress_callback_exceptions = False

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

dropdown_style = {
    "padding": "2px",
    "color": "#aaaaaa",
    "backgroundColor": main_colors["text"],
    "borderTop": f"1px solid {main_colors['accent']}",
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


@app.callback(
    Output("answers-heatmap", "figure"),
    Input("category-filter", "value"),
    Input("question-filter", "value"),
    Input("country-filter", "value"),
)
def update_heatmap(category, question_code, country):
    return apply_main_styles(figs.answers_heatmap(category, question_code, country))


answers_heatmap = apply_main_styles(
    figs.answers_heatmap("daily_life", "b1_c", "France")
)

# Layout declaration
app.layout = dhc.Div(
    style={"backgroundColor": main_colors["background"]},
    children=[
        dhc.H1(
            "EU-FRA LGBT Survey from 2021",
            style={"textAlign": "center", "color": main_colors["text"]},
        ),
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
                "background": main_colors["background"],
            },
            style=tabs_styles,
        ),
        dhc.Div(
            id="main-tabs-content",
            children=[
                dhc.Div(
                    style={"backgroundColor": main_colors["background"]},
                    children=[
                        dhc.Div(
                            style={"backgroundColor": main_colors["background"]},
                            children=[
                                dcc.Dropdown(
                                    id="country-filter",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in figs.countries_polled
                                    ],
                                    value="France",
                                    style=dropdown_style,
                                ),
                                dcc.Dropdown(
                                    id="category-filter",
                                    options=[
                                        {"label": v, "value": k}
                                        for k, v in prep.category_map.items()
                                    ],
                                    value="daily_life",
                                    style=dropdown_style,
                                ),
                                dcc.Dropdown(
                                    id="question-filter", style=dropdown_style
                                ),
                            ],
                        ),
                        dhc.Div(
                            [
                                dcc.Graph(id="answers-heatmap", figure=answers_heatmap),
                            ]
                        ),
                    ],
                )
            ],
        ),
    ],
)


@app.callback(Output("main-tabs-content", "children"), Input("main-tabs", "value"))
def main_tab_render(tab):
    if tab == "overview":
        ov = dhc.Div(
            style={"backgroundColor": main_colors["background"]},
            children=[
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
        return dhc.Div(
            style={"backgroundColor": main_colors["background"]},
            children=[
                dhc.Div(
                    style={"backgroundColor": main_colors["background"]},
                    children=[
        dhc.H2(
            "Poll questions/answers explorer",
            style={"color": main_colors["text_sub"], "textAlign": "center"},
        ),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": i, "value": i} for i in figs.countries_polled
                            ],
                            value="France",
                            style=dropdown_style,
                        ),
                        dcc.Dropdown(
                            id="category-filter",
                            options=[
                                {"label": v, "value": k}
                                for k, v in prep.category_map.items()
                            ],
                            value="daily_life",
                            style=dropdown_style,
                        ),
                        dcc.Dropdown(id="question-filter", style=dropdown_style),
                    ],
                ),
                dhc.Div(
                    [
                        dcc.Graph(id="answers-heatmap", figure=answers_heatmap),
                    ]
                ),
            ],
        )


@app.callback(
    Output("question-filter", "options"),
    Output("question-filter", "value"),
    Input("category-filter", "value"),
)
def update_question_dropdown(category):
    questions = figs.data[category][
        ["question_label", "question_code"]
    ].drop_duplicates()
    questions = questions.rename(
        columns={"question_label": "label", "question_code": "value"}
    )
    return questions.to_dict("records"), questions["value"][0]


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, port=6969)
