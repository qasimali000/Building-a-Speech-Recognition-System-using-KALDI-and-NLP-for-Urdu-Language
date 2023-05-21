
import os
import glob
import subprocess
import librosa
            
if __name__ == '__main__':
    src_folder = 'Files/wav/'
    dst_folder = 'Files/mp3/'                             #Get the list of wav files to convert to mp3.
    nn = os.listdir(src_folder)
    audio_files = librosa.util.find_files(src_folder, ext=['wav'])
    for file in audio_files:  # Read every wav file in the given source directory
        print('\n processing' + file)
        name, ext = os.path.splitext(file)  # Remove Path from File Name
        nm = os.path.basename(name)  # Getting the name of file without old extension
        sc = dst_folder + "{0}.mp3".format(nm)  # Formatting each file with name and mp3 extension.
        subprocess.call(['ffmpeg', '-i', file, '-acodec', 'libmp3lame', sc])


