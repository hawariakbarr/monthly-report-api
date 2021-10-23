from flask import jsonify
from datetime import datetime

from sqlalchemy.sql.elements import Null
from ..utils.crypt import encrypt, decrypt

from flask_sqlalchemy import SQLAlchemy
import json, requests, datetime as datetm
from requests.auth import HTTPBasicAuth

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String())
    email  = db.Column(db.String())
    role  = db.Column(db.Boolean())
    phoneNumber  = db.Column(db.String())
    password  = db.Column(db.String())
    active  = db.Column(db.Boolean(), default = True)  
    created_at = db.Column(db.DateTime, default =  datetime.now())


    def __init__(self,name,email,role,phoneNumber,password,active,created_at):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.phoneNumber = phoneNumber
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
            'phoneNumber' : self.phoneNumber,
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
            'phoneNumber' : self.phoneNumber,
            'password' : decrypt(self.password),
            'active' : self.active,
            'created_at' : self.created_at
        }

class Opd(db.Model):
    __tablename__ = 'master_opd'

    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String())
    address  = db.Column(db.String())
    pic  = db.Column(db.String())
    phone_number  = db.Column(db.String())
    created_at = db.Column(db.DateTime, default =  datetime.now())
    uptd = db.relationship('Uptd', backref='master_opd', lazy=True)
    opd_insident = db.relationship('OpdInsident', backref='opd_insident', lazy=True)
    opd_link = db.relationship('OpdLink', backref='master_opd', lazy=True)

    def __init__(self,name,address,pic,phone_number, created_at):
        self.name = name
        self.address = address
        self.pic = pic
        self.phone_number = phone_number
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<opd id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'pic' : self.pic,
            'phone_number' : self.phone_number,
            'created_at' : self.created_at
        }

    def returnToOpd(self, param_uptd, start_date, end_date):
        # if opd_id is None:
        opd_link = OpdLink.query.filter_by(opd_id = self.id).all()
        opd_insident = OpdInsident.query.filter_by(opd_id = self.id).all()
        
        if param_uptd == "none" or param_uptd == "":
            uptd_list_data = []
        else:
            if param_uptd == "all":
                uptd_list_data = [item.returnToUptd(start_date, end_date) for item in self.uptd]
            else:
                uptd = Uptd.query.filter_by(id = param_uptd).first()
                uptd_list_data = uptd.returnToUptd(start_date, end_date)
        
        return {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'pic' : self.pic,
            'phone_number' : self.phone_number,
            'uptd_list': uptd_list_data,
            'opd_link': [e.returnOpdLink(start_date, end_date) for e in opd_link],
            'opd_insident': [e.returnToOpdInsident(start_date, end_date) for e in opd_insident],
            'created_at' : self.created_at
        }

class Uptd(db.Model):
    __tablename__ = 'master_uptd'

    id = db.Column(db.Integer, primary_key = True)
    opd_id  = db.Column(db.Integer, db.ForeignKey('master_opd.id'))
    name  = db.Column(db.String())
    address  = db.Column(db.String())
    pic  = db.Column(db.String())
    phone_number  = db.Column(db.String())
    opd = db.relationship('Opd', backref='opd_master', lazy=True)
    uptd_link = db.relationship('UptdLink', backref='master_opd', lazy=True)
    uptd_insident = db.relationship('UptdInsident', backref='uptd_insident', lazy=True)
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self,opd_id,name,address,pic,phone_number, created_at):
        self.opd_id = opd_id
        self.name = name
        self.address = address
        self.pic = pic
        self.phone_number = phone_number
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<opd id {}>'.format(self.id)

    def serialise(self):
        opd = Opd.query.filter_by(id = self.opd_id).first()
        return {
            'id' : self.id,
            'opd_id': self.opd_id,
            'opd_name' : opd.name,
            'name' : self.name,
            'address' : self.address,
            'pic' : self.pic,
            'phone_number' : self.phone_number,
            'created_at' : self.created_at
        }

    def returnToUptd(self, start_date, end_date):
        # if param_uptd is None:
        #     uptd_link_data = []
        # elif param_uptd == "all":
        uptd_link = UptdLink.query.filter_by(uptd_id = self.id).all()
        uptd_insident = UptdInsident.query.filter_by(uptd_id = self.id).all()
            
        #     uptd_link_data = [e.returnUptdLink() for e in uptd_link]
        # else:
        #     uptd_link = UptdLink.query.filter_by(uptd_id = uptd_id).first()
        #     uptd_link_data = uptd_link.returnUptdLink()
        return {
            'id' : self.id,
            'opd_id': self.opd_id,
            'name' : self.name,
            'address' : self.address,
            'pic' : self.pic,
            'phone_number' : self.phone_number,
            'uptd_link':[e.returnUptdLink(start_date, end_date) for e in uptd_link],
            'uptd_insident':[e.returnToUptdInsident(start_date, end_date) for e in uptd_insident],
            'created_at' : self.created_at
        }

