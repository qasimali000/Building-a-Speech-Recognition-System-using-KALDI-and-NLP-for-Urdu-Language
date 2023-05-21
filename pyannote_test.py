"""
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

