import pandas as pd
import numpy as np
import re
import json
import boto3
from sqlalchemy import create_engine
import psycopg2


class ImportDB():

    def task1_table(self, df):
        df.to_sql('task1', engine, if_exists='replace', method='multi',
                   index=False, chunksize=1000)

if __name__ == "__main__":
    # Connecting to AWS RDS (Postgresql Engine)
    engine = create_engine(
        'postgresql+psycopg2://postgres:cmpt733db@mimic-cmpt733.cfynl4oqowhh.us-east-1.rds.amazonaws.com:5432/postgres')

    df_task1 = pd.read_csv('data/task1_res.csv', sep=',')
    print(df_task1)

    db = ImportDB()
    db.task1_table(df_task1)
