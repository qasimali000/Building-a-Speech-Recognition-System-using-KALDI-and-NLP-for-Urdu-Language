import librosa.display
import librosa.util
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
from datetime import date
from keras.preprocessing import image
from keras.models import model_from_json
from ModelfromYasir.Report_Test import Model_loader
# from ModelfromYasir.Report_Test import silence_det as ml
# "Type_Date-Time_ref_PhoneNumber"
import os
# Test code for my-voice-analysis library test
mysp = __import__("my-voice-analysis")

# p = "IWOOD_20200521-020926_itw36164_34617535-CC"
# c = r"E:\\Audio Analytics\\Audio-Analytics-20200819T083957Z-001\\Audio-Analytics\\Data\\mp3 sample"
# mysp.myspbala(p,c) # ratio
# mysp.myspst(p,c) # speaking duration without pauses
# mysp.myspgend(p,c)

# Test code for my-voice-analysis library test

############################################################################################
####                                                                                    ####
####                                   MAIN FUNCTION                                    ####
####                                                                                    ####
############################################################################################


def main():
    """
    Summary of the function:
    This function calls various function to extract metadata from the audio signal and save them in the form of
    excel files.

    """
    # Loading model here

    pathAudio = 'E:\\Audio Analytics\\Audio-Analytics-20200819T083957Z-001\\Audio-Analytics\\Data\\MCDONALD WAV'

    # print(os.path.basename(pathAudio))
    # res = Spectogram_CNN.model.predict(pathAudio)
    # print("Test for model prediction:")

    files = librosa.util.find_files(pathAudio) # Extract Filename from folder and save into files array
    # mv = Path ( files ).name
    print ( files[0] )


    data = [] # initiate an empty array to save the metadata

    for file in files:
        signal, sr = load_audio_recording(file) # extract audio signal
        time = total_duration_of_call(signal, sr) # duration of the call
        # det_pause(file)
        Campaign, Date, Time, Ref, CallerNumber = name_date_time_number(Path(file).name)
        data.append([Campaign, Date, Time, CallerNumber, int(time), Ref]) # append metadata in the array
        # mysp.myspbala ( file , file )
        # sil_dur(file)

    data_array = np.array(data) # convert data to numpy array
    df = create_data_frame(data_array) # create a dataframe from array

    save_as_xlsx(df) # save Campaign Wise dataframe
    # dtarr = np.array ( ml.s )
    # print ( dtarr )
    # sil_dur()


############################################################################################
####                                                                                    ####
####                               LOAD RECORDING FILES                                 ####
####                                                                                    ####
############################################################################################


def load_audio_recording(file):  # loading the waveform
    """

    :param file: Name and location of the file:
    :return: The digitized audio signal, Sampling rate:
    """
    signal, sr = librosa.load(file, sr=8000)  # default sr = 22050 Keeping Sampling rate low to allow fast processing
    # as we only need duaration of call in this
    return signal, sr


############################################################################################
####                                                                                    ####
####                           Calculate Duration of the Call                           ####
####                                                                                    ####
############################################################################################


def total_duration_of_call(signal, sr):  # function for call duration
    """
    :param signal:
    :param sr: Sampling Rate:
    :return: Duration of the call:
    """
    # import datetime
    time = round(librosa.get_duration(signal, sr=sr), 2)
    return time



############################################################################################
####                                                                                    ####
####             Finding the Silence/Pause duration in the call                         ####
####                                                                                    ####
############################################################################################


