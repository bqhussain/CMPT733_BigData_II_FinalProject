import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
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
last_click = 0
length_out = 13
search_input = 275642
output_list = ['NAN']*length_out
# init figure los 3
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Probability of Length of Stay > 3 Days", 'font': {'size': 20}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "lightblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",}))

fig.update_layout(width=600, height=400)

output_list[9] = fig
# init figure los 7
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Probability of Length of Stay > 7 Days", 'font': {'size': 20}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "lightblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",}))

fig.update_layout(width=600, height=400)

output_list[10] = fig
# init figure Mortality in Hospital
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Mortality Percentage in Hospital", 'font': {'size': 20}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "lightblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",}))

fig.update_layout(width=600, height=400)

output_list[11] = fig
# init figure Mortality in ICU
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Mortality Percentage in ICU", 'font': {'size': 20}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "lightblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",}))

fig.update_layout(width=600, height=400)

output_list[12] = fig
output_list_ori = output_list

# function to normalize age
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
    html.H1(id='title', style={'text-align': 'center', 'color':'white', 'background-color':'#D3D3D3', 'border-radius':'25px'}, children='Prediction of Mortality Rate and Length of Stay for ICU Patients'),
    html.Div(id="hidden-div", style={"display":"none"}),
    dbc.InputGroup(
        [
            dbc.Input(id="search_in", placeholder="ICU Stay ID (263738, 226241, 275083...)", value=search_input, style={"width": "50%"}),
            dbc.InputGroupAddon(dbc.Button("Search", color="primary", 
                                        className="mr-1", id="search_btn"), 
                                addon_type="append"),
        ],
        className="mb-3",
        style={'margin-top': '10px'}
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
    ]),
    html.Div(id='div_pat_1', children=[
            html.Div(id='div_pat_l', children=[
                dcc.Graph(id='mor_hosp'),
            ], className="col-md-6"),
            html.Div(id='pat_l', children=[
                dcc.Graph(id='mor_icu'),
            ], className="col-md-6"),
    ], className="row"),
    html.Div(id='mor', children=[
            html.Div(id='div_pat_r', children=[
                dcc.Graph(id='los_3'),
            ], className="col-md-6"),
            html.Div(id='pat_r', children=[
                dcc.Graph(id='los_7'),
            ], className="col-md-6"),
    ], className="row"),
  
])

#***callback***
@app.callback(
    [Output(component_id="id_out", component_property="value"),
    Output(component_id="gen_out", component_property="value"),
    Output(component_id="eth_out", component_property="value"),
    Output(component_id="age_out", component_property="value"),
    Output(component_id="ins_out", component_property="value"),
    Output(component_id="dia_out", component_property="value"),
    Output(component_id="adm_out", component_property="value"),
    Output(component_id="car_out", component_property="value"),
    Output(component_id="wei_out", component_property="value"),
    Output(component_id="los_3", component_property="figure"),
    Output(component_id="los_7", component_property="figure"),
    Output(component_id="mor_hosp", component_property="figure"),
    Output(component_id="mor_icu", component_property="figure")
],
    [Input(component_id="search_btn", component_property="n_clicks"),
     Input(component_id="search_in", component_property="value")]
)
def update_out(clicks, search_in):
    global last_click, output_list, search_input
    # update last click count
    # clicked search btn
    if clicks:
        if clicks-1 == last_click and search_input:
            last_click = clicks
            # get data
            try:
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
                # make figure for los_3
                los_3_1 = int(patient_info['los_3_1'][0])
                bar_color = "darkblue"
                if los_3_1 > 50:
                    bar_color = "#EA4043"
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value =  los_3_1,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Probability of Length of Stay > 3 Days", 'font': {'size': 20}},
                    number = {'suffix': "%"},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': bar_color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.70,
                            'value': 50}
                    },))
                fig.update_layout(width=600, height=400)
                output_list[9] = fig
                # make figure for los_7
                los_7_1 = int(patient_info['los_7_1'][0])
                bar_color = "darkblue"
                if los_7_1 > 50:
                    bar_color = "#EA4043"
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value =  los_7_1,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': " Probability of Length of Stay > 7 Days", 'font': {'size': 20}},
                    number = {'suffix': "%"},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': bar_color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.70,
                            'value': 50}
                    }))
                fig.update_layout(width=600, height=400)
                output_list[10] = fig
                # make figure for mort_hosp
                mort_hosp_1 = int(patient_info['mort_hosp_1'][0])
                bar_color = "darkblue"
                if mort_hosp_1 > 50:
                    bar_color = "#EA4043"
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value =  mort_hosp_1,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Mortality Percentage in Hospital", 'font': {'size': 20}},
                    number = {'suffix': "%"},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': bar_color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.70,
                            'value': 50}
                    }))
                fig.update_layout(width=600, height=400)
                output_list[11] = fig
                # make figure for mort_icu
                mort_icu_1 = int(patient_info['mort_icu_1'][0])
                bar_color = "darkblue"
                if mort_hosp_1 > 50:
                    bar_color = "#EA4043"
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value =  mort_icu_1,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Mortality Percentage in ICU", 'font': {'size': 20}},
                    number = {'suffix': "%"},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': bar_color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.70,
                            'value': 50}
                    })
                )
                fig.update_layout(width=600, height=400)
                output_list[12] = fig
            except:
                print('No Match ICU Stay ID')
                return output_list_ori
    return output_list