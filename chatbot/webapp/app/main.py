from flask import session,request, render_template,jsonify
from app import app
import dialogflow
import os
import requests
from config import Config
import json
import dialogflow_v2beta1
from app.models import Chat, Chat_History, Student, Course, Agent
from pymodm import connect
from flask_pymongo import PyMongo
import datetime
from bson.tz_util import utc, FixedOffset
import datetime
from os.path import dirname, abspath
from google.auth._default import _load_credentials_from_file
from app import socketio
from flask_socketio import send, emit
import random
import ast

@app.route('/test_assessment', methods=['GET','POST'])
def test_assessment():
    # first check if in request there is already list of question_pool
    #data = request.form['question_pool']
    #data = request.form
    if request.form.get('question_pool'):
        # if there is question pool then from then pool get the first question from that pool
        email_id=request.form['email_id']
        name=request.form['name']
        course_id=request.form['course_id']
        question_pool=request.form['question_pool']
        course_name=request.form['course_name']
        role=request.form['role']
        net_id=request.form['net_id']
        quiz_id=int(request.form['quiz_id'])
        currentQ=int(request.form['currentQ'])
        currentQ += 1
        totalQ=request.form['totalQ']
        question_pool = ast.literal_eval(question_pool)
        if (len(question_pool)):
            connect(app.config['MONGO_URI'])
            quiz_all = Course.objects.select_related('quiz').get({"course_id":course_id}).quiz
            quiz_req = [x.qa for x in quiz_all if x.q_id == quiz_id]
            question_id = question_pool.pop(0)
            question = [x.question for x in quiz_req[0] if x.question_id == question_id]
            print(question)
            return render_template('test_assessment.html', role=role,name=name, net_id=net_id,
                                                           email_id=email_id, course_id=course_id, course_name=course_name,
                                                           question_pool=question_pool, question=question[0],
                                                           question_id=question_id, quiz_id=quiz_id,
                                                           totalQ=totalQ, currentQ=currentQ)
        return render_template('test_assessment.html',role=role,name=name, net_id=net_id,
                                email_id=email_id, course_id=course_id, course_name=course_name,
                                totalQ=totalQ, currentQ=currentQ)
    # if there is not any question pool then based on quiz id get all the question
    # here there should be proper query but as of now its a temporary fix to count the number of question in given quiz
    email_id=request.form['email_id']
    name=request.form['name']
    course_id=request.form['course_id']
    course_name=request.form['course_name']
    role=request.form['role']
    net_id=request.form['net_id']
    quiz_id=1
    connect(app.config['MONGO_URI'])
    # query to select all the quiz given course_id
    quiz_all = Course.objects.select_related('quiz').get({"course_id":course_id}).quiz
    # query to get particular quiz given q_id
    quiz_req = [x.qa for x in quiz_all if x.q_id == quiz_id]
    # count the total number of question in a quiz
    totalQ= len(quiz_req[0])
    #num_of_question = len(course.quiz[0].qa)
    question_pool = []
    for i in range(totalQ):
        question_pool.append(i+1)
    random.shuffle(question_pool)
    #from question_pool pop first q_id and get that question from db and and return the template with question, question_id & question_pool
    question_id = question_pool.pop(0)
    question = [x.question for x in quiz_req[0] if x.question_id == question_id]
    question_pool = str(question_pool)
    return render_template('test_assessment.html', role=role,name=name, net_id=net_id,
                                                   email_id=email_id, course_id=course_id, course_name=course_name,
                                                   question_pool=question_pool, question=question[0],
                                                   question_id=question_id, quiz_id=quiz_id,
                                                   totalQ=totalQ, currentQ=1)


