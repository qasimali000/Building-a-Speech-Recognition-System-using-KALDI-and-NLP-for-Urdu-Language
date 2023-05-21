import mutagen
from mutagen.wave import WAVE
import librosa
import os
# function to convert the information into
# some readable format
def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds

    return hours, mins, seconds  # returns the duration


# Create a WAVE object
# Specify the directory address of your wavpack file
# "alarm.wav" is the name of the audiofile
# audio = WAVE("alarm.wav")
lent = []
mint = []
secs = []
src_folder = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/audio/Audios_Folders/'

nn = os.listdir(src_folder)
audio_files = librosa.util.find_files(src_folder, ext=['wav'])
for file in audio_files:
    # contains all the metadata about the wavpack file
    audio = WAVE(file)
    audio_info = audio.info
    length = int(audio_info.length)

    hours, mins, seconds = audio_duration(length)
    lent.append(hours)
    mint.append(mins)
    secs.append(seconds)
    print(mins)
    print(seconds)
# print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))
print(sum(mint))
print(sum(secs))
