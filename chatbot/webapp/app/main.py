from flask import session,request, render_template,jsonify
from app import app
import dialogflow
import os
import requests
from config import Config
import json
import dialogflow_v2beta1
from app.models import Chat, Chat_History, Student, Course
from pymodm import connect
from flask_pymongo import PyMongo
import datetime
from bson.tz_util import utc, FixedOffset
import time

from app import socketio
from flask_socketio import send, emit

@app.route('/', methods=['GET','POST'])
def login():
    return render_template('login.html')

#if the student enters parameters as form elements / not by BB
@app.route('/home', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email_id = request.form['netid']
        name = request.form['name']
        course_id="BUS110"

    if request.method == 'GET':
        email_id = request.args.get('netid','')
        name = request.args.get('name','')
        course_id="BUS110"

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
            return render_template('index.html',name= name, email_id= email_id, course_id= course_id)
        except Course.DoesNotExist:
            course_info = {"name": name, "email_id": email_id, "course_id": course_id}
            Course.objects.raw({"course_id":course_id}).update(
                { "$push":{"students": { "$each": [{'name':name,'email_id':email_id}] } } } )
            user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
            st = str(user.students)
            return render_template('index.html',name= name, email_id= email_id, course_id= course_id)

    except Course.DoesNotExist:
        student = Student(name=name, email_id=email_id)
        course = Course(course_id=course_id,course_name="Information Systems & Applications",
                        textbook="https://drive.google.com/file/d/14pTf5ZZ79HMSQVt4wfKtdLYVFowDlSvt/view?usp=sharing",
                        topics=["MS Office","LinkedIn learning"], students=[student]).save()
        course = Course.objects.get({'course_id':course_id})
        print(course)
        course_info = {"name": name, "email_id": email_id, "course_id": course_id}
        return render_template('index.html',name= name, email_id= email_id, course_id= course_id)

#if the BB passes parameters with the link
# @app.route('/<string:course_id>/<string:name>/<string:email_id>', methods=['GET','POST'])
# def index(course_id, name, email_id):
#     connect(app.config['MONGO_URI'])
#
#
#     # Here first check whether course is there in db or not and if not then in except add that course,student into db
#     try:
#         course = Course.objects.get({'course_id':course_id})
#         print(course)
#         # Second check whether the students is exist inside the course or not if not then in except add students into that
#         # course
#         try:
#             user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
#             course_info = {"name": name, "email_id": email_id, "course_id": course_id}
#             return render_template('index.html',name= name, email_id= email_id, course_id= course_id)
#         except Course.DoesNotExist:
#             course_info = {"name": name, "email_id": email_id, "course_id": course_id}
#             Course.objects.raw({"course_id":course_id}).update(
#                 { "$push":{"students": { "$each": [{'name':name,'email_id':email_id}] } } } )
#             user = Course.objects.get({'course_id':course_id,'students.email_id':email_id})
#             st = str(user.students)
#             return render_template('index.html',name= name, email_id= email_id, course_id= course_id)
#
#     except Course.DoesNotExist:
#         student = Student(name=name, email_id=email_id)
#         course = Course(course_id=course_id,course_name="Information Systems & Applications",
#                         textbook="https://drive.google.com/file/d/14pTf5ZZ79HMSQVt4wfKtdLYVFowDlSvt/view?usp=sharing",
#                         topics=["MS Office","LinkedIn learning"], students=[student]).save()
#         course = Course.objects.get({'course_id':course_id})
#         print(course)
#         course_info = {"name": name, "email_id": email_id, "course_id": course_id}
#         return render_template('index.html',name= name, email_id= email_id, course_id= course_id)



def detect_intent_texts(project_id, session_id, text, language_code):
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

    project_id = Config.DIALOGFLOW_PROJECT_ID
    fulfillment_text = detect_intent_texts(project_id, "unique", question, 'en')
    response_text = { "message":  fulfillment_text }
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

def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    import dialogflow_v2 as dialogflow
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)
    print('Intent created: {}'.format(response))

# socket io implementation
@socketio.on('connect')
def socket_connection():
    print("connection", request.sid)
    session['websocket'] = request.sid

@socketio.on('disconnect')
def socket_disconnect():
    pass

@socketio.on('question')
def handle_question(msg):
    # get a question and its answer here
    question = msg['question']
    name = msg['name']
    email_id = msg['email_id']
    course_id = msg['course_id']
    sid = request.sid
    date = datetime.datetime.now()
    # check whether the the sid is already in chat history if not then insert else update query
    answer = send_message(question,sid,name,email_id,course_id,date)
    socketio.emit('answer',answer,room = sid)
