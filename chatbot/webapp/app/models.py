from pymodm import MongoModel, fields, EmbeddedMongoModel

class Chat(EmbeddedMongoModel):
    question=fields.CharField()
    answer=fields.CharField()

class Chat_History(EmbeddedMongoModel):
    datetimestamp=fields.DateTimeField()
    c_id=fields.CharField()
    chats=fields.EmbeddedDocumentListField(Chat)

class Answers(EmbeddedMongoModel):
    answer=fields.CharField()
    points=fields.IntegerField()
    suggestion=fields.CharField()

class Feedback(EmbeddedMongoModel):
    question_id=fields.IntegerField()
    question=fields.CharField()
    answers=fields.EmbeddedDocumentListField(Answers)

class Quiz_record(EmbeddedMongoModel):
    datetimestamp=fields.DateTimeField()
    tid=fields.CharField()
    quiz_id=fields.IntegerField()
    score=fields.IntegerField()
    feedbacks=fields.EmbeddedDocumentListField(Feedback)

class Student(EmbeddedMongoModel):
    name=fields.CharField()
    email_id=fields.CharField()
    chat_history=fields.EmbeddedDocumentListField(Chat_History)
    net_id = fields.CharField()
    role=fields.CharField()
    quiz_result=fields.EmbeddedDocumentListField(Quiz_record)

class Question_answer(EmbeddedMongoModel):
    question_id=fields.IntegerField()
    question=fields.CharField()
    answer=fields.CharField()

class Quiz(EmbeddedMongoModel):
    q_id=fields.IntegerField()
    qa=fields.EmbeddedDocumentListField(Question_answer)

class Course(MongoModel):
    course_id=fields.CharField()
    course_name=fields.CharField()
    textbook=fields.URLField()
    topics=fields.ListField()
    students=fields.EmbeddedDocumentListField(Student)
    quiz=fields.EmbeddedDocumentListField(Quiz)

class Agent(MongoModel):
    course_id=fields.CharField()
    file_name=fields.CharField()
    project_id=fields.CharField()