class OpdLink(db.Model):
    __tablename__ = 'opd_link'

    id = db.Column(db.Integer, primary_key = True)
    prtg_id  = db.Column(db.Integer)
    opd_id  = db.Column(db.Integer, db.ForeignKey('master_opd.id'))
    isp_id  = db.Column(db.Integer, db.ForeignKey('master_isp.id'))
    band_id  = db.Column(db.Integer, db.ForeignKey('master_bandwith.id'))
    opd = db.relationship('Opd', backref='link_opd', lazy=True)
    isp = db.relationship('Isp', backref='isp_opd', lazy=True)
    bandwith = db.relationship('Bandwith', backref='bandwith_opd', lazy=True)
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self,prtg_id,opd_id,isp_id,band_id,created_at):
        self.prtg_id = prtg_id
        self.opd_id = opd_id
        self.isp_id = isp_id
        self.band_id = band_id
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<opdlink id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'prtg_id' : self.prtg_id,
            'opd_id': self.opd_id,
            'isp_id' : self.isp_id,
            'band_id' : self.band_id,
            'created_at' : self.created_at
        }

    def get_max_min(self, prtg_id, start_date, end_date, isp):
        if prtg_id == 0:
            return None

        response = {
            "error" : True,
            "message" : "",
            "data" : {}
        }

        try:
            # session = requests.Session()
            # session.trust_env = False
            username = "prtgadmin"
            passhash = 4220473478
            response_data = requests.get('https://noc.jabarprov.go.id/api/historicdata.json?username={}&passhash={}&id={}&avg=0&sdate={}&edate={}&usecaption=1&avg=3600'.format(username, passhash, prtg_id, start_date, end_date), verify=False)
            print(response_data.elapsed.total_seconds())

            #icon = speed in
            #lintas speed out
            arr_data = []
            arr_avg = []
            resp_json = response_data.json()
            

            if isp == 'Aplikanusa Lintasarta' or isp == 'Mora Telematika Indonesia':
                for data in resp_json['histdata']:
                    # if (data['Traffic Out (speed)'] * 8 / 1000) < 1000:
                    trf_out = 0 if data['Traffic Out (speed)'] == '' else data['Traffic Out (speed)']
                    trf_tot = 0 if data['Traffic Total (speed)'] == '' else data['Traffic Total (speed)']
                    if trf_out != 0:
                        arr_data.append(trf_out)
                    if trf_tot != 0:
                        arr_avg.append(trf_tot)
                    # else:
                        # arr_data.append(data['Traffic Out (speed)'] * 8 /1000000)
            elif isp == 'Icon Commnet Plus':
                for data in resp_json['histdata']:
                    # if (data['Traffic In (speed)'] * 8 / 1000) < 1000:
                    trf_in = 0 if data['Traffic In (speed)'] == '' else data['Traffic In (speed)']
                    trf_tot = 0 if data['Traffic Total (speed)'] == '' else data['Traffic Total (speed)']
                    
                    if trf_in != 0:
                        arr_data.append(trf_in)
                    if trf_tot != 0:
                        arr_avg.append(trf_tot)
                    # else:
                    #     arr_data.append(data['Traffic In (speed)'] * 8 /1000000)
            avg_speed = 0 if len(arr_avg) == 0 else sum(arr_avg) / len(arr_avg)
            if avg_speed == 0:
                data = {'max_speed': 0,'min_speed': 0,'avg_speed': avg_speed}
            else:
                data = {'max_speed': max(arr_data),'min_speed': min(arr_data),'avg_speed': avg_speed}
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
            data = None
        return data

    def get_prop_report(self, prtg_id, start_date, end_date):
        if prtg_id == 0:
            return None
        #prtg_id -> jadi id yg ngebedain setiap opd/uptd
        #daily -> ambil awal jam di hari ini sampe akhir jam di hari ini/awal jam di hari besok. contoh : 9/27/2021 00:00 - 9/28/2020 00:00
        #monthly -> ambil tanggal di awal bulan yg lg running ambil di jam awal juga sampe di tanggal awal di bulan depan dari bulang skrg yg lg running di jam awal juga. contoh 01.08.2021 00:00 - 01.09.2021 00:00
        #average interval -> ambil 60 minutes/ hour aja (default)

        # contoh url hasil dari 4 
        # https://noc.jabarprov.go.id/historicdata_html.htm?id=17385&sdate=2021-09-27-00-00-00&edate=2021-09-28-00-00-00&avg=3600&pctavg=300&pctshow=false&pct=95&pctmode=false
        response = {
            "error" : True,
            "message" : "",
            "data" : {}
        }
        try:

            username = "prtgadmin"
            passhash = 4220473478
            graph = "https://noc.jabarprov.go.id/chart.svg?username={}&passhash={}&graphid=-1&id={}&avg=3600&sdate={}&edate={}&clgid=&width=1000&height=400&graphstyling=baseFontSize=%2715%27%20showLegend=%271%27%20tooltexts=%273%27&refreshable=true%22".format(username, passhash, prtg_id, start_date, end_date)

            # 421029.3218byte to bit = di kali 8 = 3368234.5744
            # 3368234.5744 bit to kilobit = dibagi 1000  = 3368.2345744 kbps

            # goalsnya  :
            # data upto 1000Kbps -> convert ke Mbps
            # data < 1000Kbps -> stay di Kbps
            max_min_speed = self.get_max_min(prtg_id, start_date, end_date, self.isp.name)
            if (max_min_speed['max_speed'] * 8 / 1000) < 1000:
                max_speed = str(round(max_min_speed['max_speed'] * 8 / 1000, 3)) + ' Kbps'
            else:
                max_speed = str(round(max_min_speed['max_speed'] * 8 / 1000000, 3)) + ' Mbps'

            if (max_min_speed['min_speed'] * 8 / 1000) < 1000:
                min_speed = str(round(max_min_speed['min_speed'] * 8 / 1000, 3)) + ' Kbps'
            else:
                min_speed = str(round(max_min_speed['min_speed'] * 8 / 1000000, 3)) + ' Mbps'
                
            if (max_min_speed['avg_speed'] * 8 / 1000) < 1000:
                average = str(round(max_min_speed['avg_speed'] * 8 / 1000, 3)) + ' Kbps'
            else:
                average = str(round(max_min_speed['avg_speed'] * 8 / 1000000, 3)) + ' Mbps'
            
            #TODO: pisahin fucntion untuk get properti image. krn terlalu riskan untuk disatuin sama properti yg ada logiknya
            data = {
                'graph' : graph,
                'speed_average' : average,
                'max_speed': max_speed,
                'min_speed': min_speed
            }
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
            data = None
        return data
        
    def returnOpdLink(self, start_date, end_date):
        if self.prtg_id == 0:
            return None
        data_prop = self.get_prop_report(self.prtg_id, start_date, end_date)
        if data_prop == None:
            return {
                'prtg_id' : self.prtg_id,
                'isp':self.isp.name,
                'bandwith':self.bandwith.bandwith,
                'graph': '',
                'max_speed': 0,
                'min_speed': 0,
                'speed_average': 0
            }
        return {
            'prtg_id' : self.prtg_id,
            'isp':self.isp.name,
            'bandwith':self.bandwith.bandwith,
            'graph': data_prop['graph'],
            'max_speed': data_prop['max_speed'],
            'min_speed': data_prop['min_speed'],
            'speed_average': data_prop['speed_average']
        }

    def returnAllOpdLink(self):
        link_opd = Opd.query.filter_by(id = self.opd_id).first()
        return {
            'id' : self.id,
            'prtg_id' : self.prtg_id,
            'opd_id' : link_opd.id,
            'isp_id' : self.isp_id,
            'isp':self.isp.name,
            'opd_name':link_opd.name,
            'band_id':self.band_id,
            'bandwith':self.bandwith.bandwith
        }

