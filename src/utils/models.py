from datetime import datetime
from ..utils.crypt import encrypt, decrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Testing(db.Model):
    __tablename__ = 'testing'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    status_enabled = db.Column(db.Boolean(), default = True)  

    def __init__(self,name,id):
        self.name = name
        self.id = id

    # buat ngereturn npk nya
    def __repr__(self):
        return '<testing id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'name' : self.name
        }

    def returnToUser(self):

        return {
            'id' : self.id,
            'name' : self.name
        }

    def getName(self) :
        return self.name



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String())
    email  = db.Column(db.String())
    role  = db.Column(db.Boolean())
    department  = db.Column(db.String())
    password  = db.Column(db.String())
    active  = db.Column(db.Boolean(), default = True)  
    created_at = db.Column(db.DateTime, default =  datetime.now())


    def __init__(self,name,email,role,department,password,active,created_at):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.department = department
        self.active = active
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<user id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'role' : self.role,
            'department' : self.department,
            'password' : self.password,
            'active' : self.active,
            'created_at' : self.created_at
        }

    def returnToUser(self):
        print(self.role)
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'role' : self.role,
            'department' : self.department,
            'password' : decrypt(self.password),
            'active' : self.active,
            'created_at' : self.created_at
        }


class Guest(db.Model):
    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String())
    email  = db.Column(db.String())
    nik  = db.Column(db.String())
    institution  = db.Column(db.String())
    phoneNumber  = db.Column(db.String())
    arrivalTime = db.Column(db.DateTime)
    departureTime = db.Column(db.DateTime)
    ktpImage  = db.Column(db.String())
    signImage  = db.Column(db.String())
    active  = db.Column(db.Boolean(), default = True) 
    visitReason  = db.Column(db.String())

    def __init__(self,name,email,nik,institution,phoneNumber,arrivalTime,departureTime,ktpImage,signImage,active,visitReason):
        self.name = name
        self.email = email
        self.nik = nik
        self.institution = institution
        self.phoneNumber = phoneNumber
        self.arrivalTime = arrivalTime
        self.departureTime = departureTime
        self.ktpImage = ktpImage
        self.signImage = signImage
        self.active = active
        self.visitReason = visitReason


    # buat ngereturn nik nya
    def __repr__(self):
        return '<user nik {}>'.format(self.nik)

    def serialise(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'nik' : self.nik,
            'institution' : self.institution,
            'phoneNumber' : self.phoneNumber,
            'arrivalTime' : self.arrivalTime,
            'departureTime' : self.departureTime,
            'ktpImage' : self.ktpImage,
            'signImage' : self.signImage,
            'active' : self.active,
            'visitReason' : self.visitReason
        }

    def returnToGuest(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'nik' : self.nik,
            'institution' : self.institution,
            'phoneNumber' : self.phoneNumber,
            'arrivalTime' : str(self.arrivalTime),
            'departureTime' : str(self.departureTime),
            'ktpImage' : self.ktpImage,
            'signImage' : self.signImage,
            'active' : self.active,
            'visitReason' : self.visitReason
        }
