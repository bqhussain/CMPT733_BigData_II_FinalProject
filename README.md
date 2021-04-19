<p align="center">
  <img width="600" height="350" src="https://user-images.githubusercontent.com/32183829/115143177-98417880-9ffa-11eb-997a-b1f18a4681cf.png">
</p>

## Prediction on Antibiotic Resistance and Length of Stay for ICU Patients
- Big Data has been revolutionary when it comes to the banking and education system, and now it is time to implement it in healthcare in order to potentially bring social benefits to the public, such as delivering better patient treatment, improving drug efficiency, helping clinical professionals and medical caregivers and simplifying hospital operations.  
- Antibiotic resistance imposes a heavy burden on healthcare because due to the time it takes for sample and culture results to return, clinicians rely on prior experience and static guidelines to prescribe antibiotics without accounting for patient-specific attributes, leading to several fatalities. Such experimental treatment often fails to account for the changes that have been developed in antibiotic resistance with time and geographical locations. Hence, our project's first goal is to predict if an organism is resistive or sensitive towards numerous antibiotics, measured by interpreting a culture test. 
- Likewise, it is extremely insightful for medical professionals to have an estimate of how long a patient is likely to stay in the hospital and if they have a high chance of being in danger; which led to our second goal of predicting a patients length of stay and mortality rate using their demographics and first 24 hours vital signs.
    
### Highlights
- predictive model for checking if an organism is sensitive or resistant towards an antibiotic
- predictive model for mortality rate in a general hospital ward vs ICU
- predictive model and warning trigger for length of stay in a hospital greater than 3 and 7 days
- run the frontend end code and explore the different predictive models yourself!

### Data Product
- Running on EC2: http://ec2-3-84-161-149.compute-1.amazonaws.com:8088/ 
    
### Notes
This project is submitted as the final project for CMPT 733: Programming for Big Data II
- Code running instructions can be found in Running.md
- Project details can be found in report.pdf
- Quick project overview can be found on YouTube: https://www.youtube.com/watch?v=VMss4CuzvX8

### Directory Structure
    .
    |-- code                                          
    |    |-- Antibiotic Effectiveness                          
         |    |-- DatasetPreProcessing.ipynb
         |    |-- Diagnosis Models
         |    |   |-- Pickle files for each model
         |        |-- Jupyter Notebooks for running each model
         |
         |-- Mortality Rate and Length of Stay
         |    |-- Mortality_LOS_pipeline.ipynb
         |    |-- models
         |    |-- data
         |
         |-- mimic_app
         |    |-- web_application
         |    |-- Dockerfile
         |    |-- run.py
         |    |-- requirements.txt
         |
         |-- web_app
         |    |-- apps
         |    |    |-- anit.py  
         |         |-- patient_info.py
         |    |-- Dockerfile
         |    |-- app.py
         |    |-- data
         |    |-- app_temp.py
    |-- data                                          
    |    |-- mimic-iii-clinical-database-demo-1.4
    |    |-- mimic-code     
    |    |-- data_Mortality_LOS
    |-- docs
    |    |-- milestone.pdf
    |    |-- report.pdf
    |-- Running.md
    |-- README.md

### Contributors
- Bilal Hussain
- Hon Wing Eric Chan
- Kyoun Huh
- Sakina Patanwala
