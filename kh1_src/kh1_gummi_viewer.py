from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def obj_to_mesh3d(d):
    n = {
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        58: np.array([1, 1.5, 0.5]),
    }
    for i in range(96):
        try:
            df = pd.read_csv(f"assets/gummi/gumi-s0-{i}.obj", header=None, delimiter=" ")
            v = df[df[0] == "v"][[1, 2, 3]].astype(float).to_numpy() / 200 + (n[i] if i in n else 0.5)
            f = df[df[0] == "f"][[1, 2, 3]].map(lambda x: int(x.split("/")[0])).astype(int).to_numpy() - 1
            r = np.identity(3)
            b = 0
            if i == 0x01 or i == 0x02 or i == 0x03:
                r = np.array([
                    [0, -1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]
                ])
                b = np.array([2, 2, 0])
            if i == 0x04:
                r = np.array([
                    [0, -1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]
                ])
                b = np.array([1, 1, 0])
            if i == 0x0A or i == 0x0B:
                r = np.array([
                    [0, 0, -1],
                    [0, 1, 0],
                    [1, 0, 0],
                ])
                b = np.array([1, 0, 0])
            if i == 0x21 or i == 0x22:
                r = np.array([
                    [0, 1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]
                ])
                b = np.array([0, 1, 0])
            if i == 0x29:
                r = np.array([
                    [0, 1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]
                ])
                b = np.array([0, 1, 0])
            if i == 0x2A:
                r = np.array([
                    [0, 1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]
                ])
                b = np.array([0, 1, 0])
            if i == 0x3A:
                r = np.array([
                    [0, 1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]
                ])
                b = np.array([-1, 2, 0])
            v = v @ r.T + b
            d[i+1] = {"v": v, "f": f}
        except:
            continue

def viewer_callback(idx):
    kh1 = utils.kh1
    rd = {
        0: [1, 0, 0],
        1: [-1, 0, 0],
        4: [0, 1, 0],
        5: [0, -1, 0],
        2: [0, 0, 1],
        3: [0, 0, -1],
    }
    d = {}
    obj_to_mesh3d(d)
    fig = go.Figure()
    for i in range(kh1.gummiships[idx].blockcount.value):
        block = kh1.gummiships[idx].blocks[i]
        color = block.colors[block.color.value]
        if block.id.value in d:
            r = np.identity(3)
            b = 0
            if block.r.value & ~0x1000 == 0x0412:
                r = np.array([
                    [0, 0, 1],
                    [0, 1, 0],
                    [-1, 0, 0]
                ])
                b = np.array([0, 0, 1])
            if block.r.value & ~0x1000 == 0x0124:
                r = np.array([
                    [0, 0, 1],
                    [0, 1, 0],
                    [-1, 0, 0]
                ])
                b = np.array([0, 0, 1])
            if block.r.value & ~0x1000 == 0x0314:
                r = np.array([
                    [-1, 0, 0],
                    [0, 1, 0],
                    [0, 0, -1]
                ])
                b = np.array([1, 0, 1])
            if block.r.value & ~0x1000 == 0x0305:
                r = np.array([
                    [0, 0, -1],
                    [0, 1, 0],
                    [1, 0, 0]
                ])
                b = np.array([1, 0, 0])
            if block.r.value & ~0x1000 == 0x0431:
                r = np.array([
                    [-1, 0, 0],
                    [0, 1, 0],
                    [0, 0, -1]
                ])
                b = np.array([1, 0, 1])
            if block.r.value & ~0x1000 == 0x0034:
                r = np.array([
                    [0, 0, -1],
                    [0, 1, 0],
                    [1, 0, 0]
                ])
                b = np.array([1, 0, 0])
            if block.r.value & ~0x1000 == 0x0204:
                r = np.array([
                    [0, 0, -1],
                    [1, 0, 0],
                    [0, -1, 0]
                ])
                b = np.array([1, 0, 1])
            if block.r.value & ~0x1000 == 0x0215:
                r = np.array([
                    [0, 0, 1],
                    [-1, 0, 0],
                    [0, -1, 0]
                ])
                b = np.array([0, 1, 1])
            if block.r.value & ~0x1000 == 0x0241:
                r = np.array([
                    [1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]
                ])
                b = np.array([0, 1, 0])
            if block.r.value & ~0x1000 == 0x0042:
                r = np.array([
                    [1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]
                ])
                b = np.array([0, 1, 0])
            if block.r.value & ~0x1000 == 0x0143:
                r = np.array([
                    [1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]
                ])
                b = np.array([0, 1, 0])
            if block.r.value & ~0x1000 == 0x0053:
                r = np.array([
                    [1, 0, 0],
                    [0, 0, 1],
                    [0, -1, 0]
                ])
                b = np.array([0, 0, 1])
            v = d[block.id.value]["v"]
            v = v @ r.T + b
            fig.add_trace(
                go.Mesh3d(
                    x=v[:,0]+block.x.value,
                    y=v[:,1]+block.y.value,
                    z=v[:,2]+block.z.value,
                    i=d[block.id.value]["f"][:,0],
                    j=d[block.id.value]["f"][:,1],
                    k=d[block.id.value]["f"][:,2],
                    color=color,
                )
            )
        else:
            fig.add_trace(
                go.Mesh3d(
                    x=np.array([0,1,0,0,1,1,0,1])+block.x.value,
                    y=np.array([0,0,1,0,1,0,1,1])+block.y.value,
                    z=np.array([0,0,0,1,0,1,1,1])+block.z.value,
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

# 0x20 0x14 normal
# 0x24 0x11 left
# 0x25 0x10 right
# 0x21 0x15 back
# 0x50 0x12 up
# 0x40 0x13 down
# 0x30 0x15 up up or down down
# 0x12 0x14 tilt left
# 0x03 0x14 tilt right
# 0x31 0x14 upside down (tilt twice)
# 0x04 0x12 left then up
# 0x14 0x13 left then down
# 0x34 0x10 left then up up or down down
