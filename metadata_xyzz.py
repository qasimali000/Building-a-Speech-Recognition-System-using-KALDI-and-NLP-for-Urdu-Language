import librosa.display
import librosa.util
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
from datetime import date
#from keras.preprocessing import image
#from keras.models import model_from_json
#import Model_loader
# "Type_Date-Time_ref_PhoneNumber"


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



#   save_as_xlsx(df) # save Campaign Wise dataframe


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

    return Type, Date_New, Time, ref, Phonenumber, file


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
    import Model_loader
    df = pd.DataFrame(data, columns=['Campaign', 'Date', 'Call Time', 'Caller Number', 'Duration', 'Agent ID','File_Name'])
    z = Model_loader

    data_array = np.array ( z.a )
    print("data_array ================: ", data_array)
    print("df ======================:   ", df)
    df['Flag'] = data_array
    print(df.head())
    return df


############################################################################################
####                                                                                    ####
####                    Save Dataframe to Excel File                                    ####
####                                                                                    ####
############################################################################################


def metadata_func():

    pathAudio = 'Files/wav'

        # res = Spectogram_CNN.model.predict(pathAudio)
        # print("Test for model prediction:")
        # print(res)
    files = librosa.util.find_files(pathAudio) # Extract Filename from folder and save into files array

    data = [] # initiate an empty array to save the metadata
    print("length of files ================= ", len(files))
    for file in files:
        signal, sr = load_audio_recording(file) # extract audio signal
        time = total_duration_of_call(signal, sr) # duration of the call

        Campaign, Date, Time, Ref, CallerNumber, file_nm = name_date_time_number(Path(file).name)
        data.append([Campaign, Date, Time, CallerNumber, int(time), Ref,file_nm]) # append metadata in the array

    print("data =============================:", data)

    data_array = np.array(data) # convert data to numpy array
    df = create_data_frame(data_array) # create a dataframe from array
    print("data array :", data_array)

    print(df)

    return df