#LTI arguments by BB
@app.route('/', methods=['GET','POST'])
def index():
    if request.form:
        info_user=request.form
        if info_user.get('lis_person_name_full'):
            name=info_user['lis_person_name_full']
        else:
            name=info_user['name']
        if info_user.get('roles'):
            role=info_user['roles']
        else:
            role=info_user['role']
        if info_user.get('context_label'):
            course_id=info_user['context_label']
        else:
            course_id=info_user['course_id']
        if info_user.get('lis_person_sourcedid'):
            net_id=info_user['lis_person_sourcedid']
        else:
            net_id=info_user['net_id']
        if info_user.get('context_title'):
            course_name=info_user['context_title']
        else:
            course_name=info_user['course_name']
        if info_user.get('lis_person_contact_email_primary'):
            email_id=info_user['lis_person_contact_email_primary']
        else:
            email_id=info_user['email_id']
        currentTime=datetime.datetime.now()
        greeting=""
        if currentTime.hour<12:
            greeting="Good morning"
        elif 12<= currentTime.hour <18:
            greeting="Good afternoon"
        else:
            greeting="Good evening"
        connect(app.config['MONGO_URI'])


    # Here first check whether course is there in db or not and if not then in except add that course,student into db
        try:
            course = Course.objects.get({'course_id':course_id})
            print(course)
            # Second check whether the students is exist inside the course or not if not then in except add students into that
            # course
            try:
                user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
                course_info = {"name": name, "email_id": email_id, "course_id": course_id}
                return render_template('index.html',role=role,name=name, net_id=net_id,
                                        email_id=email_id, course_id=course_id, course_name=course_name, greeting=greeting)
            except Course.DoesNotExist:
                course_info = {"name": name, "email_id": email_id, "course_id": course_id}
                Course.objects.raw({"course_id":course_id}).update(
                    { "$push":{"students": { "$each": [{'name':name,'email_id':email_id, 'net_id':net_id}] } } } )
                user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
                st = str(user.students)
                return render_template('index.html',role=role,name=name, net_id=net_id,
                                        email_id=email_id, course_id=course_id, course_name=course_name,greeting=greeting)

        except Course.DoesNotExist:
            student = Student(name=name, email_id=email_id, net_id=net_id,role=role)
            course = Course(course_id=course_id,course_name=course_name,
                            textbook="https://drive.google.com/file/d/14pTf5ZZ79HMSQVt4wfKtdLYVFowDlSvt/view?usp=sharing",
                            topics=["MS Office","LinkedIn learning"], students=[student]).save()
            course = Course.objects.get({'course_id':course_id})
            print(course)
            course_info = {"name": name, "email_id": email_id, "course_id": course_id}
            return render_template('index.html',role=role,name=name, net_id=net_id,
                                    email_id=email_id, course_id=course_id, course_name=course_name,greeting=greeting)
    else:
        return render_template('login.html')
        #return render_template('index.html',role=role,name= "bansri", email_id= "bansri.barot72@gmail.com", course_id= "CSUEB", course_name="CSUEB generic Q/A")

@app.route('/login', methods=['GET','POST'])
def guest_login():

    name=request.form['name']
    role="guest"
    course_id="CSUEB"
    net_id=request.form['net_id']
    course_name="CSUEB General Questions"
    email_id =request.form['email_id']
    currentTime=datetime.datetime.now()
    greeting=""
    if currentTime.hour<12:
        greeting="Good morning"
    elif 12<= currentTime.hour <18:
        greeting="Good afternoon"
    else:
        greeting="Good evening"
    connect(app.config['MONGO_URI'])


