
# from flask import Flask, request, json, jsonify, make_response, flash, redirect, url_for, send_from_directory

# import os, datetime
# from flask.templating import render_template
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage

# from os.path import join, dirname, realpath

# from ..utils.crypt import encrypt, decrypt
# from ..utils.authorisation import generateToken
# from ..utils.authorisation import verifyLogin


# from ..utils.models import db, Guest

# from . import router

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import exists
# from sqlalchemy import func, or_




# #####################################################################################################
# # ADD GUEST
# #####################################################################################################
# @router.route('/guest/add', methods=['POST'])
# @verifyLogin
# def addGuest():
#     body = request.json

#     # id = body["id"]
#     name = body["name"]
#     email = body["email"]
#     nik = body["nik"]
#     institution = body["institution"]
#     phoneNumber = body["phoneNumber"]
#     arrivalTime = body["arrivalTime"]
#     departureTime = body["departureTime"]
#     ktpImage = body["ktpImage"] #ini nanti ngambil name filenya dari response endpoint ktp upload image
#     signImage = body["signImage"] #ini nanti ngambil name filenya dari response endpoint ttd upload image
#     # active = body["active"]
#     visitReason = body["visitReason"]

#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }

#     if arrivalTime == "":
#         arrivalTime = None
        
#     if departureTime == "":
#         departureTime = None
    
#     try:            
#         guest = Guest(
#             # id = id,
#             name = name.title(),
#             email = email,
#             nik = nik,
#             institution = institution.title(),
#             phoneNumber = phoneNumber,
#             arrivalTime = arrivalTime,
#             departureTime = departureTime,
#             ktpImage = ktpImage,
#             signImage = signImage,
#             active = True,
#             visitReason = visitReason.capitalize() )

#         db.session.add(guest)
#         db.session.commit()

#         response["message"] =  "Guest created. Guest-id = {}".format(guest.id)
#         response["error"] = False
#         response["data"] = guest.returnToGuest()
#     except Exception as e:
#         response["message"] = str(e)
#     finally:
#         db.session.close()

    
#     return jsonify(response)


# #####################################################################################################
# # UPDATE GUEST
# #####################################################################################################
# @router.route('/guest/update/<id>', methods=['PUT'])
# @verifyLogin
# def updateGuest(id):
#     body = request.json

#     # id = body["id"]
#     name = body["name"]
#     email = body["email"]
#     institution = body["institution"]
#     phoneNumber = body["phoneNumber"]
#     arrivalTime = body["arrivalTime"]
#     departureTime = body["departureTime"]
#     if body["ktpImage"] != '':
#         ktpImage = body["ktpImage"]
#     if body["signImage"] != '':
#         signImage = body["signImage"]
#     nik = body["nik"]
#     # active = body["active"]
#     visitReason = body["visitReason"]

#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }

#     # get guest
#     guest = db.session.query(Guest).filter_by(id = id).first()
    
#     if (guest == False):
#         response["message"] = "Tamu belum terdaftar"
#     else:
#         try:            
#             # guest.id = id
#             guest.name = name.title()
#             guest.email = email
#             guest.nik = nik
#             guest.institution = institution.title()
#             guest.phoneNumber = phoneNumber
#             guest.arrivalTime = arrivalTime
#             guest.departureTime = departureTime
#             guest.ktpImage = ktpImage
#             guest.signImage = signImage
#             # guest.active = active
#             guest.visitReason = visitReason.capitalize()

#             db.session.commit()

#             response["message"] =  "Guest updated. Guest-id = {}".format(guest.id)
#             response["error"] = False
#             response["data"] = guest.returnToGuest()
#         except Exception as e:
#             response["message"] = str(e)
#         finally:
#             db.session.close()

    
#     return jsonify(response)



# #####################################################################################################
# # DELETE GUEST
# #####################################################################################################
# @router.route('/guest/deleteGuest/<id>', methods=['PUT'])
# @verifyLogin
# def deleteGuest(id):
#     body = request.json
#     active = body["active"]

#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }
    
#     # get guest
#     guest = db.session.query(Guest).filter_by(id = id).first()
    
#     if (guest == False):
#         response["message"] = "Tamu belum terdaftar"
#     else:
#         try:            
#             guest.active = active
#             db.session.commit()

#             response["message"] =  "Guest deleted. User-id = {}".format(id)
#             response["error"] = False
#             response["data"] = ""
#         except Exception as e:
#             response["message"] = str(e)
#         finally:
#             db.session.close()

