from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern
#from app import mongo
from pymodm import connect
from app import app

connect(app.config['MONGO_URI'])

class QA_pair(MongoModel):
    question=fields.CharField()
    answer=fields.CharField()
    class Meta:
        write_concern = WriteConcern(j=True)
