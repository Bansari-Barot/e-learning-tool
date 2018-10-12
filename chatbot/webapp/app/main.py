from flask import request, render_template
from app import app
import dialogflow_v2beta1

#app = Flask(__name__)





@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/')
def my_form_post():
    # question = request.form.get("question")
    # chat = request.form.get("chat")
    # print(chat)
    # print(question)

    return render_template('index.html', question = question)
