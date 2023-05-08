# Convert all audio files in a directory from wav to mp3. This was done to convert IEMOCAP data from wav to mp3 format so that its size can be reduced
# Version 1.0  October 8, 2020 


import os
import glob
import subprocess
import librosa
            
if __name__ == '__main__':
    src_folder = 'Files/wav/'
    dst_folder = 'Files/mp3/'                             #Get the list of wav files to convert to mp3
    nn = os.listdir(src_folder)
    audio_files = librosa.util.find_files(src_folder, ext=['wav'])
    for file in audio_files:  # Read every wav file in the given source directory
        print('\n processing' + file)
        name, ext = os.path.splitext(file)  # Remove Path from File Name
        nm = os.path.basename(name)  # Getting the name of file without old extension
        sc = dst_folder + "{0}.mp3".format(nm)  # Formatting each file with name and mp3 extension.
        subprocess.call(['ffmpeg', '-i', file, '-acodec', 'libmp3lame', sc])


# Added this block to get directory names and then create the same directory in mp3 folder to maintain structure.

    # for n in nn:
    #     # dst_folder = 'D:\\QasimAli-DSE\\IEMOCAP_full_release\\Session1\\sentences\\mp3\\' + n
    #     an = os.mkdir(dst_folder + n)
    #
    #     audio_files = librosa.util.find_files(src_folder, ext=['wav'])
    #     # print(audio_files)
    #
    # #below code does the same as before, it takes the files and converts them to mp3
    #     for file in audio_files:                    #Read every wav file in the given source directory
    #         print('\n processing' + file)
    #         name , ext = os.path.splitext (file)     #Remove Path from File Name
    #         nm = os.path.basename(name)             #Getting the name of file without old extension
    #         sc = dst_folder + n + "\{0}.mp3".format ( nm )    #Formatting each file with name and mp3 extension.
    #         subprocess.call(['ffmpeg', '-i', file, '-acodec', 'libmp3lame', sc])
