from flask import Flask, request, render_template

app = Flask(__name__)





@app.route('/')
def my_form():

    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    question = request.form.get("question")
    chat = request.form.get("chat")
    print(chat)
    # print(question)

    return render_template('index.html', question = question)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
