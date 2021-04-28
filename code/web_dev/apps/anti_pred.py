import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app_temp import app
from apps.preprocess import data_process
import pickle

last_click = 0

gender_list = ['F', 'M']

ethnicity_list = ['unknown',
                  'white',
                  'asian',
                  'hispanic',
                  'black',
                  'other',
                  'native']

model_list = ['Conditions_Originating_In_The_Perinatal_Period',  # 0
              'Congenital_Anomalies',  # 1
              'Diseases_Of_The_Blood_And_Blood_Forming_Organs',  # 2
              'Diseases_Of_The_Circulatory_System',  # 3
              'Diseases_Of_The_Digestive_System',  # 4
              'Diseases_Of_The_Genitourinary_System',  # 5
              'Diseases_Of_The_Musculoskeletal_System_And_Connective_Tissue',  # 6
              'Diseases_Of_The_Nervous_System_And_Sense_Organs',  # 7
              'Diseases_Of_The_Respiratory_System',  # 8
              'Diseases_Of_The_Skin_And_Subcutaneous_Tissue',  # 9
              'Endocrine_Nutritional_Metabolic_Diseases_And_Immunity_Disorders',  # 10
              'Factors_Influencing_Health_Status',  # 11
              'Infectious_And_Parasitic_Diseases',  # 12
              'Injury_And_Poisoning',  # 13
              'Mental_Disorders',  # 14
              'Neoplasms',  # 15
              'Symptoms_Signs_And_Ill_Defined_Conditions'  # 16
              ]

