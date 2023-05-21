import subprocess
import os
from shutil import copyfile, copytree
import glob
import os, shutil
import pandas as pd
import pickle
src_path = "/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/diarized_sentences/"
dst_path = "/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/test/"
y = os.listdir(src_path)
z = len(y)
print(type(z))
x = []

################################


folder1 = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/scp_files/'
for filename in os.listdir(folder1):
    file_path = os.path.join(folder1, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


folder2 = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/test/'
for filename in os.listdir(folder2):
    file_path = os.path.join(folder2, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



folder3 = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/Asr_Reports/'
for filename in os.listdir(folder3):
    file_path = os.path.join(folder3, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



folder4 = '/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/temp_excel/'
for filename in os.listdir(folder4):
    file_path = os.path.join(folder4, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))




src = None
dst = None
for i in range(0,z):
    src = src_path + y[i]
    print("Printing Source File:")
    print(src)
    dst = dst_path + y[i]
    copytree(src, dst)

print(src)
import librosa
import librosa.display
os.chdir("/")


#spk2utt = []
#wav_scp = []
#utt2spk = []
#text = []

traintext = open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/scp_files/text', 'w')
trainscp = open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/scp_files/wav.scp', 'w')
trainutt2spk = open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/scp_files/utt2spk', 'w')
path = "/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/test" # wav audio path


for speaker in next(os.walk(path))[1]:
    wavfiles = next(os.walk(os.path.join(path, speaker)))[2]
    index = int(len(wavfiles) * 1.0)
    trainfiles = wavfiles[:index]


    from tqdm import tqdm
    for wav in tqdm(trainfiles):
        source_path = os.path.join(path, speaker, wav)
        wavname = os.path.splitext(wav)[0]

        a = wavname + " "
        traintext.write(a + '\n')
        # Writing to data/train/wav.scp
        b = wavname + " " + source_path
        trainscp.write(b + '\n')

        # Writing to data/train/utt2spk
        c = wavname + " test/" + speaker
        #print(c)
        trainutt2spk.write(c + '\n')
        #utt2spk.write(c + '\n')


traintext.close()
trainscp.close()
trainutt2spk.close()
os.chdir('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul')
subprocess.call(['bash','./test.sh'])

#################

path = "/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/test"
def log_scrapper(audio_file_location, log_file_location):
    important = []
    dir_name = []
    file_name = []
    for speaker in next(os.walk(path))[1]:
        dir_name.append(speaker)
        main_path = os.path.join(audio_file_location, speaker)
        audio_files = os.listdir(main_path)
        for file in audio_files:
            keep_phrases = os.path.splitext(file)[0]
            with open(log_file_location, encoding='utf-8') as f:
                f = f.readlines()
            for line in f:
                #print(line)
                if keep_phrases in line:
                    file_name.append(keep_phrases)
                    #print(keep_phrases)
                    important.append(os.path.splitext(line)[0])
                    break
    return important, file_name, dir_name



import nltk
#nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
porter = PorterStemmer()

def cleaning(sentences):
    words = []
    for s in sentences:
        #clean = re.sub(r'[^ a-z A-Z 0-9]', " " ,s)
        w = word_tokenize(s)  
        str1 = ""
        for i in w:
            # print(i)
            lemma = porter.stem(i)
# #             word = wordnet_lemmatizer.lemmatize(i,pos="v")
            str1+= lemma + " "
        words.append(str1)
    return words




def Transcriptions():
	audio_path = dst_path
	log_path = "/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/kaldi/egs/qoul/exp/sgmm2_4/decode/log/decode_pass1.1.log"

	transcription, file_name,dir_name = log_scrapper(audio_path, log_path)

	result = transcription
	return result,file_name ,dir_name
res, file, dir = Transcriptions()


def predict_intent(text):
    vectorizer = pickle.load(open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/intent_model/vectorizer.sav', 'rb'))
    classifier = pickle.load(open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/intent_model/classifier.sav', 'rb'))
    cleaned_sentences = cleaning([text])
    review_vector = vectorizer.transform(cleaned_sentences)
    label = classifier.predict(review_vector)
    labels = label[0]
    print(labels)
    return labels

def predict_intent_casual(text):
    vectorizer = pickle.load(open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/intent_casual_phrases/vectorizer.sav', 'rb'))
    classifier = pickle.load(open('/Users/qasimali/Desktop/Qasim/Aston/Dissertation/project/Pipeline/Files/intent_casual_phrases/classifier.sav', 'rb'))
    cleaned_sentences = cleaning([text])
    review_vector = vectorizer.transform(cleaned_sentences)
    label = classifier.predict(review_vector)
    labels = label[0]
    print(labels)
    return labels
