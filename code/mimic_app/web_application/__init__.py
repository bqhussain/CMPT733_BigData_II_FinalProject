from flask import Flask 

app = Flask(__name__)
app.config['SECRET_KEY'] = '710b791a8702428c954941af083ad059'

from web_application import routes

