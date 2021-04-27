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

engine = create_engine('postgresql+psycopg2://postgres:cmpt733db@mimic-cmpt733.cfynl4oqowhh.us-east-1.rds.amazonaws.com:5432/postgres')
engine.connect()

# GRAPH TITLE: Total Organism Occurrence in Patients
plot_one = pd.read_sql_table('PLOT_ONE', engine)

one = px.bar(plot_one, 
             y='ORGANISM NAME', 
             x='ORGANISM OCCURRENCE',
             color_discrete_sequence=['#3366CC']*len(plot_one), 
             orientation='h', height=600)
one.update_traces(textposition='outside')
one.update_layout(uniformtext_minsize=8,
                  uniformtext_mode='hide',
                  title_x=0.5, height=600)

# GRAPH TITLE: Percentage of Distinct Specimens Collected
plot_three = pd.read_sql_table('PLOT_THREE', engine)

three = px.pie(plot_three,
               values='SPECIMEN TYPE PERCENTAGE',
               names='SPECIMEN TYPE',
               color='SPECIMEN TYPE',
               color_discrete_map={'URINE': 'darkblue',
                                 'SPUTUM': 'skyblue',
                                 'BLOOD CULTURE': 'royalblue',
                                 'SWAB': 'lightcyan',
                                 'CATHETER TIP-IV': 'aliceblue',
                                 'BRONCHOALVEOLAR LAVAGE': 'blue',
                                 'TISSUE': 'deepskyblue',
                                 'ABSCESS': 'midnightblue',
                                 'PERITONEAL FLUID': 'cyan',
                                 'OTHERS': 'powderblue'})

# GRAPH TITLE: Count of Patients distinguished by Genders for Categorized Diagnosis
plot_four = pd.read_sql_table('PLOT_FOUR', engine)

four = px.bar(plot_four,
              y="DIAGNOSIS",
              x=["MALE", "FEMALE"],
              height=600,
              color_discrete_map={'MALE': 'royalblue', 'FEMALE': 'skyblue'})
four.update_layout(xaxis_title='NUMBER OF PATIENTS',
                   legend_title='GENDER',
                   height=600)

# GRAPH TITLE: Interpretation Patterns for Antibiotics Susceptibility against Top Five Organisms
plot_five = pd.read_sql_table('PLOT_FIVE', engine)
five = px.sunburst(plot_five,
                   path=['ORGANISM NAME', 'ANTIBIOTIC NAME', 'INTERPRETATION'],
                   values='SUBJECT_ID',
                   width=1000,
                   height=1000,
                   color_continuous_scale='blues')

#GRAPH TITLE: Actual vs Predicted Antibiotic Effectiveness
plot_six = pd.read_sql_table('PLOT_SIX', engine)

six = px.line(plot_six, x="Antibiotic", y=plot_six.columns,
              hover_data={"Antibiotic": ""})
six.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")

six.update_layout(xaxis_title='ANTIBIOTIC',
                  yaxis_title='LABEL',
                  legend_title='VARIABLE')

#***lay out
layout = html.Div(id="top-section-container",
                    children=[
                        html.H1(id='', style={'text-align': 'center', 'color':'white', 'background-color':'#D3D3D3', 'border-radius':'25px'}, children='Prediction of Antibiotic Effectiveness'),
                        html.Div(id='div_1', children=[
                            html.H2(id='header', style={'text-align': 'center', 'color':'darkblue'}, children='Total Organism Occurrence in Patients'),
                            dcc.Graph(
                            id='g1',
                            figure=one
                        ),
                        ]),
                        html.Div(id='div_2', children=[
                            html.H2(id='header', style={'text-align': 'center', 'color':'darkblue'}, children='Percentage of Distinct Specimens Collected'),
                            dcc.Graph(
                            id='g2',
                            figure=three
                        ),
                        ]),
                        html.Div(id='div_3', children=[
                            html.H2(id='header', style={'text-align': 'center', 'color':'darkblue'}, children='Count of Patients distinguished by Genders for Categorized Diagnosis'),
                            dcc.Graph(
                            id='g3',
                            figure=four
                        ),
                        ]),
                        html.Div(id='div_4', children=[
                            html.H2(id='header', style={'text-align': 'center', 'color': 'darkblue'},
                                    children='Interpretation Patterns for Antibiotics Susceptibility against Top Five Organisms'),
                            dcc.Graph(
                                id='g4',
                                figure=five,
                            ),
                        ]),
                        html.Div(id='div_5', children=[
                            html.H2(id='header', style={'text-align': 'center', 'color': 'darkblue'},
                                    children='Actual vs Predicted Antibiotic Effectiveness'),
                            dcc.Graph(
                                id='g5',
                                figure=six
                            ),
                        ]),
                    ]
        )
