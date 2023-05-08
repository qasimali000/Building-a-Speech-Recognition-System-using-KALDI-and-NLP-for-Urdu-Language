"""
Version: 0.0.1
Author: Qasim Ali
Company: Sybrid Pvt. Ltd.
Pyannote Speaker Diarization and Speaker Overlap Detection.

This file contains the code which returns the output for Speaker Diarization, Silence Detection and Sepeaker Overlap Detection.
"""

import os
import torch
from multiprocessing import Process, freeze_support
import numpy as np
import pandas as pd
import librosa
from pathlib import Path
from pydub import AudioSegment

#variables and list declrations to store speakers start and end times

start_speaker_1, end_speaker_1,start_speaker_2, end_speaker_2, start_speaker_3, end_speaker_3= [],[],[],[],[],[]

"""
The Following function provides the functionality for Speaker diarization, performs calculations to get silence, Speakers
and Speaker's Start and End time which is also used in Emotion Detection.
"""
rttm_path = 'Files/rttm/'
# Speaker Diarization Start
def dia(ff):
    pipeline = torch.hub.load ( 'pyannote/pyannote-audio' , 'dia', device='gpu' )  #Load a prebuilt model from Pyannote Library
    file = AudioSegment.from_wav(ff)        # Input audio file on which all the operations are performed which is actual audio file.

# Take the length of audio file which will be used to get actual timelines based on the fact that the files are being appended.
    n = len(file)
    n = n/1000
    n1 = round(n/3)

    # apply diarization pipeline on your audio file
    diarization = pipeline ( {'audio': ff} )
    a = os.path.basename(ff)
    name , ext = os.path.splitext(a)

    # dump result to disk using RTTM format
    with open (rttm_path + name + '_audio.rttm' , 'w' ) as f:
        diarization.write_rttm ( f )

    # iterate over speech turns
    ress = 0
    ress1 = 0
    ress2 = 0
    l1 = []     # Speaker A's Speech Start Time
    l11 = []    # Speaker A's Speech End Time
    l2 = []     # Speaker B's Speech Start Time
    l22 = []    # Speaker B's Speech End Time
    l3 = []    # Speaker B's Speech End Time
    l33 = []    # Speaker B's Speech End Time
    sil1 = 0    # Minimum Silence Var for IF Condition
    sil2 = 0    # Maximum Silence Var for IF Condition
    sil3 = 0    # Maximum Silence Var for IF Condition
    maxsil = 0  # Var for Maximum Silence
    minsil = 0  # Var for Minimum Silence
    speaker_cn = ''
    speaker_cn1 = ''
    speaker_cn2 = ''
    count = 0
    speak_A = []
    speak_B = []
    speak_C = []
    turn_start = []
    turn_end = []
    start_new = []
    end_new = []
    difference = []

    """
    The following loop start the main diarization operation as we are getting start and end time of each speaker, also the 
    label for each identified speaker in the call.
    """
    for turn , _ , speaker in diarization.itertracks ( yield_label = True ):
        res = turn.end - turn.start
        print ( f'Speaker "{speaker}" speaks between t={turn.start:.1f}s and t={turn.end:.1f}s.' )
        print(res)

        turn_start.append(turn.start)
        turn_end.append(turn.end)

        if speaker == 'A':
            sm = turn.end - turn.start
            print("Silence Timelines: " + str(sm))
            # For Emotional API Part
            start_speaker_1.append(round(turn.start))
            end_speaker_1.append(round(turn.end))
            # For Emotional API Part

            ress += sm      # Calculating the Total Speech time of Speaker A for each iteration
            speak_A.append(sm)      # Storing the speaker A's Speech duration for each iteration
            l1.append(turn.start)    # Storing the Speaker A's Speech start timelines in a list
            l11.append(turn.end)     # Storing the Speaker A's Speech end timelines in a list

            speaker_cn = speaker

            # Silence in Speech Start
            #if sil1 is None or sil1 > res:
            #    minsil = res
            #elif sil2 is None or sil2 <= res:
            #    maxsil = res
            # Silence in Speech End
        elif speaker == 'B':
            #For Emotional API Part
            start_speaker_2.append(turn.start)
            end_speaker_2.append(turn.end)
            # For Emotional API Part
            count = 1
            sm = turn.end - turn.start
            print("Silence Timelines: " + str(sm))
            ress1 += sm     # Calculating the Total Speech time of Speaker B for each iteration
            speak_B.append(sm)
            l2.append(turn.start)    # Appending the Speaker B Start Time to a list for use in Visualizations
            l22.append(turn.end)     # Appending the Speaker B End Time to a list for use in Visualizations
            speaker_cn1 = speaker

            # Silence Calculation
            #if sil1 is None or sil1 > res:
            #    minsil = res
            #elif sil2 is None or sil2 <= res:
            #    maxsil = res

        elif speaker == 'C':
            #For Emotional API Part
            start_speaker_3.append(turn.start)
            end_speaker_3.append(turn.end)
            # For Emotional API Part
            count = 1
            sm = turn.end - turn.start
            print("Silence Timelines: " + str(sm))
            ress2 += sm     # Calculating the Total Speech time of Speaker B for each iteration
            speak_C.append(sm)
            l3.append(turn.start)    # Appending the Speaker B Start Time to a list for use in Visualizations
            l33.append(turn.end)     # Appending the Speaker B End Time to a list for use in Visualizations
            speaker_cn2 = speaker

            # Silence Calculation
            #if sil1 is None or sil1 > res:
            #    minsil = res
            #elif sil2 is None or sil2 <= res:
            #    maxsil = res

