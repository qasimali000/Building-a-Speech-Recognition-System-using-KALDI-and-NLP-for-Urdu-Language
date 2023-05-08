
"""
Version: 0.0.1
Author: Qasim Ali
Pipeline which connects Speaker Dirarization, Speaker Overlap and the Flag for Good/Unusual Calls.

This file contains the code which returns the output for Speaker Diarization, Overlap Detection, Emotion Detection and Flag.
The code also performs basic data preparations for Audio files such as MP3 to WAV Conversion, Appending WAV File and creating
Spectrograms.
"""


from pydub import AudioSegment
import librosa
import os, shutil
import numpy as np
import librosa.display
from matplotlib.pyplot import xlim, ylabel, figure, legend, xticks, show, subplot, title, tight_layout, colorbar, \
    semilogy, plot, xlabel, savefig, clim, close, set_cmap
import subprocess
import pyannote_test

import time
import matplotlib.style as ms
ms.use('seaborn-muted')
import math
import pandas as pd
import random
import glob


from matplotlib.pyplot import xlim, ylabel, figure, legend, xticks, show, subplot, title, tight_layout, colorbar, \
    semilogy, plot, xlabel, savefig, clim, close, set_cmap

# Path to store Appended file which will be used in Speaker Diarization and all other operation except Emotion Detection.
appended_files = "Files/appended/"
appended_8k = "Files/appended_8k/"
sentences_path = "Files/diarized_sentences/"
path_wav_split = "Files/wav/"
appended_files_nns ="Files/appended_nns/" # path to store non noise supressed wav file
normalized_wav = "Files/normalized_wav/" # path for normalized wav audio
appended_normalized = "Files/appended_normalized/"
"""  The Following path will be used to store the appended file in the different directory which will be used 
for Emotion Detection API's Sepctrogram Generation
"""
appended_files1 = "Files/appended1/"

diaar = []
diasl = []
diamxsl = []
sodar = []
maxovl = []
# ovldur = []
# ovldur1 = []

