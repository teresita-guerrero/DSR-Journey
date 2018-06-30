# -*- coding: utf-8 -*-


from summarizer import *
from pipeline import dataProcessPipeline, predictingSummary, \
    getPredictedSentences
import pandas as pd
import nltk
from email_endpoints import apiRequestMailByID
import re


def singleSummary(threadID, email):
    text = email[threadID].get("message_content", [])
    summary = getTextSummary(text)
    return summary

def threadSummary(thread):
    # Processing the data
    eData = getDataFrameBase2(thread)
    tData = dataProcessPipeline(eData)
    path = "ml_models/"

    # choose the model to apply
    # 1.- bagging_model.pkl

    # default: bagging_model.pkl
    modelName = "bagging_model.pkl"
    prediction = predictingSummary(path, modelName, tData)
    predictedSentences = getPredictedSentences(prediction, 1, eData)
    summary = [row["sentence_content"].capitalize()
               for _, row in predictedSentences.iterrows()]

    return {"summary": summary}


def getDataFrameBase(thread):

    # defining the base dataframe
    eData = pd.DataFrame(columns=["thread_num", "id", "name", "received",
                                  "from", "to", "subject", "sentence_id",
                                  "sentence_content"])
    emailNumber = 1
    for key, value in thread.items():
        # tokenize the sentences
        normalizedSentences = tokenizeEmail(emailNumber,
                                            value["message_content"])

        sentenceNumber = 0.1
        for sentence in normalizedSentences:
            eData = eData.append({
                "thread_num": 1,
                "id": value["thread_num"],
                "name": value["subject"],
                "received": value["received"],
                "from": value["from"],
                "to": value["to"],
                "subject": value["subject"],
                "sentence_id": emailNumber + sentenceNumber,
                "sentence_content": sentence
            }, ignore_index=True)

            sentenceNumber += 0.1
        emailNumber += 1

    return eData

def getDataFrameBase2(thread):
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

        sentenceNumber = 0.1
        for sentence in normalizedSentences:
            if sentence[0]!= ">":
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