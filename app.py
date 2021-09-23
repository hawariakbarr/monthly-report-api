from flask import Flask, request, abort, jsonify, make_response
import jwt

from src.routes import router
# from src.routes.guestData import UPLOAD_FOLDER
from src.utils.models import db

from flask_cors import CORS

app = Flask(__name__)   #buat manggil flask
app.register_blueprint(router)

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import exists
CORS(app)

POSTGRES = {
    'user' : 'admin',
    'pw' : 'admin',
    'db' : 'nda_project',
    'host' : 'localhost',
    'port' : '5432'
}

MYSQL = {
    'user' : 'root',
    'pass' : 'kurakuraninja14', # 'adminroot', ''
    'db' : 'nda_project',
    'host' : 'localhost',
    'port' : '3306'
}


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#postgresql: //username:password@localhost:3794/database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'% POSTGRES

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s'% MYSQL

db.init_app(app)



@app.route('/addition/<int:firstNumber>/<int:secondNumber>')
def addition(firstNumber,secondNumber):
    response = {
        "data" : str(firstNumber + secondNumber),
        "message" : "berhasil"
    }
    return jsonify(response)


@app.route('/')
def hello_world():
    return 'Hello world!'