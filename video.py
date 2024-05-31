import ffmpeg, random
from PIL import ImageFont


def generate_time():
    _time = random.randint(0, 8)
    return ['00:0' + str(_time) + ':00', '00:0' + str(_time + 1) + ':00']

def whisper_ffmpeg(time: int) -> str: # Returns ffmpeg timestamp from whisper
    if len(str(time)) == 1:
    
        return '00:00:0' + str(time) + ':00'
    else:
        return '00:00:' + str(time) + ':00'

def create_unspliced(filename="videos/parkour.mp4") -> str: # Create unspliced short format
    width = int(720 * (9/16))
    x = (1280 - width) / 2
    
    (
        ffmpeg.input(filename)
        .crop(x, 0, width, 720) # 720p
        .output('videos/unspliced.mp4')
        .run()
    )
    return 'videos/unspliced.mp4'

def create_spliced(filename="videos/unspliced.mp4") -> str: # todo - make into spliced.mp4
    video_split = generate_time()
    (
        ffmpeg.input(filename, ss=video_split[0], to=video_split[1])
        .output('videos/spliced.mp4')
        .run()
    )
    return 'videos/spliced.mp4'

def concat(offset, videoname="videos/subtitled.mp4"): 
    video_stream = ffmpeg.input(videoname)
    title = ffmpeg.input('audio/title.mp3')
    body = ffmpeg.input('audio/body.mp3')
    body = ffmpeg.filter(body, 'adelay', f"{offset * 1010}|{offset * 1010}")
    
    merged_audio = ffmpeg.filter([title, body], 'amix')
    
    video_stream = ffmpeg.concat(video_stream, merged_audio, v=1, a=1)
    video_stream = ffmpeg.output(video_stream, 'videos/concat.mp4')
    
    ffmpeg.run(video_stream)

def append_subtitles(subtitles, filename="videos/imaged.mp4"):
    stream = ffmpeg.input(filename)

    _width = int(720 * (9/16)) # Width of video
    fontsize = 35
    font = ImageFont.truetype('utils/opensans.ttf', fontsize)
    
    for subtitle in subtitles:
        _text = ""
        fulltext = ""
        subtitle[0] = subtitle[0].split()
        for i in subtitle[0]:
            _text += i
            length = font.getlength(_text)
            if length > (_width - 100):
                fulltext += "\n"
                fulltext += ' ' + i 
                _text = i
            else:
                fulltext += ' ' + i 
        y = int(720/2)
        fulltext = fulltext.split('\n')
        for i in fulltext:
            offset = font.getlength(i) // 2
            _x = _width / 2 - offset
            stream = ffmpeg.drawtext(stream, text=i, x=int(_x), y=y, fontcolor="White", fontfile="utils/opensans.ttf", fontsize=fontsize, shadowcolor="Black", shadowx=2, shadowy=2, enable=f'between(t,{subtitle[1]},{subtitle[2]})')
            y += 40

    stream = ffmpeg.output(stream, 'videos/subtitled.mp4')
    ffmpeg.run(stream)

def truncate_video(timestamp, filename="videos/concat.mp4"):
    (
        ffmpeg.input(filename, ss='00:00:00', to='00:00:' + str(int(timestamp)))
        .output("videos/truncate.mp4")
        .run()
    )
    
def add_image(duration, filename="videos/spliced.mp4"):
   stream = ffmpeg.input(filename)
   image = ffmpeg.input('utils/title.png')
   stream = ffmpeg.filter([stream, image], 'overlay', 0, 300, enable=f'between(t,0,{str(duration)})')
   stream = ffmpeg.output(stream, 'videos/imaged.mp4')
   ffmpeg.run(stream)