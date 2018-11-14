from flask import request, render_template,jsonify
from app import app
import dialogflow
import os
import requests
from config import Config
import json
import dialogflow_v2beta1





#app = Flask(__name__)



@app.route('/')
def index():

    return render_template('test.html')

@app.route('/positive_feedback' ,methods=['POST'])
def pos_feedback():
    print("user is satisfied")

#
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