class UptdLink(db.Model):
    __tablename__ = 'uptd_link'

    id = db.Column(db.Integer, primary_key = True)
    prtg_id  = db.Column(db.Integer)
    uptd_id  = db.Column(db.Integer, db.ForeignKey('master_uptd.id'))
    isp_id  = db.Column(db.Integer, db.ForeignKey('master_isp.id'))
    band_id  = db.Column(db.Integer, db.ForeignKey('master_bandwith.id'))
    isp = db.relationship('Isp', backref='isp_uptd', lazy=True)
    bandwith = db.relationship('Bandwith', backref='bandwith_uptd', lazy=True)
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self,prtg_id,uptd_id,isp_id,band_id,created_at):
        self.prtg_id = prtg_id
        self.uptd_id = uptd_id
        self.isp_id = isp_id
        self.band_id = band_id
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<uptdlink id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'prtg_id' : self.prtg_id,
            'uptd_id': self.uptd_id,
            'isp_id' : self.isp_id,
            'band_id' : self.band_id,
            'created_at' : self.created_at
        }

    def get_max_min(self, prtg_id, start_date, end_date, isp):
        if prtg_id == 0:
            return None

        response = {
            "error" : True,
            "message" : "",
            "data" : {}
        }

        try:
            # session = requests.Session()
            # session.trust_env = False
            username = "prtgadmin"
            passhash = 4220473478
            response_data = requests.get('https://noc.jabarprov.go.id/api/historicdata.json?username={}&passhash={}&id={}&avg=0&sdate={}&edate={}&usecaption=1&avg=3600'.format(username, passhash, prtg_id, start_date, end_date), verify=False)
            print(response_data.elapsed.total_seconds())

            #icon = speed in
            #lintas speed out
            arr_data = []
            arr_avg = []
            resp_json = response_data.json()
            

            if isp == 'Aplikanusa Lintasarta' or isp == 'Mora Telematika Indonesia':
                for data in resp_json['histdata']:
                    # if (data['Traffic Out (speed)'] * 8 / 1000) < 1000:
                    trf_out = 0 if data['Traffic Out (speed)'] == '' else data['Traffic Out (speed)']
                    trf_tot = 0 if data['Traffic Total (speed)'] == '' else data['Traffic Total (speed)']
                    if trf_out != 0:
                        arr_data.append(trf_out)
                    if trf_tot != 0:
                        arr_avg.append(trf_tot)
                    # else:
                        # arr_data.append(data['Traffic Out (speed)'] * 8 /1000000)
            elif isp == 'Icon Commnet Plus':
                for data in resp_json['histdata']:
                    # if (data['Traffic In (speed)'] * 8 / 1000) < 1000:
                    trf_in = 0 if data['Traffic In (speed)'] == '' else data['Traffic In (speed)']
                    trf_tot = 0 if data['Traffic Total (speed)'] == '' else data['Traffic Total (speed)']
                    
                    if trf_in != 0:
                        arr_data.append(trf_in)
                    if trf_tot != 0:
                        arr_avg.append(trf_tot)
                    # else:
                    #     arr_data.append(data['Traffic In (speed)'] * 8 /1000000)
            avg_speed = 0 if len(arr_avg) == 0 else sum(arr_avg) / len(arr_avg)
            if avg_speed == 0:
                data = {'max_speed': 0,'min_speed': 0,'avg_speed': avg_speed}
            else:
                data = {'max_speed': max(arr_data),'min_speed': min(arr_data),'avg_speed': avg_speed}
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
            data = None
        return data

    def get_prop_report(self, prtg_id, start_date, end_date):
        if prtg_id == 0:
            return None
        #prtg_id -> jadi id yg ngebedain setiap opd/uptd
        #daily -> ambil awal jam di hari ini sampe akhir jam di hari ini/awal jam di hari besok. contoh : 9/27/2021 00:00 - 9/28/2020 00:00
        #monthly -> ambil tanggal di awal bulan yg lg running ambil di jam awal juga sampe di tanggal awal di bulan depan dari bulang skrg yg lg running di jam awal juga. contoh 01.08.2021 00:00 - 01.09.2021 00:00
        #average interval -> ambil 60 minutes/ hour aja (default)

        # contoh url hasil dari 4 
        # https://noc.jabarprov.go.id/historicdata_html.htm?id=17385&sdate=2021-09-27-00-00-00&edate=2021-09-28-00-00-00&avg=3600&pctavg=300&pctshow=false&pct=95&pctmode=false
        response = {
            "error" : True,
            "message" : "",
            "data" : {}
        }
        try:

            username = "prtgadmin"
            passhash = 4220473478
            graph = "https://noc.jabarprov.go.id/chart.svg?username={}&passhash={}&graphid=-1&id={}&avg=3600&sdate={}&edate={}&clgid=&width=1000&height=400&graphstyling=baseFontSize=%2715%27%20showLegend=%271%27%20tooltexts=%273%27&refreshable=true%22".format(username, passhash, prtg_id, start_date, end_date)

            # 421029.3218byte to bit = di kali 8 = 3368234.5744
            # 3368234.5744 bit to kilobit = dibagi 1000  = 3368.2345744 kbps

            # goalsnya  :
            # data upto 1000Kbps -> convert ke Mbps
            # data < 1000Kbps -> stay di Kbps
            max_min_speed = self.get_max_min(prtg_id, start_date, end_date, self.isp.name)
            if (max_min_speed['max_speed'] * 8 / 1000) < 1000:
                max_speed = str(round(max_min_speed['max_speed'] * 8 / 1000, 3)) + ' Kbps'
            else:
                max_speed = str(round(max_min_speed['max_speed'] * 8 / 1000000, 3)) + ' Mbps'

            if (max_min_speed['min_speed'] * 8 / 1000) < 1000:
                min_speed = str(round(max_min_speed['min_speed'] * 8 / 1000, 3)) + ' Kbps'
            else:
                min_speed = str(round(max_min_speed['min_speed'] * 8 / 1000000, 3)) + ' Mbps'
                
            if (max_min_speed['avg_speed'] * 8 / 1000) < 1000:
                average = str(round(max_min_speed['avg_speed'] * 8 / 1000, 3)) + ' Kbps'
            else:
                average = str(round(max_min_speed['avg_speed'] * 8 / 1000000, 3)) + ' Mbps'

            data = {
                'graph' : graph,
                'speed_average' : average,
                'max_speed': max_speed,
                'min_speed': min_speed
            }
        except Exception as e:
            response["error"] = True
            response["status_code"] = 500
            response["message"] = str(e)
            data = None
        return data

    def returnUptdLink(self, start_date, end_date):
        if self.prtg_id == 0:
            return None
        data_prop = self.get_prop_report(self.prtg_id, start_date, end_date)
        if data_prop == None:
            return {
                'uptd_id':self.uptd_id,
                'prtg_id' : self.prtg_id,
                'isp':self.isp.name,
                'bandwith':self.bandwith.bandwith,
                'graph': '',
                'max_speed': 0,
                'min_speed': 0,
                'speed_average': 0
            }
        return {
            'uptd_id':self.uptd_id,
            'prtg_id' : self.prtg_id,
            'isp':self.isp.name,
            'bandwith':self.bandwith.bandwith,
            'graph': data_prop['graph'],
            'max_speed': data_prop['max_speed'],
            'min_speed': data_prop['min_speed'],
            'speed_average': data_prop['speed_average']
        }

    def returnAllUptdLink(self):
        link_uptd = Uptd.query.filter_by(id = self.uptd_id).first()
        return {
            'id' : self.id,
            'prtg_id' : self.prtg_id,
            'uptd_id' : link_uptd.id,
            'isp_id':self.isp_id,
            'isp':self.isp.name,
            'uptd_name':link_uptd.name,
            'band_id':self.band_id,
            'bandwith':self.bandwith.bandwith
        }

