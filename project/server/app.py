import os
from flask import Flask, render_template, request, send_file
from speech_to_text import transcribeAudio
from translate_text import translateText
from encode_subtitles import subtitleVideo

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

speechLangDict = {'Italian': "it-IT", 'Spanish': "es-ES", 'French': "fr-FR",
    'Korean': "ko-KR", 'Chinese': "cmn-Hant-TW", 'German': "de-De", 'Hindi': "hi-IN", 'English': "en-US"}
translateLangDict = {'Italian': "it", 'Spanish': "es", 'French': "fr",
    'Korean': "ko", 'Chinese': "zh", 'German': "de", 'Hindi': "hi", 'English': "en"}

@app.route('/')
def index():
    return render_template("index.html", speechLangDict = speechLangDict, translateLangDict = translateLangDict)


@app.route('/download', methods = ['GET', 'POST'])
def upload():
    for file in request.files.getlist("file"):
        filename = file.filename
        print(filename)
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        print(APP_ROOT)
        file.save(os.path.join(APP_ROOT, filename))

    name = filename.split(".")[0]

    speechCode = speechLangDict.get(request.form.get('speechLang'))
    translateCode = translateLangDict.get(request.form.get('translateLang'))

    transcribeAudio(name, speechCode)
    os.remove(name + ".wav")
    translateText(name, translateCode)
    os.remove(name + ".txt")
    subtitleVideo(name)
    os.remove(name + ".mp4")
    os.remove(name + ".srt")

    finalPath = "download/" + name + "-subbed.mp4"
    finalName = name + "-subbed.mp4"
    return render_template("completed.html", finalName = finalName, finalPath = finalPath)


@app.route('/download/<name>')
def download(name = None):
    print(name)
    if name is None:
        return
    return send_file(name, as_attachment=True)


if __name__  == "__main__":
    app.run(debug=True)