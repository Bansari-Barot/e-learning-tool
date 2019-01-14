from pymodm import MongoModel, fields, EmbeddedMongoModel
from pymongo.write_concern import WriteConcern
#from app import mongo
from pymodm import connect
from app import app


connect(app.config['MONGO_URI'])

class Chat(EmbeddedMongoModel):
    question=fields.CharField()
    answer=fields.CharField()

class Chat_History(EmbeddedMongoModel):
    datetimestamp=fields.DateTimeField()
    c_id=fields.CharField()
    chats=fields.EmbeddedDocumentListField(Chat)

class Student(EmbeddedMongoModel):
    name=fields.CharField()
    email_id=fields.CharField()
    chat_history=fields.EmbeddedDocumentListField(Chat_History)


class Course(MongoModel):
    course_id=fields.CharField()
    course_name=fields.CharField()
    textbook=fields.URLField()
    topics=fields.ListField()
    students=fields.EmbeddedDocumentListField(Student)