######################## Silence Calculation #############################

    for start in turn_start[1:]:
        start_new.append(start)
    for end in turn_end[:-1]:
        end_new.append(end)


    print(start_new)
    print(end_new)
    # print(list(set(start_new) - set(end_new)))

    zip_object = zip(start_new, end_new)
    for list1_i, list2_i in zip_object:
        difference.append(list1_i - list2_i)

    print(difference)
    maxsil = max(difference)
    print(max(difference))
    minsil = min(difference)
    print(min(difference))
    tot_sil = sum(difference)
    sil2 = tot_sil/3
    #print(tot_sil)
    #print(actual_sil)

#######################Silence Calculation #################################

        # print(res + ress)
    print("Speaker A :",ress)
    print("Speaker B :",ress1)
    print("Speaker C :",ress2)
    tst = ress + ress1 + ress2
    tst1 = round(tst/3) # In case if file is appended 3 times
    print("Total Speaking Time:", tst1)
    #sil = n - tst
    #sil2 = sil/3
    #sil2 = n1 - tst1
    #sil2 = round(sil/3) # In case if file is appended 3 times
    print("Total Silence:",sil2)
    print("Length: ",n1)
    # Percentages
    # n1 = n/3

    # Calculating Silence Percentage for USER INTERFACE
    silPerc = round(sil2 / n1 * 100)

    # Calculating Speech Percentage for USER INTERFACE
    specPerc = round(tst1/n1 * 100)


    # Filtering Speech timeline for Speaker A
    l1_S = [number for number in l1 if number <= n1]
    l11_E = [number for number in l11 if number <= n1]

    # Filtering Speech timeline for Speaker B
    l2_S = [number for number in l2 if number <= n1]
    l22_E = [number for number in l22 if number <= n1]

    # Filtering Speech timeline for Speaker B
    l3_S = [number for number in l3 if number <= n1]
    l33_E = [number for number in l33 if number <= n1]


    # For emotion detection API
    df_speaker_1 = pd.DataFrame(columns = ['start_time', 'end_time'])
    df_speaker_2 = pd.DataFrame(columns=['start_time', 'end_time'])
    df_speaker_3 = pd.DataFrame(columns=['start_time', 'end_time'])

    # Filtering Speaker's Start and End time for original duration
    # start_speaker_1_actual = [number for number in start_speaker_1 if number <= 142]#start time
    # end_speaker_1_actual = [number for number in end_speaker_1 if number <= 142] # end time of A
    # print(start_speaker_1_actual)
    # print(end_speaker_1_actual)


    #Filtering Speaker's Start and End time for original duration
    # start_speaker_2_actual = [number for number in start_speaker_2 if number < n1]
    # end_speaker_2_actual = [number for number in end_speaker_2 if number < n1]
    # print(start_speaker_2_actual)
    # print(end_speaker_2_actual)

    df_speaker_1['start_time']= start_speaker_1
    df_speaker_1['end_time'] = end_speaker_1
    df_speaker_2['start_time']= start_speaker_2
    df_speaker_2['end_time'] = end_speaker_2
    df_speaker_3['start_time']= start_speaker_3
    df_speaker_3['end_time'] = end_speaker_3

    index = df_speaker_1.index
    # print(index)
    df_speaker_1 = df_speaker_1.head(int(len(index) / 3))

    index2 = df_speaker_2.index
    # print(index)
    df_speaker_2 = df_speaker_2.head(int(len(index2) / 3))

    index3 = df_speaker_3.index
    # print(index)
    df_speaker_3 = df_speaker_3.head(int(len(index3) / 3))
    # For Emotion Detection API
    #return tst1, sil2, round(maxsil), silPerc, specPerc, count, n1, l1,l11,l2,l22,l3,l33, speak_A,speak_B, df_speaker_1,df_speaker_2

# Speaker Diarization End

############## Update 24/11/2021 #####################

