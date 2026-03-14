from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils
import numpy as np
import plotly.graph_objects as go


def viewer_callback(idx):
    kh1 = utils.kh1
    #print(kh1.gummiships[idx].name.decode("kh1us"))
    fig = go.Figure()
    for i in range(kh1.gummiships[idx].blockcount.value):
        block = kh1.gummiships[idx].blocks[i]
        color = ["lightgray", "yellow", "orange", "red"][block.color]
        fig.add_trace(
            go.Mesh3d(
                x=np.array([0,1,0,0,1,1,0,1])+block.x,
                y=np.array([0,0,1,0,1,0,1,1])+block.y,
                z=np.array([0,0,0,1,0,1,1,1])+block.z,
                i=[0,0,1,1,0,2,1,5,2,2,3,3],
                j=[1,1,2,3,2,3,4,4,4,6,5,6],
                k=[2,3,4,5,3,6,5,7,7,7,7,7],
                color=color,
            )
        )
    fig.update_layout(
        scene=dict(
            aspectmode="data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return html.Div([
        dcc.Graph(
            figure=fig,
            style={"height": "500"},
        ),
    ])

def create_gummi_ship_viewer(idx):
    return html.Div([
        html.H1("KH1 Gummi Ship Viewer"),
        viewer_callback(idx),
    ])
