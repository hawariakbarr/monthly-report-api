from flask import Flask, request, abort, jsonify, make_response,  render_template, redirect, url_for
import jwt
import pandas as pd
# import mysql.connector

import os, datetime
from os.path import join, dirname, realpath

from src.routes import router

from src.utils.models import db

from flask_cors import CORS

app = Flask(__name__)   #buat manggil flask
app.register_blueprint(router)

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import exists
CORS(app)


# Upload folder
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'src\\static\\uploads\\files')
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

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
    'db' : 'monthly_report',
    'host' : 'localhost',
    'port' : '3306'
}


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#postgresql: //username:password@localhost:3794/database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'% POSTGRES

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s'% MYSQL


# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="kurakuraninja14",
#   database="monthly_report"
# )

db.init_app(app)


# mycursor = mydb.cursor()

# Root URL
# @app.route('/')
# def index():
     # Set The upload HTML template '\templates\index.html'
    # return render_template('upload.html')


# # Get the uploaded files
# @app.route("/", methods=['POST'])
# def uploadFiles():
#       # get the uploaded file
#     try:
#         uploaded_file = request.files['file']
#         if uploaded_file.filename != '':
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#             # set the file path
#             uploaded_file.save(file_path)
#             # save the file
#             saveData(file_path)
#     except Exception as e:
#         print(e)    

#     return redirect(url_for('index'))

# def saveData(filePath):
#     if filePath.find("OPD") != -1:
#         col_names = ['name','address', 'pic', 'phone_number']
#         csvData = pd.read_csv(filePath, names=col_names, skiprows = 1, keep_default_na=False)
    
#         for i,row in csvData.iterrows():
#             print(i, row['name'],row['address'],row['pic'],row['phone_number'], datetime.datetime.now())
#             sql = "INSERT INTO master_opd (name, address, pic, phone_number, created_at) VALUES (%s, %s, %s, %s, %s)"
#             value = (row['name'].title(),row['address'].title(),row['pic'].title(),row['phone_number'], datetime.datetime.now())
#             mycursor.execute(sql, value)
#             mydb.commit()

#     elif filePath.find("UPTD") != -1:
#         col_names = ['opd_id','name','address', 'pic', 'phone_number']
#         csvData = pd.read_csv(filePath, names=col_names, skiprows = 1, keep_default_na=False)
    
#         for i,row in csvData.iterrows():
#             print(i, row['opd_id'], row['name'],row['address'],row['pic'],row['phone_number'], datetime.datetime.now())
#             sql = "INSERT INTO master_uptd (opd_id, name, address, pic, phone_number, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
#             value = (int(row['opd_id']), row['name'].title(), row['address'].title(), row['pic'].title(), row['phone_number'], datetime.datetime.now())
#             mycursor.execute(sql, value)
#             mydb.commit()

#     elif filePath.find("opd link") != -1:
#         col_names = ['prtg_id','opd_id','isp_id', 'band_id']
#         csvData = pd.read_csv(filePath, names=col_names, skiprows = 1)
#         csvData = (csvData.fillna(0)).astype(int)
#         dtypes = {'prtg_id': 'int', 'opd_id': 'int', 'isp_id': 'int', 'band_id': 'int'}
#         for i,row in csvData.iterrows():
#             print(i, row['prtg_id'], row['opd_id'],row['isp_id'],row['band_id'], datetime.datetime.now())
#             sql = "INSERT INTO opd_link (prtg_id, opd_id, isp_id, band_id,  created_at) VALUES (%s, %s, %s, %s, %s)"
#             value = (int(row['prtg_id']), int(row['opd_id']), int(row['isp_id']), int(row['band_id']), datetime.datetime.now())
#             mycursor.execute(sql, value)
#             mydb.commit()
    
#     elif filePath.find("uptd link") != -1:
#         col_names = ['prtg_id','uptd_id','isp_id', 'band_id']
#         csvData = pd.read_csv(filePath, names=col_names, skiprows = 1)
#         csvData = (csvData.fillna(0)).astype(int)
#         dtypes = {'prtg_id': 'int', 'uptd_id': 'int', 'isp_id': 'int', 'band_id': 'int'}
#         for i,row in csvData.iterrows():
#             print(i, row['prtg_id'], row['uptd_id'],row['isp_id'],row['band_id'], datetime.datetime.now())
#             sql = "INSERT INTO uptd_link (prtg_id, uptd_id, isp_id, band_id,  created_at) VALUES (%s, %s, %s, %s, %s)"
#             value = (int(row['prtg_id']), int(row['uptd_id']), int(row['isp_id']), int(row['band_id']), datetime.datetime.now())
#             mycursor.execute(sql, value)
#             mydb.commit()

@app.route('/addition/<int:firstNumber>/<int:secondNumber>')
def addition(firstNumber,secondNumber):
    response = {
        "data" : str(firstNumber + secondNumber),
        "message" : "berhasil"
    }
    return jsonify(response)


# @app.route('/')
# def hello_world():
#     return 'Hello world!'