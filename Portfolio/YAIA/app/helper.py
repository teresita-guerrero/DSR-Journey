# -*- coding: utf-8 -*-


from summarizer import *
from pipeline import dataProcessPipeline, predictingSummary, \
    getPredictedSentences
import pandas as pd
import nltk
from email_endpoints import apiRequestMailByID
import re
import numpy as np


def singleSummary(threadID, email):
    text = email[threadID].get("message_content", [])
    summary = getTextSummary(text)
    return summary

def threadSummary(thread):
    # Processing the data
    eData = getDataFrameBase(thread)
    tData = dataProcessPipeline(eData)
    path = "ml_models/"

    # choose the model to apply
    # 1.- bagging_model.pkl
    # 2.- dt_model.pkl
    # 3.- rf_model.pkl
    # 4.- svm_model.pkl
    # 5.- gnb_model.pkl

    # default: bagging_model.pkl
    modelName = "bagging_model.pkl"
    prediction = predictingSummary(path, modelName, tData)
    predictedSentences = getPredictedSentences(prediction, 1, eData)
    predictedSentences.drop_duplicates(subset=["sentence_content"], inplace=True)

    summary = [row["sentence_content"].capitalize()
               for _, row in predictedSentences.iterrows()]

    return {"summary": summary}


def getDataFrameBase(thread):
    # defining the base dataframe
    eData = pd.DataFrame(columns=["thread_num", "id", "name", "received",
                                  "from", "to", "subject", "sentence_id",
                                  "sentence_content"])

    emailNumber = 1
    for messageID in thread:
        m = apiRequestMailByID(messageID).get_json()

        # ToDo: as GMail returns the reply mail in the body, it is necessary
        # to implement a cleaning method to remove them from the message
        mCleaned = re.sub('[\n\r]', ' ', m['message_content'])

        # tokenize the sentences
        normalizedSentences = tokenizeEmail(mCleaned)

        replySentence = False
        sentenceNumber = 0.1
        for sentence in normalizedSentences:
            # ToDo: move this to a more fancy cleaning function
            for word in sentence:
                replySentence = np.isin(">", word)
                if replySentence:
                    break

            if replySentence == False:
                eData = eData.append({
                    "thread_num": 1,
                    "id": m["id"],
                    "name": m["subject"],
                    "received": m["received"],
                    "from": m["from"],
                    "to": m["to"],
                    "subject": m["subject"],
                    "sentence_id": emailNumber + sentenceNumber,
                    "sentence_content": sentence
                }, ignore_index=True)

                sentenceNumber += 0.1
        emailNumber += 1

    return eData


def tokenizeEmail(txt):
    # get the sentences in the txt
    sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
    # normalizing sentences to lowercase
    normalizedSentences = [s.lower() for s in sentences]
    return normalizedSentences