rttm_path = 'Files/rttm'
for filename in os.listdir(rttm_path):
    file_path = os.path.join(rttm_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder_appended_normalized = 'Files/appended_normalized/'
for filename in os.listdir(folder_appended_normalized):
    file_path = os.path.join(folder_appended_normalized, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder_normalized = 'Files/normalized_wav/'
for filename in os.listdir(folder_normalized):
    file_path = os.path.join(folder_normalized, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder_nns = 'Files/appended_nns/'
for filename in os.listdir(folder_nns):
    file_path = os.path.join(folder_nns, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



folder = 'Files/wav/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder_nm = 'Files/noise_supressed_wav/'
for filename in os.listdir(folder_nm):
    file_path = os.path.join(folder_nm, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder1 = 'Files/appended/'
for filename in os.listdir(folder1):
    file_path = os.path.join(folder1, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder2 = 'Files/appended1/'
for filename in os.listdir(folder2):
    file_path = os.path.join(folder2, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))




folder3 = 'Files/Extracted_spectrograms/'
for filename in os.listdir(folder3):
    file_path = os.path.join(folder3, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



folder4 = 'Files/diarized_sentences/'
for filename in os.listdir(folder4):
    file_path = os.path.join(folder4, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



folder5 = 'Files/appended_8k/'
for filename in os.listdir(folder5):
    file_path = os.path.join(folder5, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



folder6 = 'Files/Reports/'
for filename in os.listdir(folder6):
    file_path = os.path.join(folder6, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder7 = 'Files/temp_excel/'
for filename in os.listdir(folder7):
    file_path = os.path.join(folder7, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



ls_ns_tm_calc = []

"""
The following main function declares the paths and call different functions which in turn gives a collective output at the end.
"""
def main():
    # The following path is to get MP3 file
    #mp3_path_audio = "Files/SQA_testing_mp3/test_split"
    mp3_path_audio = 'Files/mp3'

    # This path is for WAV File after conversion it is stored there.
    wav_path_audio = 'Files/wav/'
    wav_path_ns = 'Files/noise_supressed_wav/'

    mp3_2_wav(mp3_path_audio, wav_path_audio) # Function call to convert the mp3 files to Wav
    
    #audio normalization function call
    main_normalization(wav_path_audio)

    wav_audio_files = librosa.util.find_files(wav_path_audio)   # Getting the wav files from path

    # Spectrogram Path where the spectrograms for Flag prediction will be stored
    spectrogram_path = 'Files/Extracted_spectrograms/'

    #code for DTLN Noise Supression Script Call
    start_time_noise_supression = time.time()
    from DTLN.DTLN import custom_script
    noise_supression_calc = time.time() - start_time_noise_supression
    ls_ns_tm_calc.append(noise_supression_calc)
    print(" ----%s Noise Supression Time in seconds ------" % (time.time() - start_time_noise_supression))

    # Function call for Appending files for Diarization
    files_append(wav_path_ns)
    # files_append_nns(normalized_wav) #uncomment this and comment below to start normalization
    files_append_nns(wav_path_audio)

    sample_converter(wav_path_audio,appended_8k)
    # sample_converter(appended_normalized,appended_8k)
    # Spectrogram Extraction
    start_time = time.time()
    for file in wav_audio_files:
        signal, sr = load_audio_recording(file)
        short_time_fourier_transform_and_plot(signal, sr, os.path.basename(os.path.splitext(file)[0]), spectrogram_path)

    print(" ----%s seconds ------" % (time.time() - start_time))

    #  This function returns this function will returns different variables and list which are being used in USER INTERFACE
    return save_as_xlsx()
 
    #import transcription_kaldi_log as tr
    #transcription = tr.Transcriptions()
    #print(transcription)

"""
The following function performs the operations in the Pyannote Main File. In the function we are calling DIA() and SOD() functions
which returns different variables which are being returned from those functions.
"""
def Speaker_DIA(files):

    ovr = []
    ovr1 = []
    l1 = []
    l11 = []
    silperc = 0
    specperc = 0
    ovlperc = 0

    appended_files = librosa.util.find_files ( files )
    for file in appended_files:
        print("Speaker Diarization Section:")
        a = os.path.basename(file)
        name , ext = os.path.splitext(a)
        start_time = time.time()
        #tst, sil, maxsil,silperc, specperc,speaker_cn, dur,l1,l11,l2,l22, l3, l33, speak_A, speak_B, speaker_1,speaker_2 = pyannote_test.dia(file)
        tst, sil, maxsil, silperc, specperc,l1,l11 = pyannote_test.sad(file)
        #pyannote_test.dia(file)
        diaar.append(tst)
        diasl.append(sil)
        diamxsl.append(maxsil)
        print(" ----%s seconds ------" % (time.time() - start_time))


        print("Overlap Detection Section:")
        start_time1 = time.time()
        ovlp, mxovl, ovr, ovr1, ovlperc, diff = pyannote_test.sod(file)
        sodar.append(ovlp)
        maxovl.append(mxovl)
        # ovldur.append(ovr)
        print(" ----%s seconds ------" % (time.time() - start_time1))



        file_list = os.listdir(appended_8k)
        stat = []
        n1 = 1
        for file in file_list:
            aa = os.path.basename(file)
            a_name, a_ext = os.path.splitext(aa)
            if a_name == name:
                import soundfile as sf
                start_times_A = l1
                end_times_A = l11
                f= sf.SoundFile(appended_8k + file)
                duration = len(f) / f.samplerate
                speakers = 3
                print("Printing in File split function!",len(start_times_A))
                split_audio_file(sentences_path, appended_8k + file, start_times_A, end_times_A)




    #return diaar,diasl,diamxsl,sodar,maxovl, ovr, ovr1, silperc, specperc, ovlperc, speaker_cn, dur, diff, l1,l11,l2,l22, l3, l33, speak_A,speak_B,speaker_1,speaker_2
    return diaar,diasl,diamxsl,sodar,maxovl, ovr, ovr1, silperc, specperc, ovlperc,l1,l11
"""
Code for Audio Normalization
"""

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)
#path_to_normalized_files = "D:/Normalized_Audio/Audio/normalized/"
def main_normalization(wav_path):
    files = os.listdir(wav_path)
    for i in files:
        sound = AudioSegment.from_file(wav_path + i, "wav")
        print("Orignal: "+str(sound.dBFS))
        normalized_sound = match_target_amplitude(sound, -10.0)
        print("Result: "+str(normalized_sound.dBFS))
        normalized_sound.export(normalized_wav + i[:-4] + ".wav", "wav")


"""
Code for Audio Normalization
"""

"""
Files Splitting Code
"""



def split_audio_file(sentences_path , file, start_time, end_time):
    x = len(start_time)
    x_len = x/2.7
    file_path = sentences_path + "/" + os.path.splitext(os.path.basename(file))[0] + "/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for i in range(0,int(x/2.8)):
        split_audio = AudioSegment.from_wav(file)
        split_audio = split_audio[start_time[i]*1000:end_time[i]*1000]
        split_audio.export(file_path + os.path.splitext(os.path.basename(file))[0] + "_" + str(i) + "_" + ".wav", format("wav"))
        #else:
        #    print("Less than 1 second file")
        #    continue



"""
Files Splitting Code
"""




"""
The following function takes the wav files as parameter input and then appends the file and stores it into the directories
declared above. These appended files are being used in Speaker Diarization and every other essential operation.
"""
def files_append(wav_audio):
    # wav_audio1 = "E:\\Audio Analytics\\Audio-Analytics-20200819T083957Z-001\\Audio-Analytics\\Data\\conv\\MM_NEW\\"
    audio_files = librosa.util.find_files ( wav_audio , ext = ['wav'] )
    for file in audio_files:
        dur = librosa.get_duration(filename=file)
        print(dur)
        """
        if dur < 300:
            f = AudioSegment.from_wav ( file )
            name , ext = os.path.splitext ( file )
            nm = os.path.basename ( name )

            f1 = f.append ( f )
            f2 = f1.append ( f )
            #f3 = f2.append ( f )

            f2.export ( appended_files + "{0}.wav".format ( nm ) , format = "wav" )     # Storing the appended file with original name to path for all.
            f2.export(appended_files1 + "{0}.wav".format(nm), format="wav")
        else:
            f = AudioSegment.from_wav(file)
            name, ext = os.path.splitext(file)
            nm = os.path.basename(name)
            f.export(appended_files + "{0}.wav".format(nm),format="wav")  # Storing the appended file with original name to path for all.
            f.export(appended_files1 + "{0}.wav".format(nm),format="wav")  # Storing the appended file with original name to path for all.
        """
        f = AudioSegment.from_wav ( file )
        name , ext = os.path.splitext ( file )
        nm = os.path.basename ( name )
        #
        f1 = f.append ( f )
        f2 = f1.append ( f )
        # #f3 = f2.append ( f )
        #
        f2.export ( appended_files + "{0}.wav".format ( nm ) , format = "wav" )     # Storing the appended file with original name to path for all.
        f2.export ( appended_files1 + "{0}.wav".format ( nm ) , format = "wav" )    # Storing the appended file with original name to path for Emotion

##############File Append for Non Noise Supression
def files_append_nns(wav_audio):
    # wav_audio1 = "E:\\Audio Analytics\\Audio-Analytics-20200819T083957Z-001\\Audio-Analytics\\Data\\conv\\MM_NEW\\"
    audio_files = librosa.util.find_files ( wav_audio , ext = ['wav'] )
    print ( audio_files )
    for file in audio_files:
        dur = librosa.get_duration(filename=file)
        """
        print(dur)
        if dur < 300:
            f = AudioSegment.from_wav ( file )
            name , ext = os.path.splitext ( file )
            nm = os.path.basename ( name )

            f1 = f.append ( f )
            f2 = f1.append ( f )
            #f3 = f2.append ( f )

            f2.export ( appended_normalized + "{0}.wav".format ( nm ) , format = "wav" )     # Storing the appended file with original name to path for all.
            f2.export ( appended_files1 + "{0}.wav".format ( nm ) , format = "wav" )     # Storing the appended file with original name to path for all.
        else:
            f = AudioSegment.from_wav(file)
            name, ext = os.path.splitext(file)
            nm = os.path.basename(name)
            f.export(appended_normalized + "{0}.wav".format(nm),format="wav")  # Storing the appended file with original name to path for all.
            f.export(appended_files1 + "{0}.wav".format(nm), format="wav")
        """
        #dur = librosa.get_duration(filename=file)
        # print(dur)
        f = AudioSegment.from_wav ( file )
        name , ext = os.path.splitext ( file )
        nm = os.path.basename ( name )
        #
        f1 = f.append ( f )
        f2 = f1.append ( f )
        # #f3 = f2.append ( f )
        #
        f2.export ( appended_normalized + "{0}.wav".format ( nm ) , format = "wav" )     # Storing the appended file with original name to path for all.
        #f2.export ( appended_files1 + "{0}.wav".format ( nm ) , format = "wav" )    # Storing the appended file with original name to path for Emotion


"""
The following function performs MP3 to WAV format conversion. The function get the mp3 file from FLASK UPLOADS folder and
converts it to wav and stores it to the given directory for wav file above.
"""
def mp3_2_wav(mp3_path_audio, wav_audio):

    audio_files = librosa.util.find_files(mp3_path_audio, ext=['mp3'])  # Finding files with mp3 extension.
    ls_total_time = []
    for file in audio_files:    # Iterate over the audio files.
        dur = librosa.get_duration(filename=file)
        print(dur)
        ls_total_time.append(dur)
        name , ext = os.path.splitext (file)    # Splitting the name and extention
        nm = os.path.basename(name)     # Getting file's base name
        sc = wav_audio + "/{0}.wav".format ( nm )
        subprocess.call(['ffmpeg', '-i', file,'-ar', '16k', sc])    # Subprocess Call to convert mp3 to wav at 16khz Sampling rate

    print("Done Converting!!!")
    print("Total length of Audio Files:")
    print(sum(ls_total_time))



def sample_converter(src_path,dst_path):
    audio_files = librosa.util.find_files(src_path, ext=['wav'])  # Finding files with mp3 extension.
    sc = None
    fl = None

    for file in audio_files:    # Iterate over the audio files.
        name , ext = os.path.splitext (file)    # Splitting the name and extention
        nm = os.path.basename(name)     # Getting file's base name

        sc = dst_path + "/{0}.wav".format ( nm )
        subprocess.call(['ffmpeg', '-i', file, '-ar', '8k', sc])






"""
The following function loads audio recording and returns signal and sampling rate which will be used in STFT for Spectrograms
"""
def load_audio_recording(file):  # loading the waveform

    signal, sr = librosa.load(file, sr=16000)  # default sr = 22050
    return signal, sr

"""
This function performs STFT on the Signal, SR, Audio FIle and the path where the spectrogram will be stored after being
generated
"""
def short_time_fourier_transform_and_plot(signal, sr,  file, path):  # stft Spectrogram (Short time fourier transform)

    n_fft = 256  # no of samples per fft, approx 30ms for 8000 sampling rate, Vary for different campaigns
    hop_length = 128  # how much we shift during fft, 16ms for 8000Hz sampling rate
    stft_spectrogram = np.abs(librosa.stft(signal, hop_length=hop_length, n_fft=n_fft))
    log_spectrogram = librosa.amplitude_to_db(stft_spectrogram)
    # plot()
    librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length)
    set_cmap ( 'inferno' )
    clim ( -50 , +40 )
    # show()
    savefig ( path + file + '.png' )
    # savefig(path + file + '.png')
    close()
    # Qasim did work to store spectrogram in same name

            #########################################   EMOTION DETECTION INTEGRATION ########################################

sr = 16000

# function for STFT
def short_time_fourier_transform_and_plot_em(signal, file, path):  # stft Spectrogram (Short time fourier transform)

    n_fft = 512  # no of samples per fft, approx 30ms for 8000 sampling rate, Vary for different campaigns
    hop_length = 128  # how much we shift during fft, 16ms for 8000Hz sampling rate
    plot()
    stft_spectrogram = np.abs(librosa.stft(signal, hop_length=hop_length, n_fft=n_fft))

    log_spectrogram = librosa.amplitude_to_db(stft_spectrogram)
    librosa.display.specshow(log_spectrogram, sr=16000, hop_length=hop_length)

    set_cmap('plasma')
    clim(-50, +40)
    # show()
    savefig(path + '\\' + file + '.png')
    close()

########################## Function to Create Spectrograms for 2 Seconds ##############################

def create_spectogram(path,df_speaker_1,df_speaker_2):

    appended_files_path = path  # link to appended file

    orig_wave_files = os.listdir(appended_files_path)

    fl = len(orig_wave_files)/1000
    az = df_speaker_1['end_time'] <= fl/3
    print(az)
    # if orig_wave_files:
    spectrogram_path = 'Files/emotion_spectrogram' # Path to store Spectrograms for Speaker A
    spectrogram_path1 = 'Files/emotion_spectrogram1' # Path to store Spectrograms for Speaker B
    i = 0

    for file in orig_wave_files:
        # these will be loaded from pyannote_diarization
        # df_speaker_1, df_speaker_2 = pyannote_diarization.dia(file)
        # os.remove(path + "MCDONALD_20200607-014215_cmt35271_03016067777-CC.wav_audio.rttm")
        orig_wav_vector, _sr = librosa.load(appended_files_path + file , sr=sr)
        for index, row in df_speaker_1.iterrows():
            # print (row['start_time'])
            start_frame = math.floor(row['start_time'] * sr)
            end_frame = math.floor(row['end_time'] * sr)
            truncated_wav_vector = orig_wav_vector[start_frame:end_frame + 1]

            short_time_fourier_transform_and_plot_em(truncated_wav_vector, file + "_" + str(i), spectrogram_path)

            i = i + 1

        for index, row in df_speaker_2.iterrows():
            # print (row['start_time'])
            start_frame = math.floor(row['start_time'] * sr)
            end_frame = math.floor(row['end_time'] * sr)
            truncated_wav_vector = orig_wav_vector[start_frame:end_frame + 1]

            short_time_fourier_transform_and_plot_em(truncated_wav_vector, file + "_" + str(i), spectrogram_path1)

            i = i + 1

# create_spectogram()



            #########################################   EMOTION DETECTION INTEGRATION ########################################


############################## STORING TRANSCRIPTION FILES as ASR REPORTS WITH AUDIO FILE NAMES ########################
def temp_to_asr_rep():
    # path1 = '/srv/echo_pipeline_excel/Files/Reports/'
    path2 ='/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/temp_excel/'
    path3 = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/Asr_Reports/'
    # csv_files = glob.glob(os.path.join(path1, "*.xlsx"))
    csv_files1 = glob.glob(os.path.join(path2, "*.xlsx"))

    # for file in csv_files:
    #     file1 = pd.read_excel(file)
    #     df1 = pd.DataFrame(file1)
    for files in csv_files1:
        file2 = pd.read_excel(files)
        print(files)
        df2 = pd.DataFrame(file2)
        a = os.path.basename(files)
        name, ext = os.path.splitext(a)
        indexNames = df2["File_Name"].values

        nm = []
        df3 = pd.DataFrame()
        for i in indexNames:

            if name in i:
                nm.append(i)
            #else:
                #print("Not found!")


        df3["File_Name"] = nm

        df_loc = df2.loc[df2['File_Name'].isin(df3['File_Name'].values)]
        name = os.path.basename(files)

        df_loc.to_excel(path3 + name)
    ############################## STORING TRANSCRIPTION FILES as ASR REPORTS WITH AUDIO FILE NAMES ########################






def intent_write():
    intent_ls = ["Opening","Suggestive_Selling","Other","Address_confirmation","Closing","Payment_mode_verification","order confirmation","personalization name","Abuse","Assurance","Call_drop","correct_hold","magic_words","empathy","other"]
    final_report = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Final_Report.xlsx'
    intent_file = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/Asr_Reports/'
    intent_file2 = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/Asr_Reports/'
    intent_files1 = glob.glob(os.path.join(intent_file, "*.xlsx"))

    df_rep = pd.read_excel(final_report)



    df_rep["Opening"] = 1
    df_rep["Suggestive_Selling"] = 1
    df_rep["Other"] = 1
    df_rep["Address_confirmation"] = 1
    df_rep["Closing"] = 1
    df_rep["Payment_mode_verification"] = 1
    df_rep["order confirmation"] = 1
    df_rep["personalization name"] = 1
    df_rep["Abuse"] = 1
    df_rep["Assurance"] = 1
    df_rep["Call_drop"] = 1
    df_rep["correct_hold"] = 1
    df_rep["magic_words"] = 1
    df_rep["empathy"] = 1
    df_rep["other"] = 1
    int_files = os.listdir(intent_file)
    df_modified = df_rep.copy()

    for index,row in df_rep.iterrows():
        df2 = pd.read_excel(intent_file + row["File_Name"] + ".xlsx")
        for i in intent_ls:
            x = df2["Intents"].str.contains(i).any()
            y = df2["Casual_Intents"].str.contains(i).any()
            #z = df2["Empathy_Assurance_Intents"].str.contains(i).any()
            if x == False and y ==False:
                df_modified[i][index] = 0
    sb = df_modified['Silence_Duration']/ df_modified['Duration']
    silence_calc = sb.apply(lambda x: 1 if x >0.5 else 0)
    
    overlap_calc = df_modified['Total_Overlap_Duration'].apply(lambda x: 1 if x > 5 else 0)
    
    max_ovl_calc = df_modified['Max_Overlap_Duration'].apply(lambda x: 1 if x > 2 else 0)
    
    dur_calc = df_modified['Duration'].apply(lambda x: 1 if x > 180 else 0)
    
    df_modified["scores"] = round((df_modified["Opening"] + df_modified["Closing"] + df_modified["Suggestive_Selling"] + df_modified["Address_confirmation"] + df_modified["Payment_mode_verification"] + df_modified["order confirmation"] + df_modified["personalization name"] + df_modified["Abuse"] + df_modified["Assurance"] + df_modified["Call_drop"] + df_modified["correct_hold"] + df_modified["magic_words"] + df_modified["empathy"] + df_modified["other"] +  silence_calc + overlap_calc + max_ovl_calc + dur_calc) * 100/17)

    #print(df_modified["scores"])

    from datetime import datetime as d
    date = d.now()
    x = date.strftime("%Y-%m-%d")
    df_modified.to_excel("/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/consolidated_reports/final_consolidated_rep_" + str(x) + ".xlsx")



############################################################################################
####                                                                                    ####
####                    Save Dataframe to Excel File                                    ####
####                                                                                    ####
############################################################################################

"""
This function concludes all the integrations and operations into this one as it returns the output for Speaker Diarization,
Overlap, Emotion Model Percentages and dataframes
"""
def save_as_xlsx():
    # Code for Diarization integration to report

    import metadata_xyzz
    start_time_dia = time.time()
    #tst, sil, mxsl,ovlp, mxovl,ovldurr, ovldurr1, silperc, specperc, ovlperc, speaker_cn, dur, diff,l1,l11,l2,l22, l3, l33, speak_A, speak_B,df_speaker_1,df_speaker_2 = Speaker_DIA(appended_files)
    tst, sil, mxsl,ovlp, mxovl,ovldurr, ovldurr1, silperc, specperc, ovlperc,l1,l11 = Speaker_DIA(appended_8k)
    print(len(l1))
    print(" ----%s Speaker Diarization Time in seconds ------" % (time.time() - start_time_dia))
    da1 = np.array(tst)
    da2 = np.array(sil)
    da3 = np.array(mxsl)
    da4 = np.array(ovlp)
    da5 = np.array(mxovl)
    # da6 = np.array(ovldurr)
    x = metadata_xyzz.metadata_func()
    dataframe = x
    dataframe["Total_Speech_Time"] = da1
    dataframe["Silence_Duration"] = da2
    dataframe["Max_Silence_Duration"] = da3
    dataframe["Total_Overlap_Duration"] = da4
    dataframe["Max_Overlap_Duration"] = da5

    dataframe.to_excel('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Final_Report.xlsx',index=False)
    # dataframe.to_excel("Files/Reports/Final_Report.xlsx", index=False)

    # End diarization module integration

    """Files Split """
    """

    file_list = os.listdir(appended_8k)
    stat = []
    n1 = 1

    for file in file_list:
        import soundfile as sf
        start_times_A = l1
        end_times_A = l11
        #start_times_B = l2
        #end_times_B = l22
        #start_times_C = l3
        #end_times_C = l33


        f= sf.SoundFile(appended_8k + file)
        duration = len(f) / f.samplerate
        speakers = 3
        #if not start_times_B:
            #speakers = 1
        #elif not start_times_C:
            #speakers = 2

        #if (end_times_A - start_times_A > 1 and end_times_B - start_times_B > 1):
        #stat.append([(os.path.splitext(os.path.basename(file))[0]),(duration/3),speakers])
        print("Printing in File split function!!!!!!!!!",len(start_times_A))
        split_audio_file(sentences_path, appended_8k + file, start_times_A, end_times_A)
        #split_audio_file(sentences_path, appended_8k + file, start_times_B, end_times_B, "B")
        #split_audio_file(sentences_path, appended_8k + file, start_times_C, end_times_C, "C")

        #else:
            #continue
        """

    """ Files Split"""

    print("KALDI TRANSCRIPTION SECTION: ")
    start_time2 = time.time()

    import transcription_kaldi_log as tr
    trans,file_name,dir_name = tr.Transcriptions()
    df_trans = pd.DataFrame()
    tr_lis = []
    intent_lis = []
    intent_lis1 = []
    intent_lis2 = []
    for f in trans:
        x = f.split(" ")
        x.pop(0)
        y = ' '.join(word for word in x)
        #print(type(y))
        intent_label = tr.predict_intent(y)
        intent_label1 = tr.predict_intent_casual(y)
        #intent_label2 = tr.predict_empathy_courtesy(y)
        intent_lis.append(intent_label)
        intent_lis1.append(intent_label1)
        #intent_lis2.append(intent_label2)
        tr_lis.append(y)

    print(" ----%s seconds ------" % (time.time() - start_time2))


    df_trans["Transcription"] = tr_lis
    df_trans["File_Name"] = file_name
    df_trans["Intents"] = intent_lis
    df_trans["Casual_Intents"] = intent_lis1
    #df_trans["Empathy_Assurance_Intents"] = intent_lis2
    df_trans_file = pd.DataFrame()
    df_trans_file["Main_File"] = dir_name
    unique = df_trans_file['Main_File'].unique()
    print(df_trans)
    print("Test for transcriptions...")
# Stores the Dataframe results to an excel sheet
    for item in unique:
        df_trans_file = df_trans_file[df_trans_file['Main_File'] == item]
        df_trans.to_excel('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/temp_excel/' + item +'.xlsx', index=False)


    temp_to_asr_rep()

    intent_write()
    print(" ----%s Speaker Diarization Time in seconds ------" % (time.time() - start_time_dia))

    #return dataframe, ovldurr, ovldurr1, silperc, specperc, ovlperc, speaker_cn, dur, diff,l1,l11,l2,l22, speak_A,speak_B
    return dataframe, ovldurr, ovldurr1, silperc, specperc, ovlperc,l1,l11

if __name__ == "__main__":
    print("Start Main Function!!!!!")
    start_time_main = time.time()
    main()
    print("Total Time for Noise Supression:" + str(ls_ns_tm_calc))
    print("Total Time of Execution ----%s seconds ------" % (time.time() - start_time_main))