organisms_list = ['STAPH AUREUS COAG +', 'STAPHYLOCOCCUS, COAGULASE NEGATIVE',
                  'STENOTROPHOMONAS (XANTHOMONAS) MALTOPHILIA', 'ESCHERICHIA COLI',
                  'STREPTOCOCCUS MILLERI GROUP', 'PSEUDOMONAS AERUGINOSA',
                  'ENTEROBACTER CLOACAE', 'KLEBSIELLA PNEUMONIAE',
                  'NON-FERMENTER, NOT PSEUDOMONAS AERUGINOSA', 'ENTEROCOCCUS SP.',
                  'ENTEROCOCCUS FAECIUM', 'PROTEUS MIRABILIS', 'KLEBSIELLA OXYTOCA',
                  'ENTEROBACTER AEROGENES', 'CITROBACTER KOSERI',
                  'ENTEROCOCCUS FAECALIS', 'MORGANELLA MORGANII',
                  'KLEBSIELLA SPECIES', 'CITROBACTER FREUNDII COMPLEX',
                  'STREPTOCOCCUS PNEUMONIAE', 'ACINETOBACTER BAUMANNII',
                  'PROVIDENCIA RETTGERI', 'BORDETELLA SPECIES', 'ENTEROBACTERIACEAE',
                  'SERRATIA MARCESCENS', 'HAFNIA ALVEI',
                  'BURKHOLDERIA (PSEUDOMONAS) CEPACIA', 'ENTEROBACTER SPECIES',
                  'POSITIVE FOR METHICILLIN RESISTANT STAPH AUREUS',
                  'PROTEUS VULGARIS', 'MORAXELLA SPECIES',
                  'BURKHOLDERIA CEPACIA GROUP', 'ENTEROBACTER ASBURIAE',
                  'BETA STREPTOCOCCUS GROUP B', 'ACINETOBACTER BAUMANNII COMPLEX',
                  'ENTEROBACTER CLOACAE COMPLEX',
                  'ABIOTROPHIA/GRANULICATELLA SPECIES', 'STREPTOCOCCUS ANGINOSUS',
                  'STREPTOCOCCUS CONSTELLATUS', 'STREPTOCOCCUS ORALIS',
                  'CITROBACTER AMALONATICUS', 'VIRIDANS STREPTOCOCCI',
                  'PROVIDENCIA STUARTII',
                  'HAEMOPHILUS INFLUENZAE, BETA-LACTAMASE POSITIVE',
                  'STAPHYLOCOCCUS SPECIES', 'STAPHYLOCOCCUS EPIDERMIDIS',
                  'STREPTOCOCCUS BOVIS ', 'GRAM NEGATIVE ROD(S)',
                  'STREPTOCOCCUS ANGINOSUS (MILLERI) GROUP', 'MORAXELLA OSLOENSIS',
                  'ALPHA STREPTOCOCCI', 'STREPTOCOCCUS VESTIBULARIS',
                  'HAEMOPHILUS INFLUENZAE', 'PASTEURELLA MULTOCIDA',
                  'STAPHYLOCOCCUS, COAGULASE NEGATIVE, PRESUMPTIVELY NOT S. SAPROPHYTICUS',
                  'KLEBSIELLA OZAENAE', 'PROVIDENCIA SPECIES', 'RALSTONIA PICKETTII',
                  'SERRATIA SPECIES', 'CITROBACTER SPECIES',
                  'BETA STREPTOCOCCUS GROUP A', 'PANTOEA SPECIES',
                  'CITROBACTER YOUNGAE', 'SERRATIA LIQUEFACIENS',
                  'GAMMA(I.E. NON-HEMOLYTIC) STREPTOCOCCUS',
                  'ENTEROCOCCUS RAFFINOSUS', 'STREPTOCOCCUS SALIVARIUS',
                  'AEROMONAS SPECIES', 'OCHROBACTRUM ANTHROPI',
                  'ENTEROCOCCUS GALLINARUM', 'STREPTOCOCCUS SPECIES',
                  'SHIGELLA FLEXNERI', 'ENTEROBACTER AGGLOMERANS',
                  'STREPTOCOCCUS SANGUIS', 'PANTOEA (ENTEROBACTER) AGGLOMERANS',
                  'LACTOBACILLUS SPECIES', 'GRAM NEGATIVE ROD #1',
                  'ENTEROCOCCUS AVIUM', 'CORYNEBACTERIUM SPECIES (DIPHTHEROIDS)',
                  'AEROMONAS HYDROPHILA', 'SERRATIA RUBIDAEA',
                  'PRESUMPTIVE STREPTOCOCCUS BOVIS',
                  'BACILLUS SPECIES; NOT ANTHRACIS', 'ENTEROBACTER SAKAZAKII',
                  'BURKHOLDERIA SPECIES', 'LISTERIA MONOCYTOGENES',
                  'ALCALIGENES XYLOSOXIDANS', 'STREPTOCOCCUS MILLERI',
                  'ACHROMOBACTER (ALCALIGENES) DENTRIFICANS',
                  'ENTEROCOCCUS CASSELIFLAVUS', 'CHRYSEOBACTERIUM MENINGOSEPTICUM',
                  'NUTRITIONALLY VARIANT STREPTOCOCCUS',
                  'ALCALIGENES (ACHROMOBACTER) SPECIES', 'PSEUDOMONAS PUTIDA ',
                  'SALMONELLA HADAR', 'KLUYVERA SPECIES', 'PSEUDOMONAS SPECIES',
                  'LEUCONOSTOC SPECIES', 'SALMONELLA ENTERITIDIS',
                  'BORDETELLA BRONCHISEPTICA', 'GRAM NEGATIVE ROD #2',
                  'CHRYSEOBACTERIUM INDOLOGENES',
                  'ACHROMOBACTER (ALCALIGENES) XYLOSOXIDANS SS DENTRIFICANS',
                  'ENTEROBACTER GERGOVIAE', 'PROTEUS VULGARIS GROUP',
                  'STAPHYLOCOCCUS LUGDUNENSIS', 'SHEWANELLA SPECIES',
                  'LECLERCIA ADECARBOXYLATA', 'SALMONELLA SPECIES',
                  'CORYNEBACTERIUM UREALYTICUM SP. NOV.', 'STAPHYLOCOCCUS HOMINIS',
                  'PSEUDOMONAS PUTIDA/FLUORESCENS', 'BETA STREPTOCOCCUS GROUP G',
                  'STREPTOCOCCUS MITIS', 'PROPIONIBACTERIUM ACNES',
                  'HAEMOPHILUS INFLUENZAE, BETA-LACTAMASE NEGATIVE',
                  'CRONOBACTER (ENTEROBACTER) SAKAZAKII',
                  'RAOULTELLA ORNITHINOLYTICA',
                  'ELIZABETHKINGIA (CHRYSEOBACTERIUM) MENIGOSEPTICA',
                  'SALMONELLA DUBLIN', 'ACINETOBACTER SP.', 'VIBRIO SPECIES',
                  'PSEUDOMONAS LUTEOLA', 'GRAM POSITIVE COCCUS(COCCI)',
                  'PSEUDOMONAS FLUORESCENS', 'ALCALIGENES FAECALIS']

