import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dataprep as prep

flag_colors = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"]

data = prep.open_data()
groups = prep.groups


def bar_repartition(title="", log=False, f=lambda x: x, width=None, height=700):
    country_counts = data["counts"]

    fig = go.Figure()
    for i, g in enumerate(groups):
        fig.add_trace(
            go.Bar(
                x=country_counts.CountryName,
                y=f(country_counts[g]),
                name=g,
                text=country_counts[g],
                marker_color=flag_colors[i],
            ),
        )

    fig.update_layout(
        title=title,
        barmode="stack",
        yaxis={"categoryorder": "category ascending"},
        width=width,
        height=height,
    )
    fig.update_yaxes(type="log" if log else "linear")
    return fig


def map_repartition(title="", f=lambda x: x, width=None, height=800):
    country_counts = data["counts"]
    N = country_counts.N

    fig = go.Figure()

    for i, g in enumerate(groups):
        print(g, groups[:i], f(N - country_counts[groups[:i]].sum(axis=1)))
        fig.add_trace(
            go.Scattergeo(
                text=country_counts[g],
                name=g,
                locationmode="country names",
                locations=country_counts[[g, "CountryName"]].CountryName,
                marker={
                    "size": f(N - country_counts[groups[:i]].sum(axis=1)),
                    "color": flag_colors[i],
                    "line_width": 0,
                },
            )
        )
    fig.update_layout(
        title=title,
        geo=go.layout.Geo(
            projection={"type": "hammer", "scale": 1.5},
            scope="europe",
            landcolor="rgb(229, 229, 229)",
            coastlinecolor="#ffffff",
            resolution=50,
            center={"lon": 7.766463, "lat": 48.593740},
        ),
        width=width,
        height=height,
    )
    return fig


def map_heatmap():
    fig = go.Figure()

    return fig
