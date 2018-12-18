from flask import Flask
from config import Config
import json
import datetime
from bson.objectid import ObjectId
from pymodm import connect

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)

app.config.from_object(Config)
#mongo = PyMongo(app)


from app import main
app.json_encoder = JSONEncoder

#from app.controllers import *