layout = html.Div([
    # Manually select metrics
    html.Div(
        id="set-specs-intro-container",
        # className='twelve columns',
        children=html.P(
            "Use historical control limits to establish a benchmark, or set new values."
        ),
    ),
    html.Div(
        id="settings-menu",
        children=[
            html.Div(
                id="metric-select-menu",
                # className='five columns',
                children=[
                    html.Label(id="gender", children="Gender:"),
                    dcc.Dropdown(
                        id="gender-dropdown",
                        options=list(
                            {"label": gender, "value": gender} for gender in gender_list
                        ),
                        value=gender_list[0],
                    ),
                    html.Br(),
                    html.Label(id="age", children="Age (Years):"),
                    dcc.Input(
                        id="age-input",
                        placeholder='Enter a age...',
                        type='number',
                        style={"margin-bottom": "20px", "width": "100%",
                               "backgroundColor": "#242633",
                               "color": "white"},
                        value=28
                    ),
                    # html.Br(),
                    html.Label(id="ethnicity", children="Ethnicity:"),
                    dcc.Dropdown(
                        id="ethnicity-dropdown",
                        options=list(
                            {"label": eth, "value": eth} for eth in ethnicity_list
                        ),
                        value=ethnicity_list[0],
                    ),
                    html.Br(),
                    html.Label(id="diagnosis", children="Diagnosis:"),
                    dcc.Dropdown(
                        id="diagnosis-dropdown",
                        options=list(
                            {"label": model, "value": model} for model in model_list
                        ),
                        value=model_list[0],
                    ),
                    html.Br(),
                    html.Label(id="previous-admissions", children="Previous Admissions:"),
                    dcc.Input(
                        id="previous-admissions-input",
                        type='number',
                        style={"margin-bottom": "20px", "width": "100%",
                               "backgroundColor": "#242633",
                               "color": "white"},
                        value=1
                    ),
                    # html.Br(),
                    html.Label(id="sample-collection", children="Sample Collection Interval (Days):"),
                    dcc.Input(
                        id="sample-collection-input",
                        type='text',
                        style={"margin-bottom": "20px", "width": "100%",
                               "backgroundColor": "#242633",
                               "color": "white"},
                        value='0.1'
                    ),
                    # html.Br(),
                    html.Label(id="antibiotic", children="Antibiotic Name:"),
                    dcc.Input(
                        id="antibiotic-input",
                        type='text',
                        style={"margin-bottom": "20px", "width": "100%",
                               "backgroundColor": "#242633",
                               "color": "white"},
                        value='GENTAMICIN'
                    ),
                    # html.Br(),
                    html.Label(id="organism", children="Organism Name:"),
                    dcc.Dropdown(
                        id="organisms-dropdown",
                        options=list(
                            {"label": org, "value": org} for org in organisms_list
                        ),
                        value=organisms_list[0],
                    ),
                    html.Br(),
                    html.Label(id="specimen", children="Specimen Type:"),
                    dcc.Input(
                        id="specimen-input",
                        type='text',
                        style={"margin-bottom": "20px", "width": "100%",
                               "backgroundColor": "#242633",
                               "color": "white"},
                        value='SPUTUM'
                    ),
                ],
            ),

            html.Div(
                id="value-setter-menu",
                # className='six columns',
                children=[
                    html.Div(id="value-setter-panel"),
                    html.Br(),
                    html.Div(
                        id="button-div",
                        children=[
                            html.Button("Predict",
                                        id="predict-btn",
                                        ),
                            # html.Button(
                            #     "View current setup",
                            #     id="value-setter-view-btn",
                            #     n_clicks=0,
                            # ),
                            html.Div(id='predict-output-container')
                        ],
                    ),
                    # html.Div(
                    #     id="value-setter-view-output", className="output-datatable"
                    # ),
                ],
            ),
        ],
    ),
])


@app.callback(
    Output('predict-output-container', 'children'),
    [Input('gender-dropdown', 'value'),
     Input('age-input', 'value'),
     Input('ethnicity-dropdown', 'value'),
     Input('diagnosis-dropdown', 'value'),
     Input('previous-admissions-input', 'value'),
     Input('sample-collection-input', 'value'),
     Input('antibiotic-input', 'value'),
     Input('organisms-dropdown', 'value'),
     Input('specimen-input', 'value'),
     Input("predict-btn", "n_clicks")
     ]
)
def get_gender(gender, age, ethn, diag, prev_adm, sample_col, anti, orgs, speci,
               clicks):
    input_dict = {
        'gender': gender,
        'age': age,
        'ethnicity': ethn,

        'previous_admission': prev_adm,
        'simple_collection_interval': sample_col,
        'antibiotic_name': anti,
        'organism_name': orgs,
        'specimen_type': speci,
    }

    print(clicks)
    if clicks:
        global last_click
        if clicks == 1 and last_click > 0:
            last_click = 0
        if clicks - 1 == last_click:
            last_click = clicks

            # conversion
            input_dict['simple_collection_interval'] = float(input_dict['simple_collection_interval'])
            print(input_dict['simple_collection_interval'])

            MODEL_PATH = 'models/'

            diagnosis = diag
            index = model_list.index(diagnosis)

            with open(MODEL_PATH + model_list[index] + '.pkl', 'rb') as s:
                model = pickle.load(s)

            # data_process
            test_data = data_process(input_dict)

            pred = model.predict(test_data)
            print(pred[0])

            return 'Prediction "{}"'.format(pred[0])

    return None
