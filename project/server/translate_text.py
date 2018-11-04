import os

# Imports the Google Cloud client library
from google.cloud import translate

def translateText(filename, language):
	# Instantiates a client
	translate_client = translate.Client()

	contents = [line.rstrip('\n') for line in open(filename + ".txt")]
	contents[2] = translate_client.translate(contents[2], target_language=language)['translatedText']

	i = 0
	j = 3
	for i in range(len(contents)):
		if i > 2:
			if j == 0:	
				contents[i] = translate_client.translate(contents[i], target_language=language)['translatedText']
				j = 4
			j -= 1
		i += 1	


	f = open(filename + ".srt", "a")
	for line in contents:
		f.write(str(line) + "\n")
