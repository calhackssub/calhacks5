import subprocess

def subtitleVideo(name):
	command = "ffmpeg -i " + name + ".mp4" + " -vf subtitles=" + name + ".srt " + name + "-subbed.mp4"
	subprocess.call(command, shell=True)