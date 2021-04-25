import pandas as pd
from pickle import load


def data_process(data):
    SPEC_TYPE_DESC = data['specimen_type']
    ORG_NAME = data['organism_name']
    AB_NAME = data['antibiotic_name']
    gender = data['gender']
    ethnicity_grouped = data['ethnicity']
    admission_age = pd.Series(data['age'])

    collection_interval = pd.Series(data['simple_collection_interval'])
    previous_admissions = pd.Series(data['previous_admission'])

    inputs = [SPEC_TYPE_DESC, ORG_NAME, AB_NAME, gender, ethnicity_grouped]

    pred_data = pd.DataFrame([inputs],
                             columns=['SPEC_TYPE_DESC', 'ORG_NAME', 'AB_NAME', 'gender', 'ethnicity_grouped', ])

    # load the encoder
    # change the path
    encoder = load(open('data/mimicEncoder.pkl', 'rb'))
    encode = encoder.transform(pred_data)
    encoded_data = pd.DataFrame(encode)
    encoded_data['admission_age'] = admission_age
    encoded_data['collection_interval'] = collection_interval
    encoded_data['previous_admissions'] = previous_admissions

    # load the scaler
    # change the path
    scaler = load(open('data/mimicScaler.pkl', 'rb'))
    scaled_df = scaler.transform(encoded_data)
    transformed_df = pd.DataFrame(scaled_df)

    return transformed_df
