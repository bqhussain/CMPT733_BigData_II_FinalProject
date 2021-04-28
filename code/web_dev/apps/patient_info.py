import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
from app_temp import app
from sqlalchemy import create_engine, text
import plotly.graph_objects as go
import psycopg2

engine = create_engine(
        'postgresql+psycopg2://postgres:cmpt733db@mimic-cmpt733.cfynl4oqowhh.us-east-1.rds.amazonaws.com:5432/postgres')
engine.connect()
patient_data = pd.read_sql_table('task1', engine)
print("patient_info")
print(patient_data.info())
params = patient_data['icustay_id'].tolist()
last_click = 0
def clean_age(age):
  if age == 300:
    return 90
  elif age > 300:
    dif = age - 300
    age = 90 + dif
    return age
  elif age == 0:
    return 54
  return age

#***html layout***
layout = html.Div([
    html.Label(id="metric-select-title", children="Select ICU Stay ID of Patient"),
    dbc.InputGroup(
        [
            dcc.Dropdown(
                id="metric-select-dropdown",
                options=list(
                    {"label": param, "value": param} for param in params[1:]
                ),
                value=params[1],
            ),
            dbc.InputGroupAddon(html.Button("Search", id="search_btn"), 
                                addon_type="append", style={'margin-left': '5px'}),
        ],
        className="",
        style={'margin-top': '2px'}
    ),

    html.Div([
        dbc.InputGroup([
            dbc.InputGroupAddon("ICU Stay ID", addon_type="prepend"),
                                dcc.Input(
                                    id="id_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Gender", addon_type="prepend"),
                                dcc.Input(
                                    id="gen_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Ethnicity", addon_type="prepend"),
                                dcc.Input(
                                    id="eth_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Age", addon_type="prepend"),
                                dcc.Input(
                                    id="age_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Weight (kg)", addon_type="prepend"),
                                dcc.Input(
                                    id="wei_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Insurance", addon_type="prepend"),
                                dcc.Input(
                                    id="ins_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Diagnosis", addon_type="prepend"),
                                dcc.Input(
                                    id="dia_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("Admission Type", addon_type="prepend"),
                                dcc.Input(
                                    id="adm_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
        dbc.InputGroup([
            dbc.InputGroupAddon("First Careunit", addon_type="prepend"),
                                dcc.Input(
                                    id="car_out",
                                    placeholder="NAN",
                                    readOnly=True,
                                    style={"width": "80%"}
                                ),
        ]),
    ], className="patient_demo"),
    html.Div(id='los', children=[
        html.Div(
            id="card-2",
            children=[
                html.P("Mortality Percentage in Hospital"),
                daq.Gauge(
                    id="mor_hosp",
                    max=100,
                    min=0,
                    units="%",
                    color="#87ceeb",
                    size=300,
                    showCurrentValue=True,
                ),
            ],
            className="col-md-6",
        ),
        html.Div(
            id="card-2",
            children=[
                html.P("Mortality Percentage in ICU"),
                daq.Gauge(
                    id="mor_icu",
                    max=100,
                    min=0,
                    units="%",
                    color="#87ceeb",
                    size=300,
                    showCurrentValue=True,
                ),
            ],
            className="col-md-6",
        ),
    ], className="row"),
    html.Div(id='mor', children=[
        html.Div(
            id="card-2",
            children=[
                html.P("Probability of Length of Stay > 3 Days"),
                daq.Gauge(
                    id="los_3",
                    max=100,
                    min=0,
                    units="%",
                    color="#87ceeb",
                    size=300,
                    showCurrentValue=True,
                ),
            ],
            className="col-md-6",
        ),
        html.Div(
            id="card-2",
            children=[
                html.P("Probability of Length of Stay > 7 Days"),
                daq.Gauge(
                    id="los_7",
                    max=100,
                    min=0,
                    units="%",
                    color="#87ceeb",
                    size=300,
                    showCurrentValue=True,
                ),
            ],
            className="col-md-6",
        ),
    ], className="row"),
])


#***callback***
@app.callback(
    [
        Output(component_id="id_out", component_property="value"),
        Output(component_id="gen_out", component_property="value"),
        Output(component_id="eth_out", component_property="value"),
        Output(component_id="age_out", component_property="value"),
        Output(component_id="ins_out", component_property="value"),
        Output(component_id="dia_out", component_property="value"),
        Output(component_id="adm_out", component_property="value"),
        Output(component_id="car_out", component_property="value"),
        Output(component_id="wei_out", component_property="value"),
        Output(component_id="mor_hosp", component_property="value"),
        Output(component_id="mor_icu", component_property="value"),
        Output(component_id="los_3", component_property="value"),
        Output(component_id="los_7", component_property="value"),
        Output(component_id="mor_hosp", component_property="color"),
        Output(component_id="mor_icu", component_property="color"),
        Output(component_id="los_3", component_property="color"),
        Output(component_id="los_7", component_property="color")
    ],
    [
     Input(component_id="search_btn", component_property="n_clicks"),
    ],
    state=[State(component_id="metric-select-dropdown", component_property='value')]

)
def update_out(clicks, search_in):
    global last_click
    print(clicks, last_click, search_in)
    output_list = ['NAN']*17
    if clicks:
        if clicks == 1 and last_click > 0:
            last_click = 0
        print(clicks, last_click, search_in)
        if clicks-1 == last_click and search_in:
            last_click = clicks
            # get data
            if search_in:
                patient_info = patient_data.loc[patient_data['icustay_id']==int(search_in)]
                patient_info = patient_info.reset_index()
                output_list[0] = str(patient_info['icustay_id'][0])
                output_list[1] = str(patient_info['gender'][0])
                output_list[2] = str(patient_info['ethnicity'][0])
                output_list[3] = str(int(clean_age(patient_info['age'][0])))
                output_list[4] = str(patient_info['insurance'][0])
                output_list[5] = str(patient_info['diagnosis_at_admission'][0])
                output_list[6] = str(patient_info['admission_type'][0])
                output_list[7] = str(patient_info['first_careunit'][0])
                output_list[8] = str(patient_info['weight_first'][0])
                ori_color = "#87ceeb"
                alert_color = "#f45060"
                # change value of los_3
                mort_hosp = int(patient_info['mort_hosp_1'][0])
                print(patient_info['mort_hosp'][0])
                output_list[9] = mort_hosp
                # change value of los_3
                mort_icu = int(patient_info['mort_icu_1'][0])
                output_list[10] = mort_icu
                # change value of los_3
                los_3_1 = int(patient_info['los_3_1'][0])
                output_list[11] = los_3_1
                # change value of los_3
                los_7_1 = int(patient_info['los_7_1'][0])
                output_list[12] = los_7_1
                output_list[13] = ori_color
                if output_list[9] > 50:
                    output_list[13] = alert_color
                output_list[14] = ori_color
                if output_list[10] > 50:
                    output_list[14] = alert_color
                output_list[15] = ori_color
                if output_list[11] > 50:
                    output_list[15] = alert_color
                output_list[16] = ori_color
                if output_list[12] > 50:
                    output_list[16] = alert_color
                return output_list
    output_list[9] = 0
    output_list[10] = 0
    output_list[11] = 0
    output_list[12] = 0
    output_list[13] = "#87ceeb"
    output_list[14] = "#87ceeb"
    output_list[15] = "#87ceeb"
    output_list[16] = "#87ceeb"
    return output_list