#     return jsonify(response)






# #####################################################################################################
# # GET GUEST PER ID
# #####################################################################################################
# @router.route('/guest/getGuest/<id>')
# @verifyLogin
# def getGuestById(id):
#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }

#     # cek username ada atau engga
#     guestExist = db.session.query(Guest).filter_by(id = id).scalar() is not None

#     if (guestExist == True) :
#         try:
#             guest = Guest.query.filter_by(id = id).first()

#             response["message"] ="Guest found"
#             response["error"] = False
#             response["data"] = (guest.returnToGuest())
#         except Exception as e:
#             response["message"] = str(e)
#         finally:
#             db.session.close()

#     else :
#         response["message"] = "Tamu tidak ditemukan"

#     return jsonify(response)



# #####################################################################################################
# # GET ALL GUESTS
# #####################################################################################################
# @router.route('/guest/getAll')
# @verifyLogin
# def getAllGuests():
#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }

#     try:
#         guestActve = Guest.query.filter(Guest.active == 1).order_by(Guest.name).all()

#         data = ([e.returnToGuest() for e in guestActve])
#         guestActiveCount  = len(data)
#         response["message"] = "Guest(s) found : " + str(guestActiveCount)
#         response["error"] = False
#         response["data"] = data
#     except Exception as e:
#         response["message"] = str(e)
#     finally:
#         db.session.close()


#     return jsonify(response)




# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# UPLOAD_FOLDER_KTP = join(dirname(realpath(__file__)), '..\static\\uploads\\ktp')
# UPLOAD_FOLDER_TTD = join(dirname(realpath(__file__)), '..\static\\uploads\\ttd')

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# #####################################################################################################
# # UPLOAD KTP
# #####################################################################################################
# @router.route('/guest/uploaderKTP', methods = ['GET', 'POST'])
# # @verifyLogin
# def uploadFileKTP():
#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }
#     if 'file' not in request.files:
#         response["message"] = "no file"
#         return jsonify(response)
#     if request.method == 'POST':
#         f = request.files['file']
        
#         if f.filename == '':
#             response["message"] = "no image selected for uploading"
#             return jsonify(response)

#         dt = str(datetime.datetime.now())
#         dt = dt.split(" ")
#         day = dt[0].replace("-","_")
#         time = dt[1].split(".")
#         time = time[0].replace(":","_")
#         nameDt = day + "_" + time
#         if f and allowed_file(f.filename):
#             fname = secure_filename(nameDt+'_ktp_'+f.filename)
#             f.save(os.path.join(UPLOAD_FOLDER_KTP, fname))
#             response["error"] = False
#             response["message"] = "upload success"
#             response["data"] = {"fileName" : fname}
#             return jsonify(response)
#         else:
#             response["message"] = "format file not supported"
#             return jsonify(response)



# #####################################################################################################
# # UPLOAD TTD
# #####################################################################################################
# @router.route('/guest/uploaderTTD', methods = ['GET', 'POST'])
# @verifyLogin
# def uploadFileTTD():
#     response = {
#         "error" : True,
#         "message" : "",
#         "data" : {}
#     }
#     if 'file' not in request.files:
#         response["message"] = "no file"
#         return jsonify(response)
#     if request.method == 'POST':
#         f = request.files['file']
        
#         if f.filename == '':
#             response["message"] = "no image selected for uploading"
#             return jsonify(response)

#         dt = str(datetime.datetime.now())
#         dt = dt.split(" ")
#         day = dt[0].replace("-","_")
#         time = dt[1].split(".")
#         time = time[0].replace(":","_")
#         nameDt = day + "_" + time
#         if f and allowed_file(f.filename):
#             fname = secure_filename(nameDt+'_ttd_'+f.filename)
#             f.save(os.path.join(UPLOAD_FOLDER_TTD, fname))
#             response["error"] = False
#             response["message"] = "upload success"
#             response["data"] = {"fileName" : fname}
#             return jsonify(response)
#         else:
#             response["message"] = "format file not supported"
#             return jsonify(response)


# # app.config["IMAGE_UPLOADS"] = "C:/Flask/Upload/"
# @router.route('/uploads/<folder>/<filename>')
# def send_uploaded_file(filename='',folder=''):
#     path = dirname(realpath(__file__))
#     path = path.split("\\src\\")
#     path = path[0] + '\\src\\static\\uploads\\' + folder + '\\'
#     return send_from_directory(path, filename)

