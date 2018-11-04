# Imports the Google Cloud client library
from google.cloud import translate


# Instantiates a client
translate_client = translate.Client()

target = 'es'




contents = [line.rstrip('\n') for line in open("foreign.txt")]

contents[2] = translate_client.translate(contents[2], target_language=target)['translatedText']


i = 0
j = 3
for i in range(len(contents)):
	if i > 2:
		if j == 0:	
			contents[i] = translate_client.translate(contents[i], target_language=target)['translatedText']
			j = 4
		j -= 1
	i += 1	


f = open("translation.srt", "a")
for line in contents:
	f.write(str(line) + "\n")






# # The text to translate
# text = "Hello-->bears"
# text_array = text.split('-->')

# # The target language
# target = 'es'

# # Translates some text into Russian
# translation_a = translate_client.translate(
#     text_array[0],
#     target_language=target)

# translation_b = translate_client.translate(
#     text_array[1],
#     target_language=target)

# subtitles_a = translation_a['translatedText']
# subtitles_b = translation_b['translatedText']

# subtitles = subtitles_a + "-->" + subtitles_b

# f = open("translation.srt", "a")
# f.write(subtitles)

# # print(u'Text: {}'.format(text))
# # print(u'Translation: {}'.format(translation['translatedText']))