def sad(file):
    pipeline = torch.hub.load ( 'pyannote/pyannote-audio' , 'sad', pipeline=True)

    # apply diarization pipeline on your audio file
    speech_activity_detection = pipeline ( {'audio': file})
    ff = AudioSegment.from_wav(file)
    n = len(ff)
    n = n/1000
    n1 = round(n/3)

    a = os.path.basename(file)
    name , ext = os.path.splitext(a)

    # dump result to disk using RTTM format
    with open (rttm_path + name + '_audio.sad.rttm' , 'w' ) as f:
        speech_activity_detection.write_rttm ( f )


    res1 = 0
    res2 = 0
    sil = 0

    ress = 0
    ress1 = 0
    ress2 = 0
    turn_start = []
    turn_end = []
    start_new = []
    end_new = []
    difference = []



    # iterate over speech turns
    for speech_region in speech_activity_detection.get_timeline():
        rs = speech_region.end - speech_region.start
        turn_start.append(speech_region.start)
        turn_end.append(speech_region.end)
        ress +=rs
        print ( f'There is speech between t={speech_region.start:.1f}s and t={speech_region.end:.1f}s.' )
        if res1 is None or res1 > rs:
            res1 = rs
        elif res2 is None or res2 <= rs:
            res2 = rs

    tst = ress
    tst1 = round(tst/3)

   ######################## Silence Calculation #############################

    for start in turn_start[1:]:
        start_new.append(start)
    for end in turn_end[:-1]:
        end_new.append(end)


    print(start_new)
    print(end_new)
    # print(list(set(start_new) - set(end_new)))

    zip_object = zip(start_new, end_new)
    for list1_i, list2_i in zip_object:
        difference.append(list1_i - list2_i)

    print(difference)
    maxsil = max(difference)
    print(max(difference))
    minsil = min(difference)
    print(min(difference))
    tot_sil = sum(difference)
    sil2 = tot_sil/3
    #print(tot_sil)
    #print(actual_sil)

#######################Silence Calculation #################################
    # Calculating Silence Percentage for USER INTERFACE
    silPerc = round(sil2 / n1 * 100)

    # Calculating Speech Percentage for USER INTERFACE
    specPerc = round(tst1/n1 * 100)

    print("Max Silence:",res2)
    print("Min Silence:",res1)
    print("Turn Start Length",len(turn_start))
    print("Turn End Length",len(turn_end))
#tst, sil, maxsil, silperc, specperc,l1,l11
    return tst1, sil2, round(maxsil), silPerc, specPerc, turn_start,turn_end
# Speech activity detection (SAD)




################# Update 24/11/2021 ##################

# Speaker overlap detection (SOD) Start

"""
The Following function provides the functionality for Speaker Overlap Detection, performs calculations to get Total Overlap
Duration, Maximum Overlap and the overlap percentage calculation for USER INTERFACE
"""

def sod(filename):

    # The following line of code loads the Speaker Overlap Detection's Pre-Built Pipeline from Pyannote Library
    pipeline = torch.hub.load ( 'pyannote/pyannote-audio' , 'ovl', pipeline = True)
    file = AudioSegment.from_wav(filename)      # Load the Appended Wav Audio file passed from UI
    n = len(file)      # Takes the length of the file
    n = n / 1000        # Converting Milliseconds to Seconds
    n1 = n / 3          # Dividin the file duration with the times the original file is appended to get original duration

    # apply diarization overlap pipeline on your audio file
    diarization = pipeline ( {'audio': filename} )

    a = os.path.basename(filename)
    name , ext = os.path.splitext(a)

    # dump result to disk using RTTM format
    with open (rttm_path + name + 'ovr_audio.rttm' , 'w' ) as f:
        diarization.write_rttm ( f )

    # iterate over speech turns
    ress = 0    # Var for Total Overlap Time
    ress1 = 0   # Var for Maximum Overlap Time
    ress2 = 0   # Var for Minimum Overlap Time
    ovr1 = []   # List to get Overlap Start times
    ovr2 = []   # List to get Overlap End times
    diff = []   # Calculating difference for UI Bar Graph

    """
    The following loop start the main overlap detection operation as we are getting start and end times where overlap is
    detected, we also aim to find the Speaker Label from which overlap is being initiated in future
    """

    for turn in diarization.get_timeline():
        res = turn.end - turn.start
        ress += res # Gets the total overlap duration
        print(f'Overlap between t={turn.start:.1f}s and t={turn.end:.1f}s.' )
        ovrr1 = turn.start
        ovrr2 = turn.end
        ovr1.append(round(ovrr1))   # Appends the overlap start times to a list
        ovr2.append(round(ovrr2))   # Appends the overlap end times to a list
        a = turn.end - turn.start
        diff.append(a)  # Appends the differences for each overlap instances

        print(res)
        if ress1 is None or res > ress1:
            ress1 = res
        elif ress2 is None or res <= ress2:
            ress2 = res

    ovr11 = [number for number in ovr1 if number < n1]  # Getting the overlap Start Time for original duration of the call
    ovr22 = [number for number in ovr2 if number < n1]  # Getting the overlap End Time for original duration of the call

    ovlPerc = round(ress / n1 * 100)    # Calculating Overalp Percentage in the audio

    return round(ress/3), round(ress1), ovr11, ovr22, ovlPerc, diff
# Speaker overlap detection (SOD)

