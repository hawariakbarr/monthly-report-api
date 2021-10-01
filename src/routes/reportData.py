
from flask import Flask, request, json, jsonify, make_response, flash, redirect, url_for, send_from_directory

import os, datetime, csv, json
from flask.templating import render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from os.path import join, dirname, realpath

from ..utils.crypt import encrypt, decrypt
from ..utils.authorisation import generateToken
from ..utils.authorisation import verifyLogin


from ..utils.models import db, Opd, Uptd, Bandwith, Isp, OpdLink

from . import router

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from sqlalchemy import func, or_, and_,  not_



#####################################################################################################
# GET OPD PER ID
#####################################################################################################
@router.route('/report/get-opd', methods=['POST', 'GET'])
@verifyLogin
def getOpdById():

    body = request.json

    opd_param = body["opd_param"]
    uptd_param = body["uptd_param"]
    strat_date = body["start_date"]
    end_date = body["end_date"]

    # opd_param = 22
    # uptd_param = "all"
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    try:
        if opd_param == "all":
            opd_all = Opd.query.order_by(Opd.name).all()        
            data = ([e.returnToOpd(uptd_param, strat_date, end_date) for e in opd_all])
        else:                    
            opd = Opd.query.filter_by(id = opd_param).first()
            data = opd.returnToOpd(uptd_param, strat_date, end_date)

        # uptd_all = Uptd.query.filter_by(opd_id = opd_param).order_by(Uptd.name).all()
        # uptd_one = Uptd.query.filter_by(opd_id = id, id = 78).first()
        # data = ([e.returnToUptd() for e in uptd_all])
        # data = uptd_one.returnToUptd()
        # uptd_count  = len(data)

        # response["message"] ="Opd ditemukan. Jumlah Uptd: " + str(uptd_count)
        response["error"] = False
        response["status_code"] = 200
        response["data"] = data
    except Exception as e:
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()

    return jsonify(response)


#####################################################################################################
# GET ALL OPD
#####################################################################################################
    
@router.route('/report/get-opd-all')
@verifyLogin
def getOpdAll():

    body = request.json

    opd_param = body["opd_param"]
    uptd_param = body["uptd_param"]
    strat_date = body["start_date"]
    end_date = body["end_date"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        opd_all = Opd.query.order_by(Opd.name).all()        

        data = ([e.returnToOpd(uptd_param, strat_date, end_date) for e in opd_all])
        opd_all_count  = len(data)
        response["message"] = "Jumlah Opd: " + str(opd_all_count)
        response["error"] = False
        if opd_all_count <= 0:
            response["status_code"] = 404
        else:
            response["status_code"] = 200

        # for i in data:
            
        response["data"] = data
        
    except Exception as e:
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()

    return jsonify(response)


@router.route('/bandwith/add', methods=['POST'])
def addBandwith():
    body = request.json

    bandwith = body["bandwith"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek email udah dipake belum
    bandwithExist = db.session.query(Bandwith).filter_by(bandwith = bandwith).scalar() is not None
    
    if (bandwithExist == True):
        response["message"] = "Data bandwith sudah ada"
    else:
        try:            
            bandwith = Bandwith(
                bandwith = bandwith,
                created_at = datetime.datetime.now() )

            db.session.add(bandwith)
            db.session.commit()

            response["message"] =  "Bandwith created. User-id = {}".format(bandwith.id)
            response["error"] = False
            response["data"] = bandwith.returnToBandwith()
        except Exception as e:
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)

@router.route('/bandwith/get-all-band')
@verifyLogin
def getAllBand():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    band_exist = db.session.query(Bandwith.bandwith).all() is not None

    if (band_exist == True) :
        try:
            band = Bandwith.query.order_by(Bandwith.bandwith).all()
            data = ([e.returnToBandwith() for e in band])

            bandCount  = len(data)
            response["message"] = "Bandwith(s) found : " + str(bandCount)
            response["error"] = False
            response["status_code"] = 200
            response["data"] = data
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
        finally:
            db.session.close()

    else :
        response["status_code"] = 404
        response["error"] = False
        response["message"] = "Bandwith Tidak Ditemukan"

    return jsonify(response)

@router.route('/isp/add', methods=['POST'])
def addIsp():
    body = request.json

    name = body["name"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek email udah dipake belum
    ispExist = db.session.query(Isp).filter_by(name = name).scalar() is not None
    
    if (ispExist == True):
        response["message"] = "Data Isp sudah ada"
    else:
        try:            
            name = Isp(
                name = name,
                created_at = datetime.datetime.now() )

            db.session.add(name)
            db.session.commit()

            response["message"] =  "Isp created. User-id = {}".format(name.id)
            response["error"] = False
            response["data"] = name.returnToIsp()
        except Exception as e:
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)


@router.route('/isp/get-all-isp')
@verifyLogin
def getAllIsp():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    isp_exist = db.session.query(Isp.name).all() is not None

    if (isp_exist == True) :
        try:
            isp = Isp.query.order_by(Isp.name).all()
            data = ([e.returnToIsp() for e in isp])
            
            ispCount  = len(data)
            response["message"] = "Isp(s) found : " + str(ispCount)
            response["error"] = False
            response["status_code"] = 200
            response["data"] = data
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
        finally:
            db.session.close()

    else :
        response["status_code"] = 404
        response["error"] = False
        response["message"] = "Isp Tidak Ditemukan"

    return jsonify(response)



@router.route('/report/get-opd-link')
@verifyLogin
def getOpdLink():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        opd_link_all = OpdLink.query.order_by(OpdLink.id).all()

        data = ([e.returnOpdLink() for e in opd_link_all])
        opd_all_count  = len(data)
        response["message"] = "Jumlah Opd: " + str(opd_all_count)
        response["error"] = False
        if opd_all_count <= 0:
            response["status_code"] = 404
        else:
            response["status_code"] = 200
        response["data"] = data
    except Exception as e:
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()

    return jsonify(response)

@router.route('/report/get-opd-name')
@verifyLogin
def getOpdName():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        opd = Opd.query.order_by(Opd.name).all()

        data = ([e.serialise() for e in opd])
        opdCount  = len(data)
        response["message"] = "Opd(s) found : " + str(opdCount)
        response["error"] = False
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)


@router.route('/report/get-uptd-name/<id>')

def getUptdName(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        uptd = db.session.query(Uptd).filter_by(opd_id = id).all()
        data = ([e.serialise() for e in uptd])
        # uptdCount  = len(data)
        # response["message"] = "Uptd(s) found : " + str(uptdCount)
        response["error"] = False
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)