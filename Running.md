## How to run the applications on local machine <br>
### (Option 1) Using Docker registry
```
docker run -p 5005:5005 -d --name mimic_app ghcr.io/qyune/mimic_app:v1
docker run -p 8088:8088 -d --name mimic_web ghcr.io/qyune/mimic_web:v1
```

### (Option 2) Running Flask / Dash application using virtual environment
- mimic_app (Flask): Antibiotic Effectiveness Prediction<br>
In mimic_app/ directory,
```
pip3 install virtualenv
python3 -m venv venv
for Linux or Mac: source venv/bin/activate
for Windows: venv\Scripts\activate.bat
pip3 install -r requirements.txt
(optional) pip3 freeze > requirements.txt
--> Add current packages on to requirements.txt
python3 run.py
```

- web_app (Dash): Dashboard App for Querying Mortality Rate and LOS <br>
In web_app/ directory,
python3 run.py
```
pip3 install virtualenv
python3 -m venv venv
for Linux or Mac: source venv/bin/activate
for Windows: venv\Scripts\activate.bat
pip3 install -r requirements.txt
(optional) pip3 freeze > requirements.txt
--> Add current packages on to requirements.txt
python3 app.py
```
### Antibiotic Effectiveness
- code/DatasetPreProcessing.ipynb is the jupyter notebook that generates the 17 csv files for running the models
- code/Diagnosis Models/*Diagnosis Name* includes the code for running every model in their jupyter notebook and their generated pickle files
- code/CSV_files_for_Dash.ipynb has the jupyter notebook that will generate CSV files for the Dasboard for the web application and will push these .csv files into AWS Cloud

### LOS and Mortaility Rate Prediction
- code/Mortality_LOS_pipeline.ipynb is the jupyter notebook that contains the entire pipeline for this task.
