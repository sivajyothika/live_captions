from pydub import AudioSegment
from pydub.utils import mediainfo

# Set file names and formats
input_file = "input.mp4"
output_file = "output1.wav"

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

# from pydub import AudioSegment


# # Set file names and formats
# input_file = "input.aac"
# output_file = "output.wav"

# # Read in the AAC audio file
# aac_audio = AudioSegment.from_file(input_file, format="aac")

# # Export the AAC audio file to WAV format
# aac_audio.export(output_file, format="wav")
