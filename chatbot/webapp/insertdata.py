from config import Config
from app.models import Agent, Question_answer, Quiz, Course
from pymodm import connect
import json
#connect(Config.Mongo_URI)
# get the agent data from file and store it into data variable which is of type list
with open('agent_record.json') as json_file:
    data = json.load(json_file)
print(data)
print(type(data))
print(data[0]['course_id'])
print(type(data[0]))
print(len(data))
for i in range(len(data)):
    print(data[i])
    print(data[i]['course_id'])
# connect to database and insert record into database
connect(Config.MONGO_URI)
for i in range(len(data)):
    try:
        agent = Agent.objects.get({'course_id':data[i]['course_id']})
        print(agent)
    except Agent.DoesNotExist:
        agent = Agent(course_id=data[i]['course_id'], file_name=data[i]['file_name'], project_id=data[i]['project_id']).save()
        print(agent)
        #print(type(data))

# get the quiz record into quiz_data variable
with open('quiz_record.json') as json_file:
    quiz_data = json.load(json_file)

print(quiz_data)
connect(Config.MONGO_URI)
try:
    #query to see if quiz record is already in Course or not
    print("Test inside try block")
    course = Course.objects.get({'course_id':'CSUEB','quiz.q_id':1})
    print(course)
except Course.DoesNotExist:
    print("Test inside except block")
    #course = Course.objects.get({'course_id':'CSUEB'})
    # quizData=[{"quiz_id":1, "qa":quiz_data}]
    #course.quiz=quizData
    for i in range(len(quiz_data)):
        try:
            course = Course.objects.get({'course_id':'CSUEB','quiz.q_id':1})
            Course.objects.raw({"course_id":"CSUEB","quiz.q_id":1}).update({ "$push":{"quiz.$.qa":{"$each":[{"question_id":quiz_data[i]['question_id'],
                                                                                                      "question": quiz_data[i]['question'],
                                                                                                      "answer": quiz_data[i]['answer']}] } } })
        except Course.DoesNotExist:
            Course.objects.raw({"course_id":"CSUEB"}).update({"$push":{"quiz":{"$each":[{"q_id":1,
                                                                                         "qa": [ {"question_id":quiz_data[i]['question_id'],
                                                                                                  "question": quiz_data[i]['question'],
                                                                                                  "answer": quiz_data[i]['answer']} ]}]} }})


try:
    #query to see if quiz record is already in Course or not
    print("Test inside try block")
    course = Course.objects.get({'course_id':'CSUEB','quiz.q_id':2})
    print(course)
except Course.DoesNotExist:
    print("Test inside except block")
    #course = Course.objects.get({'course_id':'CSUEB'})
    # quizData=[{"quiz_id":1, "qa":quiz_data}]
    #course.quiz=quizData
    for i in range(len(quiz_data)):
        try:
            course = Course.objects.get({'course_id':'CSUEB','quiz.q_id':2})
            Course.objects.raw({"course_id":"CSUEB","quiz.q_id":2}).update({ "$push":{"quiz.$.qa":{"$each":[{"question_id":quiz_data[i]['question_id'],
                                                                                                      "question": quiz_data[i]['question'],
                                                                                                      "answer": quiz_data[i]['answer']}] } } })
        except Course.DoesNotExist:
            Course.objects.raw({"course_id":"CSUEB"}).update({"$push":{"quiz":{"$each":[{"q_id":2,
                                                                                         "qa": [ {"question_id":quiz_data[i]['question_id'],
                                                                                                  "question": quiz_data[i]['question'],
                                                                                                  "answer": quiz_data[i]['answer']} ]}]} }})
