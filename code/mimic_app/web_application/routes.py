from web_application import app
import os, json, pickle, random
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from flask_jsglue import JSGlue
import pandas as pd
import numpy as np


from web_application.preprocess import data_process


jsglue = JSGlue(app)


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
              'Endocrine_Nutritional_Metabolic_Diseases_And_Immu|nity_Disorders',  # 10
              'Factors_Influencing_Health_Status',  # 11
              'Infectious_And_Parasitic_Diseases',  # 12
              'Injury_And_Poisoning',  # 13
              'Mental_Disorders',  # 14
              'Neoplasms',  # 15
              'Symptoms_Signs_And_Ill_Defined_Conditions'  # 16
              ]

gender_list = ['F', 'M']

ethnicity_list = ['unknown',
                  'white',
                  'asian',
                  'hispanic',
                  'black',
                  'other',
                  'native']

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


@app.route("/", methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # 1 input features by user
        inputs = ['gender', 'age', 'ethnicity',
                  'diagnosis', 'previous_admission', 'simple_collection_interval',
                  'antibiotic_name', 'organism_name', 'specimen_type']

        data = []
        for i in inputs:
            if not request.form[i]:
                flash('Invalid Input')
                return render_template('home.html',
                                       diagnosis=model_list,
                                       gender=gender_list,
                                       ethnicity=ethnicity_list,
                                       organism_name=organisms_list
                                       )
            else:
                data.append(request.form[i])

        input_dict = {
            'gender': data[0],
            'age': int(data[1]),
            'ethnicity': data[2],

            'previous_admission': int(data[4]),
            'simple_collection_interval': float(data[5]),
            'antibiotic_name': data[6],
            'organism_name': data[7],
            'specimen_type': data[8],
        }
        print(input_dict)

        # input_dict = {
        #     'gender': 'M',
        #     'age': 28,
        #     'ethnicity': 'unknown',
        #     'previous_admission': 1,
        #     'simple_collection_interval': 0.1,
        #     'antibiotic_name': 'GENTAMICIN',
        #     'organism_name': 'STAPH AUREUS COAG +',
        #     'specimen_type': 'SPUTUM',
        # }

        # 2 model selection
        MODEL_PATH = 'models/'

        diagnosis = data[3]
        index = model_list.index(diagnosis)

        with open(MODEL_PATH + model_list[index] + '.pkl', 'rb') as s:
            model = pickle.load(s)

        # data_process
        test_data = data_process(input_dict)

        pred = model.predict(test_data)
        print(pred[0])

        return render_template('home.html', data=pred[0], title='Prediction',
                               result1='Sensitive', result2='Resistant',
                               diagnosis=model_list,
                               gender=gender_list,
                               ethnicity=ethnicity_list,
                               organism_name=organisms_list)

    else:
        return render_template('home.html',
                               diagnosis=model_list,
                               gender=gender_list,
                               ethnicity=ethnicity_list,
                               organism_name=organisms_list
                               )
