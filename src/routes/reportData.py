
from operator import indexOf
from flask import Flask, request, json, jsonify, make_response, flash, redirect, url_for, send_from_directory

import os, datetime, csv, json
from flask.templating import render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from os.path import join, dirname, realpath

from ..utils.crypt import encrypt, decrypt
from ..utils.authorisation import generateToken
from ..utils.authorisation import verifyLogin


from ..utils.models import db, Opd, Uptd, Bandwith, Isp, OpdLink, UptdLink, OpdInsident, UptdInsident, Complaint

from . import router

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from sqlalchemy import func, or_, and_,  not_



#####################################################################################################
# GET OPD WITH PROP DATA
#####################################################################################################
@router.route('/report/get-opd', methods=['POST', 'GET'])
@verifyLogin
def getOpd():

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
# ADD OPD MASTER
#####################################################################################################
@router.route('/report/add-opd', methods=['POST'])
def addOpd():
    body = request.json

    name = body["name"]
    address = body["address"]
    pic = body["pic"]
    phone_number = body["phone_number"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    opd_exist = db.session.query(Opd).filter_by(name = name).scalar() is not None
    
    if (opd_exist):
        response["message"] = "Data Opd sudah ada"
        response["status_code"] = 401
    
    else:
        try:            
            opd = Opd(
                name = name.title(),
                address = address.title(),
                pic = pic.title(),
                phone_number = phone_number,
                created_at = datetime.datetime.now() )

            db.session.add(opd)
            db.session.commit()

            response["message"] =  "Opd created. Opd-id = {}".format(opd.id)
            response["error"] = False
            response["data"] = opd.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL OPD
#####################################################################################################
@router.route('/report/get-opd-all')
@verifyLogin
def getOpdAll():

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        opd_all = Opd.query.order_by(Opd.name).all()        

        data = ([e.serialise() for e in opd_all])
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

#####################################################################################################
# GET OPD BY ID
#####################################################################################################
@router.route('/report/get-opd/<id>')
@verifyLogin
def getOpdById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    opdExist = db.session.query(Opd).filter_by(id = id).scalar() is not None

    if (opdExist == True) :
        try:
            opd = Opd.query.filter_by(id = id).first()

            response["message"] ="Data Opd ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = opd.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data Opd tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE OPD BY ID
#####################################################################################################
@router.route('/report/update-opd/<id>', methods=['PUT'])
@verifyLogin
def updateOpdById(id):
    body = request.json
    
    name = body["name"]
    address = body["address"]
    pic = body["pic"]
    phone_number = body["phone_number"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    opd = db.session.query(Opd).filter_by(id = id).first()
    
    if (opd == None):
        response["message"] = "Opd tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            opd.name = name.title() 
            opd.address = address.title()
            opd.pic = pic.title()
            opd.phone_number = phone_number 

            db.session.commit()

            response["message"] =  "Data updated. opd-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = opd.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE OPD MASTER
#####################################################################################################
@router.route('/report/delete-opd/<id>', methods=['DELETE'])
@verifyLogin
def deleteOpdMaster(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    opd = db.session.query(Opd).filter_by(id = id).first()

    if (opd == None):
        response["message"] = "Data opd tidak ditemukan"
    else:
        try:            
            Opd.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data master opd with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)




#####################################################################################################
# ADD UPTD MASTER
#####################################################################################################
@router.route('/report/add-uptd', methods=['POST'])
def addUptd():
    body = request.json

    name = body["name"]
    address = body["address"]
    opd_id = body["opd_id"]
    pic = body["pic"]
    phone_number = body["phone_number"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    uptd_exist = db.session.query(Uptd).filter_by(name = name).scalar() is not None
    
    if (uptd_exist):
        response["message"] = "Data Uptd sudah ada"
        response["status_code"] = 401
    
    else:
        try:            
            uptd = Uptd(
                name = name.title(),
                address = address.title(),
                pic = pic.title(),
                opd_id = opd_id,
                phone_number = phone_number,
                created_at = datetime.datetime.now() )

            db.session.add(uptd)
            db.session.commit()

            response["message"] =  "Uptd created. Opd-id = {}".format(uptd.id)
            response["error"] = False
            response["data"] = uptd.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL UPTD
#####################################################################################################
@router.route('/report/get-uptd-all')
@verifyLogin
def getAllUptd():

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        uptd_all = Uptd.query.order_by(Uptd.name).all()        

        data = ([e.serialise() for e in uptd_all])
        uptd_all_count  = len(data)
        response["message"] = "Jumlah Uptd: " + str(uptd_all_count)
        response["error"] = False
        if uptd_all_count <= 0:
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

#####################################################################################################
# GET UPTD BY ID
#####################################################################################################
@router.route('/report/get-uptd/<id>')
@verifyLogin
def getUptdById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }
    
    uptdExist = db.session.query(Uptd).filter_by(id = id).scalar() is not None

    if (uptdExist == True) :
        try:
            uptd = Uptd.query.filter_by(id = id).first()

            response["message"] ="Data Uptd ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = uptd.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500            
        finally:
            db.session.close()

    else :
        response["message"] = "Data Uptd tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE UPTD BY ID
#####################################################################################################
@router.route('/report/update-uptd/<id>', methods=['PUT'])
@verifyLogin
def updateUptdById(id):
    body = request.json
    
    name = body["name"]
    address = body["address"]
    pic = body["pic"]
    phone_number = body["phone_number"]
    opd_id = body["opd_id"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    uptd = db.session.query(Uptd).filter_by(id = id).first()
    
    if (uptd == None):
        response["message"] = "Uptd tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            uptd.name = name 
            uptd.address = address 
            uptd.pic = pic 
            uptd.phone_number = phone_number 
            uptd.opd_id = opd_id

            db.session.commit()

            response["message"] =  "Data updated. uptd-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = uptd.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE UPTD MASTER
#####################################################################################################
@router.route('/report/delete-uptd/<id>', methods=['DELETE'])
@verifyLogin
def deleteUptdMaster(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    uptd = db.session.query(Uptd).filter_by(id = id).first()

    if (uptd == None):
        response["message"] = "Data uptd tidak ditemukan"
    else:
        try:            
            Uptd.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data master uptd with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)




#####################################################################################################
# ADD NEW BANDWITH
#####################################################################################################
@router.route('/bandwith/add', methods=['POST'])
def addBandwith():
    body = request.json

    bandwith = body["bandwith"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

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
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET BANDWITH BY ID
#####################################################################################################
@router.route('/bandwith/get-bandwith/<id>')
@verifyLogin
def getBandById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    bandwithExist = db.session.query(Bandwith).filter_by(id = id).scalar() is not None

    if (bandwithExist == True) :
        try:
            bandwith = Bandwith.query.filter_by(id = id).first()

            response["message"] ="Data Bandwith ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = bandwith.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data Bandwith tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE BANDWITH BY ID
#####################################################################################################
@router.route('/bandwith/update-bandwith/<id>', methods=['PUT'])
@verifyLogin
def updateBandById(id):
    body = request.json
    
    band = body["bandwith"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    bandwith = db.session.query(Bandwith).filter_by(id = id).first()
    
    if (bandwith == None):
        response["message"] = "Banwdith tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            bandwith.bandwith = band

            db.session.commit()

            response["message"] =  "Bandwith updated. bandwith-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = bandwith.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE BANDWITH MASTER
#####################################################################################################
@router.route('/bandwith/delete-bandwith/<id>', methods=['DELETE'])
@verifyLogin
def deleteBandwith(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    bandwith = db.session.query(Bandwith).filter_by(id = id).first()

    if (bandwith == None):
        response["message"] = "Data bandwith tidak ditemukan"
    else:
        try:            
            Bandwith.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data master bandwith with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL BANDWITH
#####################################################################################################

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




#####################################################################################################
# ADD NEW ISP
#####################################################################################################
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
                name = name.title(),
                created_at = datetime.datetime.now() )

            db.session.add(name)
            db.session.commit()

            response["message"] =  "Isp created. User-id = {}".format(name.id)
            response["error"] = False
            response["data"] = name.returnToIsp()
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL ISP
#####################################################################################################
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

#####################################################################################################
# GET ISP BY ID
#####################################################################################################
@router.route('/isp/get-isp/<id>')
@verifyLogin
def getIspById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    ispExist = db.session.query(Isp).filter_by(id = id).scalar() is not None

    if (ispExist == True) :
        try:
            isp = Isp.query.filter_by(id = id).first()

            response["message"] ="Data Isp ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = isp.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data Isp tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE ISP BY ID
#####################################################################################################
@router.route('/isp/update-isp/<id>', methods=['PUT'])
@verifyLogin
def updateIspById(id):
    body = request.json
    
    isp_name = body["name"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    isp = db.session.query(Isp).filter_by(id = id).first()
    
    if (isp == None):
        response["message"] = "Isp tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            isp.name = isp_name.title()

            db.session.commit()

            response["message"] =  "Isp updated. bandwith-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = isp.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE ISP MASTER
#####################################################################################################
@router.route('/isp/delete-isp/<id>', methods=['DELETE'])
@verifyLogin
def deleteIsp(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    isp = db.session.query(Isp).filter_by(id = id).first()

    if (isp == None):
        response["message"] = "Data isp tidak ditemukan"
    else:
        try:            
            Isp.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data master isp with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)








#####################################################################################################
# ADD NEW COMPLAINT CATOGORY
#####################################################################################################
@router.route('/complaint/add', methods=['POST'])
def addComplaint():
    body = request.json

    category = body["category"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek email udah dipake belum
    is_exist = db.session.query(Complaint).filter_by(category = category).scalar() is not None
    
    if (is_exist == True):
        response["message"] = "Data kategori keluhan sudah ada"
    else:
        try:            
            complaint = Complaint(
                category = category.title(),
                created_at = datetime.datetime.now() )

            db.session.add(complaint)
            db.session.commit()

            response["message"] =  "Complaint created. User-id = {}".format(complaint.id)
            response["error"] = False
            response["data"] = complaint.serialise()
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL COMPLAINT CATOGORY
#####################################################################################################
@router.route('/complaint/get-all-complaint')
@verifyLogin
def getAllComplaint():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    is_exist = db.session.query(Complaint.category).all() is not None

    if (is_exist == True) :
        try:
            complaint = Complaint.query.order_by(Complaint.category).all()
            data = ([e.serialise() for e in complaint])
            
            data_count  = len(data)
            response["message"] = "Complaint(s) found : " + str(data_count)
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
        response["message"] = "Complaint Tidak Ditemukan"

    return jsonify(response)

#####################################################################################################
# GET COMPLAINT BY ID
#####################################################################################################
@router.route('/complaint/get-complaint/<id>')
@verifyLogin
def getComplaintById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    is_exist = db.session.query(Complaint).filter_by(id = id).scalar() is not None

    if (is_exist == True) :
        try:
            complaint = Complaint.query.filter_by(id = id).first()

            response["message"] ="Data Complaint ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = complaint.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data Complaint tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE COMPLAINT BY ID
#####################################################################################################
@router.route('/complaint/update-complaint/<id>', methods=['PUT'])
@verifyLogin
def updateComplaintById(id):
    body = request.json
    
    category = body["category"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    is_exist = db.session.query(Complaint).filter_by(id = id).first()
    
    if (is_exist == None):
        response["message"] = "Complaint tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            is_exist.category = category.title()

            db.session.commit()

            response["message"] =  "Complaint updated. bandwith-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = is_exist.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE COMPLAINT MASTER
#####################################################################################################
@router.route('/complaint/delete-complaint/<id>', methods=['DELETE'])
@verifyLogin
def deleteComplaint(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    complaint = db.session.query(Complaint).filter_by(id = id).first()

    if (complaint == None):
        response["message"] = "Data complaint tidak ditemukan"
    else:
        try:            
            Complaint.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data master complaint category with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)








#####################################################################################################
# ADD NEW OPD LINK
#####################################################################################################
@router.route('/report/add-opd-link', methods=['POST'])
def addOpdLink():
    body = request.json

    prtg_id = 0 if body["prtg_id"] == "" else body["prtg_id"]
    opd_id = body["opd_id"]
    isp_id = body["isp_id"]
    band_id = body["band_id"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek email udah dipake belum
    link_opd = db.session.query(OpdLink).filter_by(opd_id = id).first()
    
    if link_opd != None:
        if link_opd.prtg_id == prtg_id:
            response["message"] = "Data prtg sudah ada"
            response["status_code"] = 401
    else:
        try:            
            link = OpdLink(
                prtg_id = prtg_id,
                opd_id = opd_id,
                isp_id = isp_id,
                band_id = band_id,
                created_at = datetime.datetime.now() )

            db.session.add(link)
            db.session.commit()

            response["message"] =  "Opd Link addded. Opdlink-id = {}".format(opd_id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = link.returnAllOpdLink()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL OPD LINK
#####################################################################################################
@router.route('/report/get-opd-link')
@verifyLogin
def getOpdLink():
    # body = request.json
    # start_date = body['start_date']
    # end_date = body['end_date']
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        opd_link_all = OpdLink.query.order_by(OpdLink.id).all()

        data = ([e.returnAllOpdLink() for e in opd_link_all])
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

#####################################################################################################
# GET OPD LINK BY ID
#####################################################################################################
@router.route('/report/get-opd-link/<id>')
@verifyLogin
def getOpdLinkById(id):
    # body = request.json
    # start_date = body['start_date']
    # end_date = body['end_date']
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    
    }
    # cek username ada atau engga
    opdlink_exist = db.session.query(OpdLink).filter_by(id = id).first()

    if (opdlink_exist != None):
        try:
            opd_link = OpdLink.query.filter_by(id = id).first()

            response["message"] ="Data ditemukan"
            response["error"] = False
            response["status_code"] = 200
            response["data"] = opd_link.returnAllOpdLink()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data tidak ditemukan"


    return jsonify(response)

#####################################################################################################
# UPDATE OPD LINK
#####################################################################################################
@router.route('/report/update-opd-link/<id>', methods=['PUT'])
@verifyLogin
def updateOpdLink(id):
    body = request.json
    
    prtg_id = 0 if body["prtg_id"] == "" else body["prtg_id"]
    opd_id = body["opd_id"]
    isp_id = body["isp_id"]
    band_id = body["band_id"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    link_opd = db.session.query(OpdLink).filter_by(id = id).first()
    
    if (link_opd == None):
        response["message"] = "Opd opd tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            link_opd.prtg_id = prtg_id
            link_opd.opd_id = opd_id
            link_opd.isp_id = isp_id
            link_opd.band_id = band_id

            db.session.commit()

            response["message"] =  "Data updated. opd-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = link_opd.returnAllOpdLink()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE OPD LINK
#####################################################################################################
@router.route('/report/delete-opd-link/<id>', methods=['DELETE'])
@verifyLogin
def deleteOpdLink(id):

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    link_opd = db.session.query(OpdLink).filter_by(id = id).first()

    if (link_opd == None):
        response["message"] = "Data opd tidak ditemukan"
    else:
        try:                        
            OpdLink.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data opd with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)





#####################################################################################################
# ADD NEW UPTD LINK
#####################################################################################################
@router.route('/report/add-uptd-link', methods=['POST'])
def addUptdLink():
    body = request.json

    prtg_id = 0 if body["prtg_id"] == "" else body["prtg_id"]
    uptd_id = body["uptd_id"]
    isp_id = body["isp_id"]
    band_id = body["band_id"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek email udah dipake belum
    link_uptd = db.session.query(UptdLink).filter_by(uptd_id = id).first()
    
    if link_uptd != None:
        if link_uptd.prtg_id == prtg_id:
            response["message"] = "Data prtg sudah ada"
            response["status_code"] = 401
    else:
        try:            
            link = UptdLink(
                prtg_id = prtg_id,
                uptd_id = uptd_id,
                isp_id = isp_id,
                band_id = band_id,
                created_at = datetime.datetime.now() )

            db.session.add(link)
            db.session.commit()

            response["message"] =  "Uptd Link addded. UptdLink-id = {}".format(uptd_id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = link.returnAllUptdLink()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL UPTD LINK
#####################################################################################################
@router.route('/report/get-uptd-link')
@verifyLogin
def getUptdLink():
    # body = request.json
    # start_date = body['start_date']
    # end_date = body['end_date']
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        uptd_link_all = UptdLink.query.order_by(UptdLink.id).all()

        data = ([e.returnAllUptdLink() for e in uptd_link_all])
        uptd_all_count  = len(data)
        response["message"] = "Jumlah Uptd: " + str(uptd_all_count)
        response["error"] = False
        if uptd_all_count <= 0:
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

#####################################################################################################
# GET UPTD LINK BY ID
#####################################################################################################
@router.route('/report/get-uptd-link/<id>')
@verifyLogin
def getUptdLinkById(id):
    # body = request.json
    # start_date = body['start_date']
    # end_date = body['end_date']
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    
    }
    # cek username ada atau engga
    uptdlink_exist = db.session.query(UptdLink).filter_by(id = id).first()

    if (uptdlink_exist != None):
        try:
            uptd_link = UptdLink.query.filter_by(id = id).first()

            response["message"] ="Data ditemukan"
            response["error"] = False
            response["status_code"] = 200
            response["data"] = uptd_link.returnAllUptdLink()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data tidak ditemukan"


    return jsonify(response)

#####################################################################################################
# UPDATE UPTD LINK
#####################################################################################################
@router.route('/report/update-uptd-link/<id>', methods=['PUT'])
@verifyLogin
def updateUptdLink(id):
    body = request.json
    
    prtg_id = 0 if body["prtg_id"] == "" else body["prtg_id"]
    uptd_id = body["uptd_id"]
    isp_id = body["isp_id"]
    band_id = body["band_id"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    link_uptd = db.session.query(UptdLink).filter_by(id = id).first()
    
    if (link_uptd == None):
        response["message"] = "Uptd tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            link_uptd.prtg_id = prtg_id
            link_uptd.uptd_id = uptd_id
            link_uptd.isp_id = isp_id
            link_uptd.band_id = band_id

            db.session.commit()

            response["message"] =  "Data updated. uptd-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = link_uptd.returnAllUptdLink()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE UPTD LINK
#####################################################################################################
@router.route('/report/delete-uptd-link/<id>', methods=['DELETE'])
@verifyLogin
def deleteUptdLink(id):

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    link_uptd = db.session.query(UptdLink).filter_by(id = id).first()

    if (link_uptd == None):
        response["message"] = "Data opd tidak ditemukan"
    else:
        try:            
            UptdLink.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data uptd with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)







#####################################################################################################
# ADD NEW OPD INSIDENT
#####################################################################################################
@router.route('/insident/add-opd-insident', methods=['POST'])
def addOpdInsident():
    body = request.json

    opd_id = body["opd_id"]
    month = body["month"]
    comp_id = body["comp_id"]
    amount = body["amount"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    insident_exist = db.session.query(OpdInsident.id).filter(OpdInsident.opd_id == opd_id, OpdInsident.month == month, OpdInsident.comp_id == comp_id).scalar() is not None
    
    if insident_exist:
        response["message"] = "Data keluhan sudah ada"
        response["status_code"] = 401

    else:
        try:            
            opd_insident = OpdInsident(
                opd_id = opd_id,
                month = month,
                comp_id = comp_id,
                amount = amount,
                created_at = datetime.datetime.now() )

            db.session.add(opd_insident)
            db.session.commit()

            response["message"] =  "Data keluhan ditambahkan. id keluhan = {}".format(opd_insident.id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = opd_insident.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL OPD INSIDENT
#####################################################################################################
@router.route('/insident/get-all-opd-insident')
def getOpdInsident():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        opd_insident = db.session.query(OpdInsident).all()
        data = ([e.serialise() for e in opd_insident])
        # uptdCount  = len(data)
        # response["message"] = "Uptd(s) found : " + str(uptdCount)
        response["message"] ="Data keluhan ditemukan"
        response["error"] = False            
        response["status_code"] = 200
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
        response["error"] = True
        response["status_code"] = 500
    finally:
        db.session.close()


    return jsonify(response)

#####################################################################################################
# GET OPD INSIDENT BY ID
#####################################################################################################
@router.route('/insident/get-opd-insident/<id>')
@verifyLogin
def getOpdInsidentById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    insidentExist = db.session.query(OpdInsident).filter_by(id = id).scalar() is not None

    if (insidentExist == True) :
        try:
            insident = OpdInsident.query.filter_by(id = id).first()

            response["message"] ="Data keluhan ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = insident.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data keluhan tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE OPD INSIDENT BY ID
#####################################################################################################
@router.route('/insident/update-opd-insident/<id>', methods=['PUT'])
@verifyLogin
def updateOpdInsident(id):
    body = request.json
    
    opd_id = body["opd_id"]
    month = body["month"]
    comp_id = body["comp_id"]
    amount = body["amount"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    insident = db.session.query(OpdInsident).filter_by(id = id).first()
    
    if (insident == None):
        response["message"] = "Data keluhan tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            insident.opd_id = opd_id
            insident.month = month
            insident.comp_id = comp_id
            insident.amount = amount

            db.session.commit()

            response["message"] =  "Insident updated. insident-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = insident.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE OPD INSIDENT
#####################################################################################################
@router.route('/insident/delete-opd-insident/<id>', methods=['DELETE'])
@verifyLogin
def deleteOpdInsident(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    insident = db.session.query(OpdInsident).filter_by(id = id).first()

    if (insident == None):
        response["message"] = "Data keluhan tidak ditemukan"
    else:
        try:            
            OpdInsident.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data opd insident with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)






#####################################################################################################
# ADD NEW UPTD INSIDENT
#####################################################################################################
@router.route('/insident/add-uptd-insident', methods=['POST'])
def addUptdInsident():
    body = request.json

    uptd_id = body["uptd_id"]
    month = body["month"]
    comp_id = body["comp_id"]
    amount = body["amount"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    insident_exist = db.session.query(UptdInsident.id).filter(UptdInsident.uptd_id == uptd_id, UptdInsident.month == month, UptdInsident.comp_id == comp_id).scalar() is not None
    
    if insident_exist:
        response["message"] = "Data keluhan sudah ada"
        response["status_code"] = 401

    else:
        try:            
            uptd_insident = UptdInsident(
                uptd_id = uptd_id,
                month = month,
                comp_id = comp_id,
                amount = amount,
                created_at = datetime.datetime.now() )

            db.session.add(uptd_insident)
            db.session.commit()

            response["message"] =  "Data keluhan ditambahkan. id keluhan = {}".format(uptd_insident.id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = uptd_insident.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# GET ALL UPTD INSIDENT
#####################################################################################################
@router.route('/insident/get-all-uptd-insident')
@verifyLogin
def getUptdComplaint():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        insident = db.session.query(UptdInsident).all()
        data = ([e.serialise() for e in insident])
        # uptdCount  = len(data)
        # response["message"] = "Uptd(s) found : " + str(uptdCount)
        response["message"] ="Data keluhan ditemukan"
        response["error"] = False            
        response["status_code"] = 200
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
        response["error"] = True
        response["status_code"] = 500
    finally:
        db.session.close()


    return jsonify(response)

#####################################################################################################
# GET UPTD INSIDENT BY ID
#####################################################################################################
@router.route('/insident/get-uptd-insident/<id>')
@verifyLogin
def getUptdInsidentById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    insidentExist = db.session.query(UptdInsident).filter_by(id = id).scalar() is not None

    if (insidentExist == True) :
        try:
            insident = UptdInsident.query.filter_by(id = id).first()

            response["message"] ="Data keluhan ditemukan"
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = insident.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    else :
        response["message"] = "Data keluhan tidak ditemukan"

    return jsonify(response)

#####################################################################################################
# UPDATE OPD INSIDENT BY ID
#####################################################################################################
@router.route('/insident/update-uptd-insident/<id>', methods=['PUT'])
@verifyLogin
def updateUptdInsident(id):
    body = request.json
    
    uptd_id = body["uptd_id"]
    month = body["month"]
    comp_id = body["comp_id"]
    amount = body["amount"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    insident = db.session.query(UptdInsident).filter_by(id = id).first()
    
    if (insident == None):
        response["message"] = "Data keluhan tidak ditemukan"
        response["status_code"] = 403
    else:
        try:            
            insident.uptd_id = uptd_id
            insident.month = month
            insident.comp_id = comp_id
            insident.amount = amount

            db.session.commit()

            response["message"] =  "Insident updated. insident-id = {}".format(id)
            response["error"] = False            
            response["status_code"] = 200
            response["data"] = insident.serialise()
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)

#####################################################################################################
# DELETE UPTD INSIDENT
#####################################################################################################
@router.route('/insident/delete-uptd-insident/<id>', methods=['DELETE'])
@verifyLogin
def deleteUptdInsident(id):
    
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    insident = db.session.query(UptdInsident).filter_by(id = id).first()

    if (insident == None):
        response["message"] = "Data keluhan tidak ditemukan"
    else:
        try:            
            UptdInsident.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "Data uptd insident with id {} has been deleted".format(id)
            response["error"] = False
            response["status_code"] = 200      
        except Exception as e:
            response["message"] = str(e)
            response["error"] = True
            response["status_code"] = 500
        finally:
            db.session.close()

    
    return jsonify(response)




  

#####################################################################################################
# GET ALL ISP NAME
#####################################################################################################
@router.route('/report/get-isp-name')
@verifyLogin
def getIspName():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        isp = Isp.query.order_by(Isp.name).all()

        data = ([e.serialise() for e in isp])
        dataCount  = len(data)
        response["message"] = "Data(s) found : " + str(dataCount)
        response["error"] = False
        response["status_code"] = 200      
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)


  

#####################################################################################################
# GET ALL BANDWITH LISTs
#####################################################################################################
@router.route('/report/get-band-list')
@verifyLogin
def getBandList():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        band = Bandwith.query.order_by(Bandwith.bandwith).all()

        data = ([e.serialise() for e in band])
        dataCount  = len(data)
        response["message"] = "Data(s) found : " + str(dataCount)
        response["error"] = False
        response["status_code"] = 200      
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)



#####################################################################################################
# GET ALL OPD NAME
#####################################################################################################
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
        response["status_code"] = 200      
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)

#####################################################################################################
# GET ALL UPTD NAME
#####################################################################################################
@router.route('/report/get-uptd-name/<id>')
@verifyLogin
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
        response["status_code"] = 200      
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
        response["error"] = True
        response["status_code"] = 500
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)


