import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import patient_info, anit
from app_temp import app

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H3("Prediction on Antibiotics Resistance and Length of Stay for ICU Patients")
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    dbc.NavLink(html.Button( children="GITHUB"), href="https://github.com/qyune/CMPT733_BigData_II_FinalProject", id="Github-button"),
                    html.Img(id="logo", src=app.get_asset_url("sfu_bigdata_logo2.png")),
                ],
            ),
        ],
    )

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab3",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Antibiotic Effectiveness Dashboard",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Antibiotic Effectiveness Prediction",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="LOS-tab",
                        label="Mortality Rate and LOS Prediction",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        )
    ],
)

@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")]
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return [anit.layout]
    elif tab_switch == "tab2":
        return [anit.layout]
    elif tab_switch == "tab3":
        return [patient_info.layout]

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8088, debug=False)