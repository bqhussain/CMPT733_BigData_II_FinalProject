## How to run the applications on local machine <br>
### (Option 1) Using Docker registry
```
docker run -p 5005:5005 -d --name mimic_app ghcr.io/qyune/mimic_app:v1
docker run -p 8088:8088 -d --name mimic_web ghcr.io/qyune/mimic_web:v1
```

### (Option 2) Running Flask / Dash application using virtual environment
```
pip3 install virtualenv
python3 -m venv venv
for Linux or Mac: source venv/bin/activate
for Windows: venv\Scripts\activate.bat
pip3 install -r requirements.txt
(optional) pip3 freeze > requirements.txt
python3 run.py
```
