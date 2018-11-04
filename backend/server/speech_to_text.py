import io, os
import subprocess

#set to your path to the key
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/blues/repo2/backend/key.JSON"

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


#takes in an audio file from /audio and prints text to  /text/transcribed_audio.txt
def transcribeAudio(name, language):
    
    #Convert video file to .wav 
    command = "ffmpeg -i " + name + ".mp4" + " -ab 160k -ac 1 -ar 44100 -vn " + name + ".wav"
    print(command)

    subprocess.call(command, shell=True)

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        name + ".wav")

    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code=language,
        enable_word_time_offsets=True)

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        alternative = result.alternatives[0]
  
    tF = open(os.path.join(
        os.path.dirname(__file__),
        name + '.txt'), 'a')

    i = 1
    words = []
    bookend = {
        "start": None,
        "end": None
    }

    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time
        words.append(word)

        if ((len(words) - 1) % 8) == 0:
            bookend["start"] = "00:" + "00:" + str(start_time.seconds) + "," + str(int(start_time.nanos * 1e-8)) + "00"
        elif (len(words) % 8) == 0:
            bookend["end"] = "00:" + "00:" + str(end_time.seconds) + "," + str(int(end_time.nanos * 1e-8)) + "00"
            if i > 1:
                tF.write("\n")
            tF.write(str(i) + "\n")
            tF.write(bookend["start"] + " --> " + bookend["end"] + "\n")
            for item in words:
                tF.write(item + " ")
            tF.write("\n")
            words = []
            i += 1