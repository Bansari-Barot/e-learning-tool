from flask import request, render_template,jsonify
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
#app = Flask(__name__)



@app.route('/')
def index():
    # connect(app.config['MONGO_URI'])
    # chat1=Chat(question="hi", answer="hello")
    # chat_history1=Chat_History(datetimestamp=datetime.datetime(2006, 7, 2, 1, 3, 4),c_id="12345", chats=[chat1])
    # student1 = Student(name="Oscar", netid="yr5667", chat_history=[chat_history1])
    # course = Course(course_id="BUS110",course_name="Information Systems and Application",
    #     textbook="https://drive.google.com/file/d/14pTf5ZZ79HMSQVt4wfKtdLYVFowDlSvt/view?usp=sharing",
    #     topics=["MS Office","LinkedIn learning"], students=[student1]).save()
    # print(course)
    return render_template('test.html')

@app.route('/<string:course_id>/<string:course_name>/<string:netid>/<string:name>/<string:session_id>', methods=['GET','POST'])
def course_home(course_id,course_name,netid,name,session_id):
    connect(app.config['MONGO_URI'])
    chat1=Chat(question="hi", answer="hello")
    chat_history1=Chat_History(datetimestamp=datetime.datetime(2006, 5, 2, 1, 3, 4),c_id=session_id, chats=[chat1])
    student1 = Student(name=name, netid="yr5667", chat_history=[chat_history1])
    course = Course(course_id=course_id,course_name=course_name,
        textbook="https://drive.google.com/file/d/14pTf5ZZ79HMSQVt4wfKtdLYVFowDlSvt/view?usp=sharing",
        topics=["MS Office","LinkedIn learning"], students=[student1]).save()
    print(course)
    return '{} {} {} {} {}'.format(course_id,course_name,netid,name,session_id)


# @app.route('/')
# def my_form():
#     return render_template('index.html')
#
# @app.route('/')
# def my_form_post():
#     # question = request.form.get("question")
#     # chat = request.form.get("chat")
#     # print(chat)
#     # print(question)
#
#     return render_template('index.html', question = question)

# def test():
#     client = dialogflow_v2beta1.AgentsClient()
#     parent = client.project_path(Config.DIALOGFLOW_PROJECT_ID)
#     response = client.export_agent(parent)
#     # print("response", response)
#     def callback(operation_future):
#         result = operation_future.result()
#         #print("result",result)
#
#
#     response.add_done_callback(callback)
#     print("response", response)
#     metadata = response.metadata()
#     print("metadata",metadata)

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

@app.route('/send_message', methods=['POST'])
def send_message():

    message = request.form['message']
    project_id = Config.DIALOGFLOW_PROJECT_ID
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    return jsonify(response_text)

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
