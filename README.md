# nda_project

https://phoenixnap.com/kb/install-flask

py -m pip install virtualenv
mkdir project
cd project

py -m venv .\

---
settings.json
{
    "window.zoomLevel": -1,
    "json.schemas": [
    
    ],
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
          "source": "PowerShell",
          "icon": "terminal-powershell",
          "args": ["-ExecutionPolicy", "Bypass"]
        }
      },
      "terminal.integrated.defaultProfile.windows": "PowerShell"
}
---

pip install flask
pip install jwt
pip install flask_sqlalchemy
pip install pymysql
pip install pyjwt



============================
TABLE:
============================
user
---------------
pk:id
name
email
role
department
password
active
created_at

guest
----------------
pk:id
name
email
nik
institution
phoneNumber
arrivalTime
departureTime
ktpImage
signImage
active
visitReason

============================


eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiMGx6MDkiLCJleHAiOjE2MzEzNzQ1NzQsImlhdCI6MTYzMTI4OTk3NH0.gdmXJ548qRJwg_trswINHzOZdpntm3cWBdTn8zDuSAk