class Bandwith(db.Model):
    __tablename__ = 'master_bandwith'

    id = db.Column(db.Integer, primary_key = True)
    bandwith  = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self,bandwith,created_at):
        self.bandwith = bandwith,
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<band id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'bandwith' : self.bandwith,
            'created_at' : self.created_at
        }

    def returnToBandwith(self):
        return {
            'id' : self.id,
            'bandwith' : self.bandwith,
            'created_at' : self.created_at
        }

class Isp(db.Model):
    __tablename__ = 'master_isp'

    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String())
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self,name,created_at):
        self.name = name,
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<isp id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'created_at' : self.created_at
        }

    def returnToIsp(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'created_at' : self.created_at
        }

class Complaint(db.Model):
    __tablename__ = 'master_complaint'

    id = db.Column(db.Integer, primary_key = True)
    category  = db.Column(db.String())
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self,category,created_at):
        self.category = category,
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<isp id {}>'.format(self.id)

    def serialise(self):
        return {
            'id' : self.id,
            'category' : self.category,
            'created_at' : self.created_at
        }

    def returnToComplaint(self):
        return {
            'id' : self.id,
            'category' : self.category,
            'created_at' : self.created_at
        }

class OpdInsident(db.Model):
    __tablename__ = 'opd_insident'

    id = db.Column(db.Integer, primary_key = True)
    opd_id  = db.Column(db.Integer, db.ForeignKey('master_opd.id'))
    month = db.Column(db.Integer)
    comp_id = db.Column(db.Integer, db.ForeignKey('master_complaint.id'))
    amount = db.Column(db.Integer)
    complaint = db.relationship('Complaint', backref='complaint_opd', lazy=True)
    opd = db.relationship('Opd', backref='opd', lazy=True)
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self, opd_id, month, comp_id, amount, created_at):
        self.opd_id = opd_id,
        self.month = month,
        self.comp_id = comp_id,
        self.amount = amount,
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<isp id {}>'.format(self.id)

    def serialise(self):
        opd = Opd.query.filter_by(id = self.opd_id).first()
        complaint = Complaint.query.filter_by(id = self.comp_id).first()
        return {
            'id' : self.id,
            'opd_id' : self.opd_id,
            'comp_id' : self.comp_id,
            'opd_name': opd.name,
            'month' : self.month,
            'amount' : self.amount,
            'complaint': complaint.category,
            'created_at' : self.created_at
        }

    def returnToOpdInsident(self, start_date, end_date):
        st_date = datetm.datetime.strptime(start_date, "%Y-%m-%d-%H-%M-%S")    
        ed_date = datetm.datetime.strptime(end_date, "%Y-%m-%d-%H-%M-%S")
        # rg_date = range(int(st_date.month), int(ed_date.month))
        if self.month >= int(st_date.month) or self.month <= int(ed_date.month):
            return {
                'month' : self.month,
                'comp_id' : self.comp_id,
                'amount' : self.amount,
                'complaint':self.complaint.category,
                'created_at' : self.created_at
            }
        else: return None
            

