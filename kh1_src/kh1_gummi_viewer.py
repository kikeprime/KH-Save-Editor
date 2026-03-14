from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def obj_to_mesh3d(d):
    n = {0: 1, 58: np.array([1, 1.5, 0.5])}
    for i in range(96):
        try:
            df = pd.read_csv(f"assets/gummi/gumi-s0-{i}.obj", header=None, delimiter=" ")
            v = df[df[0] == "v"][[1, 2, 3]].astype(float).to_numpy() / 200 + (n[i] if i in n else 0.5)
            f = df[df[0] == "f"][[1, 2, 3]].map(lambda x: int(x.split("/")[0])).astype(int).to_numpy() - 1
            d[i+1] = {"v": v, "f": f}
        except:
            continue

def viewer_callback(idx):
    kh1 = utils.kh1
    d = {}
    obj_to_mesh3d(d)
    fig = go.Figure()
    for i in range(kh1.gummiships[idx].blockcount.value):
        block = kh1.gummiships[idx].blocks[i]
        color = ["lightgray", "yellow", "orange", "red"][block.color]
        fig.add_trace(
            go.Mesh3d(
                x=d[block.id]["v"][:,0]+block.x,
                y=d[block.id]["v"][:,1]+block.y,
                z=d[block.id]["v"][:,2]+block.z,
                i=d[block.id]["f"][:,0],
                j=d[block.id]["f"][:,1],
                k=d[block.id]["f"][:,2],
                color=color,
            ) if block.id in d else\
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
