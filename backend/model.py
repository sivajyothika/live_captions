import os
import subprocess
import whisper
from IPython.display import Audio
from IPython.display import HTML
from base64 import b64encode
from typing import TextIO

# import downloadvid

# downloadvid.download_video()

model = whisper.load_model("base")


def video2mp3(video_file, output_ext="mp3"):
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"

#input_video = 'this+invention+makes+getting+out+of+bed+so+much+easier..mp4'


input_video = 'video.mp4'

audio_file = video2mp3(input_video)

# Audio(audio_file)


def translate(audio):
    
    options = dict(beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)
    result = model.transcribe(audio_file,**translate_options)
    return result


result = translate(audio_file)

# print(result["language"])

# print(result["text"])

# print(result["segments"])

mp4 = open(input_video,'rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""
<video width=400 controls>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)


output_dir = ''

# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

audio_path = audio_file.split(".")[0]


def format_timestamp(seconds: float, always_include_hours: bool = False, decimal_marker: str = '.'):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"


extension: str = "vtt"


def write_result(result: dict, file: TextIO):
  print("WEBVTT\n", file=file)
  for segment in result["segments"]:
    print(
        f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
        f"{segment['text'].strip().replace('-->', '->')}\n",
        file=file,
        flush=True,
        )


with open(os.path.join(output_dir, audio_path + ".vtt"), "w") as vtt:
    write_result(result, file=vtt)

subtitle = audio_path + ".vtt"
output_video = audio_path + "_subtitled.mp4"

os.system(f"ffmpeg -i {input_video} -vf subtitles={subtitle} {output_video}")


# subprocess.call(["ffmpeg", "-i", input_video , "-vf", f"subtitles={subtitle}", f"{output_video}"], 
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.STDOUT)

mp4 = open(output_video,'rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""
<video width=400 controls>
      <source src="%s" type="video/mp4">
</video>
""" % data_url)