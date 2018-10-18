from flask import request, render_template,jsonify
from app import app
import dialogflow
import os
import requests
from config import Config
import json

#app = Flask(__name__)



@app.route('/')
def index():
    return render_template('test.html')


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