class UptdInsident(db.Model):
    __tablename__ = 'uptd_insident'

    id = db.Column(db.Integer, primary_key = True)
    uptd_id  = db.Column(db.Integer, db.ForeignKey('master_uptd.id'))
    month = db.Column(db.Integer)
    comp_id = db.Column(db.Integer, db.ForeignKey('master_complaint.id'))
    amount = db.Column(db.Integer)
    complaint = db.relationship('Complaint', backref='complaint_uptd', lazy=True)
    uptd = db.relationship('Uptd', backref='uptd', lazy=True)
    created_at = db.Column(db.DateTime, default =  datetime.now())

    def __init__(self, uptd_id, month, comp_id, amount, created_at):
        self.uptd_id = uptd_id,
        self.month = month,
        self.comp_id = comp_id,
        self.amount = amount,
        self.created_at = created_at

    # buat ngereturn npk nya
    def __repr__(self):
        return '<isp id {}>'.format(self.id)

    def serialise(self):
        uptd = Uptd.query.filter_by(id = self.uptd_id).first()
        complaint = Complaint.query.filter_by(id = self.comp_id).first()
        return {
            'id' : self.id,
            'uptd_id' : self.uptd_id,
            'month' : self.month,
            'comp_id' : self.comp_id,
            'amount' : self.amount,
            'uptd_name': uptd.name,
            'complaint': complaint.category,
            'created_at' : self.created_at
        }

    def returnToUptdInsident(self, start_date, end_date):
        st_date = datetm.datetime.strptime(start_date, "%Y-%m-%d-%H-%M-%S")    
        ed_date = datetm.datetime.strptime(end_date, "%Y-%m-%d-%H-%M-%S")
        # rg_date = range(int(st_date.month), int(ed_date.month))
        if self.month >= int(st_date.month) or self.month <= int(ed_date.month):
            return {
                'month' : self.month,
                'comp_id' : self.comp_id,
                'amount' : self.amount,
                'complaint':self.complaint.category,
                'created_at' : self.created_at
            }
        else: return None  

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
