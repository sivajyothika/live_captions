import tensorflow as tf
import numpy as np
from pydub import AudioSegment
from pydub.utils import mediainfo
import librosa
import os
from base64 import b64encode
from IPython.display import HTML

from model import format_timestamp


# Define the classes
classes = ["yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"]

# Load the trained model
model = tf.keras.models.load_model('SpeechRecogModel.h5')


# Set file names and formats
input_file = "input.mp4"
output_file = "output.wav"
output_dir = "./"


# Extract the audio from the MP4 video file
audio = AudioSegment.from_file(input_file, format="mp4").set_channels(1)

# Check if the audio is already in WAV format
if mediainfo(input_file).get('audio_format') == 'wav':
    # If the audio is already in WAV format, copy it to the output file
    with open(output_file, "wb") as f:
        f.write(audio.raw_data)
else:
    # If the audio is not in WAV format, export it to WAV format
    audio.export(output_file, format="wav")


# Function to predict the class label of the audio
def predict(audio):
    # Reshape the input to a 3D tensor
    audio = np.expand_dims(audio, axis=0)  # shape: (1, time_steps, input_dim)
    
    # Normalize the input
    audio = audio / np.max(np.abs(audio))

    # Make the prediction
    prob = model.predict(audio)
    index = np.argmax(prob[0])
    return classes[index]


# Load the audio file and transcribe it
audio, sr = librosa.load(output_file, sr=8000, mono=True)
duration = librosa.get_duration(audio, sr=sr)

result = {
    "segments": []
}

# Define the segment length in seconds
segment_length = 1.5

# Transcribe the audio in segments and store the predictions and timestamps
for i in range(0, int(np.ceil(duration / segment_length))):
    start = i * segment_length
    end = min(duration, start + segment_length)
    segment = audio[int(start * sr):int(end * sr)]
    text = predict(segment)
    result["segments"].append({
        "start": start,
        "end": end,
        "text": text
    })


# Write the transcribed text to a VTT file
audio_path = os.path.splitext(os.path.basename(output_file))[0]
subtitle_file = os.path.join(output_dir, audio_path + ".vtt")

with open(subtitle_file, "w") as vtt:
    print("WEBVTT\n", file=vtt)
    for segment in result["segments"]:
        print(f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
              f"{segment['text'].strip().replace('-->', '->')}\n",
              file=vtt,
              flush=True)


# Generate the subtitled video
output_video = os.path.join(output_dir, audio_path + "_subtitled.mp4")

os.system(f"ffmpeg -i {input_file} -vf subtitles={subtitle_file} {output_video}")


# Display the generated video
mp4 = open(output_video, 'rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""
# <video width=400 controls>
#       <source src="%s" type="video/mp4">
# </video>
# """ % data_url)

# import tensorflow as tf
# import numpy as np
# from pydub import AudioSegment
# from pydub.utils import mediainfo
# import librosa
# import os

# classes = ["yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"]
# model = tf.keras.models.load_model('SpeechRecogModel.h5')

# # Set file names and formats
# input_file = "input.mp4"
# output_file = "output1.wav"

# # Extract the audio from the MP4 video file
# audio = AudioSegment.from_file(input_file, format="mp4").set_channels(1)

# # Check if the audio is already in WAV format
# if mediainfo(input_file).get('audio_format') == 'wav':
#     # If the audio is already in WAV format, copy it to the output file
#     with open(output_file, "wb") as f:
#         f.write(audio.raw_data)
# else:
#     # If the audio is not in WAV format, export it to WAV format
#     audio.export(output_file, format="wav")

# # Load the audio file and resample to 8000 Hz
# audio, sr = librosa.load('output1.wav', sr=8000, mono=True)

# # Trim the audio to 8000 samples (1 second)
# audio = audio[:8000]

# # Reshape the input to a 3D tensor
# audio = np.expand_dims(audio, axis=0)  # shape: (1, time_steps, input_dim)

# # Normalize the input
# audio = audio / np.max(np.abs(audio))

# # Make the prediction
# prob = model.predict(audio)
# index = np.argmax(prob[0])
# predicted_text = classes[index]

# print(predicted_text)
# output_dir = ''

# # if not os.path.exists(output_dir):
# #     os.makedirs(output_dir)

# audio_path = audio_file.split(".")[0]


# def format_timestamp(seconds: float, always_include_hours: bool = False, decimal_marker: str = '.'):
#     assert seconds >= 0, "non-negative timestamp expected"
#     milliseconds = round(seconds * 1000.0)

#     hours = milliseconds // 3_600_000
#     milliseconds -= hours * 3_600_000

#     minutes = milliseconds // 60_000
#     milliseconds -= minutes * 60_000

#     seconds = milliseconds // 1_000
#     milliseconds -= seconds * 1_000

#     hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
#     return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"


# extension: str = "vtt"


# def write_result(result: dict, file: TextIO):
#   print("WEBVTT\n", file=file)
#   for segment in result["segments"]:
#     print(
#         f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
#         f"{segment['text'].strip().replace('-->', '->')}\n",
#         file=file,
#         flush=True,
#         )


# with open(os.path.join(output_dir, audio_path + ".vtt"), "w") as vtt:
#     write_result(result, file=vtt)

# subtitle = audio_path + ".vtt"
# output_video = audio_path + "_subtitled.mp4"

# os.system(f"ffmpeg -i {input_video} -vf subtitles={subtitle} {output_video}")


# # subprocess.call(["ffmpeg", "-i", input_video , "-vf", f"subtitles={subtitle}", f"{output_video}"], 
# #                 stdout=subprocess.DEVNULL,
# #                 stderr=subprocess.STDOUT)

# mp4 = open(output_video,'rb').read()
# data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
# HTML("""
# <video width=400 controls>
#       <source src="%s" type="video/mp4">
# </video>
# """ % data_url)

# classes = ["yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"]
# model = tf.keras.models.load_model('SpeechRecogModel.h5')


# # Set file names and formats
# input_file = "input.mp4"
# output_file = "output1.wav"

# # Extract the audio from the MP4 video file
# audio = AudioSegment.from_file(input_file, format="mp4").set_channels(1)

# # Check if the audio is already in WAV format
# if mediainfo(input_file).get('audio_format') == 'wav':
#     # If the audio is already in WAV format, copy it to the output file
#     with open(output_file, "wb") as f:
#         f.write(audio.raw_data)
# else:
#     # If the audio is not in WAV format, export it to WAV format
#     audio.export(output_file, format="wav")


# def predict(audio):
#     # Reshape the input to a 3D tensor
#     audio = np.expand_dims(audio, axis=0)  # shape: (1, time_steps, input_dim)
    
#     # Normalize the input
#     audio = audio / np.max(np.abs(audio))

#     # Make the prediction
#     prob = model.predict(audio)
#     index = np.argmax(prob[0])
#     return classes[index]



# audio, sr = librosa.load('output1.wav', sr=8000, mono=True)
# predictions = predict(audio)
# print(predictions)
