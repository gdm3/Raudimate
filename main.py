# put title.png and opensans in a seperate utils
import audio, video, ffmpeg, os
from faster_whisper import WhisperModel
from PIL import ImageGrab

with open('utils/config.txt', 'a+') as file: # Check if API key exists, if not create it
    file.seek(0)
    if not file.read():
        file.write(input("API Key? \n-> "))
    file.seek(0)
    api_key = file.read()    

title = input("Title? \n-> ")

print("Body? \nC-Z -> ")
lines = []
while True:
    try:
        line = input()
        lines.append(line)
    except EOFError:
        break
body = '\n'.join(lines)

if input("Create new audio? \n-> ") == "Y":
    audio.generate_audio(title, 'title.mp3', api_key)
    audio.generate_audio(body, 'body.mp3', api_key)
    
if input("Clear files? \n-> ") == "Y":
    try:
        os.remove("videos/spliced.mp4")
        os.remove("videos/imaged.mp4")
        os.remove("videos/subtitled.mp4")
        os.remove("videos/concat.mp4")
        os.remove("videos/truncate.mp4")
    except:
        print("-> Failed to remove files")
        
input("Title image? \n-> ")
try:
    im = ImageGrab.grabclipboard()
    sc = im.width / 405
    im = im.resize((405, int(im.height/sc)))
    im.save('utils/title.png','PNG')
except AttributeError as e:
    print("Clipbord does not contain an image!")
    raise(e)

video.create_spliced()

model = WhisperModel("small") # Transcrptions
segments, info = model.transcribe("audio/body.mp3")
segments = list(segments)

subtitles = []
for segment in segments:
    subtitles.append([segment.text, round(segment.start, 2), round(segment.end, 2)])
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

subtitles = audio.split_whisper(subtitles)

titleLength = round(float(ffmpeg.probe('audio/title.mp3')['format']['duration']), 2)

for i in subtitles:
    i[1] += titleLength
    i[2] += titleLength
    
video.add_image(duration=titleLength)

video.append_subtitles(subtitles)

video.concat(titleLength)

video.truncate_video(subtitles[-1][2] + 2) 