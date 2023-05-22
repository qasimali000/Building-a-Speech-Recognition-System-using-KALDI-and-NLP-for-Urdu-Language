import os
import csv
from random import shuffle
from shutil import copyfile
from tqdm import tqdm

kaldi_root = '../../'
kaldi_tools = os.path.join(kaldi_root, 'tools')
kaldi_examples = os.path.join(kaldi_root, 'egs')


traintext = open('data/train/text', 'w')
trainscp = open('data/train/wav.scp', 'w')
trainutt2spk = open('data/train/utt2spk', 'w')

testtext = open('data/test/text', 'w')
testscp = open('data/test/wav.scp', 'w')
testutt2spk = open('data/test/utt2spk', 'w')


# Setting Paths
wav_dir = 'audio/csalt'
transc_path = 'audio/csalt_transcription.txt'

with open(transc_path, 'r') as transc:
    # Preparing Data
    lines = transc.readlines()
    wavfiles = next(os.walk(wav_dir))[2]
    shuffle(wavfiles)
    shuffle(wavfiles)
    index = int(len(wavfiles) * 0.9)
    trainfiles = wavfiles[:index]
    testfiles = wavfiles[index:]

    for wav in tqdm(trainfiles):
        source_path = os.path.join(wav_dir, wav)
        wavname = os.path.splitext(wav)[0]

        a = "csalt_speaker_" + wavname + lines[int(wav[1: -4]) - 1].strip()
        traintext.write(a + '\n')
        # Writing to data/train/wav.scp
        b = "csalt_speaker_" + wavname + source_path
        trainscp.write(b + '\n')

        # Writing to data/train/utt2spk
        c = "csalt_speaker_" + wavname + " csalt_speaker"
        trainutt2spk.write(c + '\n')
#
    for wav in tqdm(testfiles):
        source_path = os.path.join(wav_dir, wav)
        wavname = os.path.splitext(wav)[0]

        # Writing to data/test/text
        a = "csalt_speaker_" + wavname + lines[int(wav[1: -4]) - 1].strip()
        testtext.write(a + '\n')

        # Writing to data/test/wav.scp
        b = "csalt_speaker_" + wavname + source_path
        testscp.write(b + '\n')

        # Writing to data/test/utt2spk
        c = "csalt_speaker_" + wavname + " csalt_speaker"
        testutt2spk.write(c + '\n')


wav_dir = 'audio/rumi'
transc_path = 'audio/rumi_transcription.txt'


with open(transc_path, 'r', encoding = 'utf8') as transc:
    lines = transc.readlines()
    transcription = {line.split(' ', 1)[0]: line.split(' ', 1)[1].strip() for line in lines}


for speaker in next(os.walk(wav_dir))[1]:

    wavfiles = next(os.walk(os.path.join(wav_dir, speaker)))[2]
    shuffle(wavfiles)
    shuffle(wavfiles)
    index = int(len(wavfiles) * 0.9)
    trainfiles = wavfiles[:index]
    testfiles = wavfiles[index:]

    for wav in tqdm(trainfiles):
        source_path = os.path.join(wav_dir, speaker, wav)
        wavname = os.path.splitext(wav)[0]

        # Writing to data/train/text
        a = "rumi_speaker_" + speaker + "_" + wavname + " " + transcription[wavname]
        traintext.write(a + '\n')

        # Writing to data/train/wav.scp
        b = "rumi_speaker_" + speaker + "_" + wavname + " " + source_path
        trainscp.write(b + '\n')

        # Writing to data/train/utt2spk
        c = "rumi_speaker_" + speaker + "_" + wavname + " " + " rumi_speaker_" + speaker
        trainutt2spk.write(c + '\n')

    for wav in tqdm(testfiles):
        source_path = os.path.join(wav_dir, speaker, wav)
        wavname = os.path.splitext(wav)[0]

        # Writing to data/test/text
        a = "rumi_speaker_" + speaker + "_" + wavname + " "+ transcription[wavname]
        testtext.write(a + '\n')

        # Writing to data/test/wav.scp
        b = "rumi_speaker_" + speaker + "_" + wavname + " "+ source_path
        testscp.write(b + '\n')

        # Writing to data/test/utt2spk
        c = "rumi_speaker_" + speaker + "_" + wavname + " "+ " rumi_speaker_" + speaker
        testutt2spk.write(c + '\n')


traintext.close()
trainscp.close()
trainutt2spk.close()

testtext.close()
testscp.close()
testutt2spk.close()