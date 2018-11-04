import os
from flask import Flask, render_template, request
from speech_to_text import transcribeAudio
from translate_text import translateText
from encode_subtitles import subtitleVideo

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

speechLangDict = {'English': "en-US", 'Spanish': "es-ES", 'French': "fr-FR",
    'Korean': "ko-KR", 'Chinese': "cmn-Hant-TW", 'German': "de-De", 'Hindi': "hi-IN", 'Italian': "it-IT"}
translateLangDict = {'English': "en", 'Spanish': "es", 'French': "fr",
    'Korean': "ko", 'Chinese': "zh", 'German': "de", 'Hindi': "hi", 'Italian': "it"}

@app.route('/')
def index():
    return render_template("index.html", speechLangDict = speechLangDict, translateLangDict = translateLangDict)

@app.route('/upload', methods = ['GET', 'POST'])

def upload():
    for file in request.files.getlist("file"):
        filename = file.filename
        print(filename)
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        print(APP_ROOT)
        # destination = "/".join(filename)
        file.save(os.path.join(APP_ROOT, filename))

    name = filename.split(".")[0]

    speechCode = speechLangDict.get(request.form.get('speechLang'))
    translateCode = translateLangDict.get(request.form.get('translateLang'))
    # print(speechCode)
    # print(translateCode)

    transcribeAudio(name, speechCode)
    os.remove(name + ".wav")
    translateText(name, translateCode)
    os.remove(name + ".txt")
    subtitleVideo(name)
    os.remove(name + ".mp4")
    os.remove(name + ".srt")

    finalName = name + "-subbed.srt" 
    return render_template("completed.html")


if __name__  == "__main__":
    app.run(debug=True)