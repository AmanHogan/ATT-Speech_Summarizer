from summarizer.sbert import SBertSummarizer
import src.loggers.logger as logger
import warnings
import os
import shutil
import sys
from sentence_transformers import SentenceTransformer
import en_core_web_sm
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")

############# INIT PATHS #############
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIBED_FILE_PATH = os.path.join(SCRIPT_DIR, '../../../uploads/call-transcription.txt')
SUMMARIZED_FILE_PATH = os.path.join(SCRIPT_DIR, '../../../uploads/call-summary-text.txt')

# FUNC - Loads trained english model and runs tracription against it and returns summary
def summarizeText():
    transcribedText = None

    # Get transcribed text 
    try:
        with open(TRANSCRIBED_FILE_PATH) as fp1:
            transcribedText = fp1.read()
    except FileNotFoundError:
        logger.logData("The file "+ TRANSCRIBED_FILE_PATH + " does not exist. ")
        print("The file "+ TRANSCRIBED_FILE_PATH + " does not exist. ")


    def summarize(text, per):
        
        # Load english model and tokenize transcription
        nlp = en_core_web_sm.load()
        doc= nlp(text)
        tokens=[token.text for token in doc]

        # Create hashmap of token frequency
        word_frequencies={}
        for word in doc:
            if word.text.lower() not in list(STOP_WORDS):
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        
        # Normalize frequencies
        max_frequency= max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word]=word_frequencies[word]/max_frequency

        # Score each frequency
        sentence_tokens= [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():                            
                        sentence_scores[sent]=word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent]+=word_frequencies[word.text.lower()]
        
        # Find four sentences with the highest score
        select_length= 4
        summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)
        return summary
    
    summarizedText = summarize(str(transcribedText), 0.05)
    print(f'The summary: {summarizedText}' )

    # Save summary to a text file
    try:
        with open(SUMMARIZED_FILE_PATH, "w") as fp2:
            fp2.write(summarizedText)
        logger.logData('Summary uploaded successfully')
        print('Summary created and saved successfully')
    except :
        logger.logData("Could not write to or create file: " + SUMMARIZED_FILE_PATH)
        print('Summary unsuccessfully created or saved ')
