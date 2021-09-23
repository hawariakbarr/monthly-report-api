
from flask import Flask, request, json, jsonify, make_response
import os, datetime

from ..utils.crypt import encrypt, decrypt
from ..utils.authorisation import generateToken
from ..utils.authorisation import verifyLogin


from ..utils.models import db, User, Guest

from . import router

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from sqlalchemy import func, or_




#####################################################################################################
# REGISTER USER
#####################################################################################################
@router.route('/user/register', methods=['POST'])
def registerUser():
    body = request.json

    body["password"] = encrypt(body["password"])

    name = body["name"]
    email = body["email"]
    password = body["password"]
    role = body["role"]
    department = body["department"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek email udah dipake belum
    emailExist = db.session.query(User).filter_by(email = email).scalar() is not None
    
    if (emailExist == True):
        response["message"] = "email sudah pernah dipakai"
    else:
        try:            
            user = User(
                name = name.title(),
                email = email,
                password = password,
                role = role,
                department = department.title(),
                active =  True,
                created_at = datetime.datetime.now() )

            db.session.add(user)
            db.session.commit()

            response["message"] =  "User created. User-id = {}".format(user.id)
            response["error"] = False
            response["data"] = user.returnToUser()
        except Exception as e:
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)




#####################################################################################################
# LOGIN USER
#####################################################################################################
@router.route('/user/login', methods = ['POST'])
def loginUser():
    body = request.json

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }
    errorCode = 404

    # cek username ada atau engga
    emailExist = db.session.query(User).filter_by(email = body["email"]).scalar() is not None
    user = db.session.query(User).filter_by(email = body["email"]).first()

    if (emailExist and user.active) :
        try:
            user.serialise()
            if (decrypt(user.password) == body["password"]):
                nameForToken = (user.name.lower()).replace(" ","")
                data = {
                    # ini tokennya generate pake nama, ga unik.
                    "token" : generateToken(nameForToken),
                    "name" : user.name,
                    "id" : user.id,
                    "role": user.role
                }
                response["message"] = "Login berhasil"
                response["error"] = False
                response["data"] = data
                errorCode = 200
            else:
                response["message"] = "Password salah"
                errorCode = 401

        except Exception as e:
            response["message"] = str(e)

        finally:
            db.session.close()

    else:
        response["message"] = "Email tidak terdaftar atau sudah tidak aktif"
        errorCode = 401
    return jsonify(response), errorCode




#####################################################################################################
# UPDATE USER
#####################################################################################################
@router.route('/user/update/<id>', methods=['PUT'])
@verifyLogin
def updateUser(id):
    body = request.json

    body["password"] = encrypt(body["password"])
    
    name = body["name"]
    email = body["email"]
    password = body["password"]
    role = body["role"]
    active = body["active"]
    department = body["department"]

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    user = db.session.query(User).filter_by(id = id).first()
    
    if (user == False):
        response["message"] = "User belum terdaftar"
    else:
        try:            
            user.name = name.title()
            user.email = email
            user.password = password
            user.role = role
            user.active = active
            user.department = department.title()

            db.session.commit()

            response["message"] =  "User updated. User-id = {}".format(user.id)
            response["error"] = False
            response["data"] = user.returnToUser()
        except Exception as e:
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)



#####################################################################################################
# DELETE USER
#####################################################################################################
@router.route('/user/deleteUser/<id>', methods=['DELETE'])
@verifyLogin
def deleteUser(id):

    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # get user
    user = db.session.query(User).filter_by(id = id).scalar() is not None
    
    if (user == False):
        response["message"] = "User doesn't exist"
    else:
        try:            
            User.query.filter_by(id=id).delete()

            db.session.commit()

            response["message"] =  "User with id {} has been deleted".format(id)
            response["error"] = False
            response["data"] = ""
        except Exception as e:
            response["message"] = str(e)
        finally:
            db.session.close()

    
    return jsonify(response)






#####################################################################################################
# GET USER PER ID
#####################################################################################################
@router.route('/user/getUser/<id>')
@verifyLogin
def getUserById(id):
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    # cek username ada atau engga
    userExist = db.session.query(User).filter_by(id = id).scalar() is not None

    if (userExist == True) :
        try:
            user = User.query.filter_by(id = id).first()

            response["message"] ="User found"
            response["error"] = False
            response["data"] = (user.returnToUser())
        except Exception as e:
            response["message"] = str(e)
        finally:
            db.session.close()

    else :
        response["message"] = "User tidak ditemukan"

    return jsonify(response)



#####################################################################################################
# GET ALL USERS
#####################################################################################################
@router.route('/user/getAll')
@verifyLogin
def getAllUsers():
    response = {
        "error" : True,
        "message" : "",
        "data" : {}
    }

    try:
        userActve = User.query.order_by(User.name).all()

        data = ([e.returnToUser() for e in userActve])
        userActiveCount  = len(data)
        response["message"] = "User(s) found : " + str(userActiveCount)
        response["error"] = False
        response["data"] = data
    except Exception as e:
        response["message"] = str(e)
    finally:
        db.session.close()


    return jsonify(response)

