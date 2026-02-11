from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_config(encoding):
    kh1 = utils.kh1
    autolock = dcc.Dropdown(
        options=[
            {"label": "On", "value": 0},
            {"label": "Off", "value": 1},
        ],
        value=kh1.autolock.value,
        id="AutoLock",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    targetlock = dcc.Dropdown(
        options=[
            {"label": "Auto", "value": 0},
            {"label": "Manual", "value": 1},
        ],
        value=kh1.targetlock.value,
        id="TargetLock",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    camera = dcc.Dropdown(
        options=[
            {"label": "Auto", "value": 0},
            {"label": "Manual", "value": 1},
        ],
        value=kh1.camera.value,
        id="Camera",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    vibration = dcc.Dropdown(
        options=[
            {"label": "On", "value": 0},
            {"label": "Off", "value": 1},
        ],
        value=kh1.vibration.value,
        id="Vibration",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    sound = dcc.Dropdown(
        options=[
            {"label": "Stereo", "value": 0},
            {"label": "Mono", "value": 1},
        ],
        value=kh1.sound.value,
        id="Sound",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    datainstall = dcc.Dropdown(
        options=[
            {"label": "DVD-ROM", "value": 0},
            {"label": "Hard Drive", "value": 1},
        ],
        value=kh1.datainstall.value,
        id="DataInstall",
        disabled=not (kh1.fm or encoding=="Japanese"),
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    difficulty = dcc.Dropdown(
        options=[
            {"label": "Normal", "value": 0},
            {"label": "Expert", "value": 1},
        ] if not kh1.fm else [
            {"label": "Beginner", "value": 0},
            {"label": "Standard", "value": 1},
            {"label": "Proud", "value": 2},
        ],
        value=kh1.difficulty.value,
        id="Difficulty",
        disabled=not kh1.fm and encoding=="Japanese",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([dcc.Markdown("Auto Lock:"), autolock]),
        html.Div([dcc.Markdown("Target Lock:"), targetlock]),
        html.Div([dcc.Markdown("Camera:"), camera]),
        # html.Div([dcc.Markdown("Unknown:"), None]),
        html.Div([dcc.Markdown("Vibration:"), vibration]),
        html.Div([dcc.Markdown("Sound:"), sound]),
        html.Div([dcc.Markdown("Data Install:"), datainstall]),
        html.Div([dcc.Markdown("Difficulty:"), difficulty]),
    ])

@callback(
    Output("DataInstall", "value"),
    Output("Difficulty", "value"),
    Input("AutoLock", "value"),
    Input("TargetLock", "value"),
    Input("Camera", "value"),
    Input("Vibration", "value"),
    Input("Sound", "value"),
    Input("DataInstall", "value"),
    Input("Difficulty", "value"),
    State("Encoding", "value"),
)
def config_callback(
    autolock,
    targetlock,
    camera,
    vibration,
    sound,
    datainstall,
    difficulty,
    encoding
):
    kh1 = utils.kh1
    try:
        kh1.autolock.value = autolock
        kh1.targetlock.value = targetlock
        kh1.camera.value = camera
        kh1.vibration.value = vibration
        kh1.sound.value = sound
        if kh1.fm:
            kh1.datainstall.value = datainstall
            kh1.difficulty.value = difficulty
        else:
            kh1.datainstall.value = datainstall if encoding == "Japanese" else difficulty
            kh1.difficulty.value = difficulty if encoding == "International" else datainstall
        return kh1.datainstall.value, kh1.difficulty.value
    except:
        pass
