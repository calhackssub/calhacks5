import os
from flask import Flask, render_template, request
from server.text.speech_to_text import transcribeAudio

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

speechLangDict = {'1': "one", '2': "two", '3': "three"}
translateLangDict = {'4': "four", '5': "five", '6': "six"}

@app.route('/')
def index():
    return render_template("index.html", speechLangDict = speechLangDict, translateLangDict = translateLangDict)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    target = os.path.join(APP_ROOT, 'audio/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    filename = 1
    for file in request.files.getlist("file"):
        filename = file.filename
        print(filename)
        destination = "/".join([target, filename])
        file.save(destination)

    speechLangCode = speechLangDict.get(request.form.get('speechLang'))
    translateLangCode = translateLangDict.get(request.form.get('translateLang'))
    print(speechLangCode)
    print(translateLangCode)

    transcribeAudio(filename)

    return render_template("completed.html")


if __name__  == "__main__":
    app.run(debug=True)