# def sil_dur(file):
    # Import the AudioSegment class for processing audio and the
    # split_on_silence function for separating out silent chunks.
    # from pydub import AudioSegment
    # from pydub.silence import split_on_silence
    #
    # # Define a function to normalize a chunk to a target amplitude.
    # def match_target_amplitude(aChunk , target_dBFS):
    #     ''' Normalize given audio chunk '''
    #     change_in_dBFS = target_dBFS - aChunk.dBFS
    #     return aChunk.apply_gain ( change_in_dBFS )
    #
    # # Load your audio.
    # # song = AudioSegment.from_wav (
    # #     "E:\\Audio Analytics\\Audio-Analytics-20200819T083957Z-001\\Audio-Analytics\\Data\\MCDONALD WAV\\Unusual\\MCDONALD_20200506-214227_cmt35271_03338777704-CC.wav" )
    #
    # song = AudioSegment.from_wav(file)
    # # print(song)
    # # Split track where the silence is 2 seconds or more and get chunks using
    # # the imported function.
    # chunks = split_on_silence (
    #     # Use the loaded audio.
    #     song ,
    #     # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
    #     min_silence_len = 2000 ,
    #     # Consider a chunk silent if it's quieter than -16 dBFS.
    #     # (You may want to adjust this parameter.)
    #     silence_thresh = -17
    #     )
    # s = []
    # # Process each chunk with your parameters
    # for i , chunk in enumerate ( chunks ):
    #     # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
    #     silence_chunk = AudioSegment.silent ( duration = 500 )
    #
    #     # Add the padding chunk to beginning and end of the entire chunk.
    #     audio_chunk = silence_chunk + chunk + silence_chunk
    #
    #     # Normalize the entire chunk.
    #     normalized_chunk = match_target_amplitude ( audio_chunk , -20.0 )
    #     s.append(len(normalized_chunk)/1000)
    #
    #     print ( "Pause Duration: " , len ( normalized_chunk ) / 1000 )
    #     # Export the audio chunk with new bitrate.
    #     print ( "Exporting chunk{0}.wav.".format ( i ) )
    #     # normalized_chunk.export (
    #     #     ".//chunk{0}.wav".format ( i ) ,
    #     #     bitrate = "256k" ,
    #     #     format = "wav"
    #     #     )
    #     normalized_chunk.export(
    #         "E:\Audio Analytics\Audio-Analytics-20200819T083957Z-001\Audio-Analytics\Data\pause\chunk.wav" ,
    #         bitrate = "256k" ,
    #         format = "wav"
    #         )

    # dtarr = np.array(ml.s)
    # print(dtarr)


############################################################################################
####                                                                                    ####
####          Extract Campaign, Time, Date, Call Reference, and Number                  ####
####                                                                                    ####
############################################################################################

def name_date_time_number(file):
    """
    Summary of the Function
    Input: Audio File Title
    Output Returns: Campaign Name, Data_of_Call, Time_of_Call, CRE_ReferenceNumber, CallerPhoneNumber

    File Name Follows the pattern: Campaign_Date-Time_CREREF_CallerNumber
    """

    file = os.path.splitext(file)[0]

    temp = file.split("_")  # Split File Name at each '_' and save them in temp

    Type = temp[0]  # Campaign Name
    Date = temp[1]  # Date and time combined
    ref = temp[2]  # CRE Reference Number
    Phonenumber = temp[3]  # Caller Number

    Time = Date[Date.find("-") + 1:]  # Separate Time from Date
    Date = Date.replace(f"-{Time}", "")  # Remove TIme from Date

    try:
        Date_New = int2date(int(Date))  # Concert Date Integer to Date
        Time = get_time(Time)  # Get time in HH:MM

    except ValueError:
        Date_New = Date
        Time = Time

    return Type, Date_New, Time, ref, Phonenumber

def det_pause(file):
    sl = librosa.effects.trim(y = file,top_db = 40, frame_length = 8000)
    print(sl)
############################################################################################
####                                                                                    ####
####                           Convert Integer Date to Dat                              ####
####                                                                                    ####
############################################################################################


def int2date(argdate: int) -> date:
    """
    If you have date as an integer, use this method to obtain a datetime.date object.

    Parameters
    ----------
    argdate : int
      Date as a regular integer value (example: 20160618)

    Returns
    -------
    dateandtime.date
      A date object which corresponds to the given value `argdate`.
    """
    year = int(argdate / 10000)
    month = int((argdate % 10000) / 100)
    day = int(argdate % 100)

    return date(year, month, day)


############################################################################################
####                                                                                    ####
####                         Convert Integer time to Time                               ####
####                                                                                    ####
############################################################################################

def get_time(t):
    t = t[:2] + ':' + t[2:4]
    return t


############################################################################################
####                                                                                    ####
####                     Create Data Frame                                              ####
####                                                                                    ####
############################################################################################

def create_data_frame(data):
    df = pd.DataFrame(data, columns=['Campaign', 'Date', 'Call Time', 'Caller Number', 'Duration', 'Agent ID'])
    z = Model_loader

    data_array = np.array ( z.a )
    df['Flag'] = data_array

    #print(df.head())
    return df


############################################################################################
####                                                                                    ####
####                    Save Dataframe to Excel File                                    ####
####                                                                                    ####
############################################################################################


def save_as_xlsx(dataframe):
    unique = dataframe['Campaign'].unique()

    for item in unique:
        df = dataframe[dataframe['Campaign'] == item]
        df.to_excel(r'E:\Audio Analytics\Audio-Analytics-20200819T083957Z-001\Audio-Analytics\Data\output' + item +
                    '.xlsx', index=False)


if __name__ == "__main__":
    main()