# Here first check whether course is there in db or not and if not then in except add that course,student into db
    try:
        course = Course.objects.get({'course_id':course_id})
        print(course)
        # Second check whether the students is exist inside the course or not if not then in except add students into that
        # course
        try:
            user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
            course_info = {"name": name, "email_id": email_id, "course_id": course_id}
            return render_template('index.html',role=role,name= name, net_id=net_id,
                                    email_id= email_id, course_id= course_id, course_name=course_name,greeting=greeting)
        except Course.DoesNotExist:
            course_info = {"name": name, "email_id": email_id, "course_id": course_id}
            Course.objects.raw({"course_id":course_id}).update(
                { "$push":{"students": { "$each": [{'name':name,'email_id':email_id, 'net_id':net_id}] } } } )
            user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
            st = str(user.students)
            return render_template('index.html',role=role,name= name, net_id=net_id,
                                    email_id= email_id, course_id= course_id, course_name=course_name,greeting=greeting)

    except Course.DoesNotExist:
        student = Student(name=name, email_id=email_id, net_id=net_id, role=role)
        course = Course(course_id=course_id,course_name=course_name,students=[student]).save()
        course = Course.objects.get({'course_id':course_id})
        print(course)
        course_info = {"name": name, "email_id": email_id, "course_id": course_id}
        return render_template('index.html',role=role,name= name, net_id=net_id,
                                email_id= email_id, course_id= course_id, course_name=course_name,greeting=greeting)



def detect_intent_texts(session_id, text, language_code, course_id):
        # connect to db to get the name of agent file for course id
        connect(app.config['MONGO_URI'])
        agent = Agent.objects.get({'course_id':course_id})
        file_name = agent.file_name
        print(file_name)
        path_to_file = dirname(dirname(abspath(__file__))) + file_name
        print(path_to_file)
        # set that file as google application credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path_to_file
        project_id = agent.project_id
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        if text:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = session_client.detect_intent(
                session=session, query_input=query_input)

            return response.query_result.fulfillment_text

def send_message(question, sid, name, email_id, course_id, date):

    fulfillment_text = detect_intent_texts("unique", question, 'en', course_id)
    response_text = { "message":  fulfillment_text, "name": name }
    #add QA into db - update query_input
    connect(app.config['MONGO_URI'])

    try:
        user = Course.objects.get({"students.chat_history.c_id":sid})
        Course.objects.raw({"course_id":course_id, "students.email_id":email_id,"students.chat_history.c_id":sid}).update(
           { "$push":{"students.$.chat_history.0.chats": { "$each": [{ "question":question, "answer":fulfillment_text }] }}})

    except Course.DoesNotExist:
        Course.objects.raw({ "course_id":course_id, "students.email_id":email_id }).update(
            { "$push":{"students.$.chat_history": {"$each":[{"datetimestamp" : date,
                                                             "c_id":sid,
                                                             "chats" : [ {"question": question,"answer":fulfillment_text} ] }] } } }
             )

    # use try and except for insert and upsert
    #Course.objects.raw({"course_id":"BUS200" ,"students.email_id":"jh@horizon.csueastbay.edu","students.chat_history.c_id":sid}).update(
    #    { "$push":{"students.$.chat_history.0.chats": { "$each": [{ "question":question, "answer":fulfillment_text }] }}})

    return response_text

# socket io implementation
@socketio.on('connect')
def socket_connection():
    print("connection", request.sid)
    session['websocket'] = request.sid

@socketio.on('disconnect')
def socket_disconnect():
    pass

# to get question for dialogflow
@socketio.on('question')
def handle_question(msg):
    # get a question and its answer here
    question = msg['question']
    name = msg['name']
    email_id = msg['email_id']
    course_id = msg['course_id']
    sid = request.sid
    date = datetime.datetime.now()
    answer = send_message(question,sid,name,email_id,course_id,date)
    socketio.emit('answer',answer,room = sid)

# to get answer for quiz
@socketio.on('quiz_answer')
def handle_question(msg):
    user_answer = msg['answer']
    name = msg['name']
    email_id = msg['email_id']
    course_id = msg['course_id']
    question_id = msg['question_id']
    tid = request.sid
    date = datetime.datetime.now()
    #answer = send_message(question,sid,name,email_id,course_id,date)
    answer = { "message":  user_answer, "name": name}
    socketio.emit('quiz_feedback',answer,room = tid)
