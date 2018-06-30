# Adding the text sentence / email features **
#    - sentence_position. The position of the sentence in the thread
#    - words_in_sentence. The number of words in the sentence
#    - is_question. Does the sentence has a question mark?
#    - position_mail. The position of the mail in the thread
#    - is_money. Does the sentence has numbers?
#    - is_date. Does the sentence has a date?
#    - is_in_title. Does a word sentence appears in the thread title?
#    - tf_idf_score. The sentence score in the mail
#    - tf_idf_total_score. The sentence score in the thread

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from summarizer import scoreSentences
from sklearn.externals import joblib


def dataProcessPipeline(eData):
    eData = sentencePosition(eData)
    eData = wordsInSentence(eData)
    eData = isQuestion(eData)
    eData = positionMail(eData)
    eData = isMoney(eData)
    eData = isDate(eData)
    eData = isInTitle(eData)
    eData = tfidfMail(eData)
    eData = tfidfThread(eData)
    dTest = getFinalDataset(eData)

    return dTest

def predictingSummary(path, modelName, X_test):
    model = joblib.load(path+modelName)
    result = model.predict(X_test)

    return result


def getPredictedSentences(predClass, thread, eData):
    tData = eData.copy()
    pred = pd.DataFrame(predClass, columns=['predicted'])
    tData = pd.concat([tData, pred], axis=1)

    return tData.loc[(tData["predicted"] == 1) & (
                tData["thread_num"] == thread)].iloc[:, [8]]


def sentencePosition(eData):
    # converting received date to datetime
    eData["received"] = pd.to_datetime(eData["received"])

    # ordering the dataframe by thread and date
    eData.sort_values(by=['thread_num', 'received'],
                      ascending=[True, True], inplace=True)

    sentencePosition = []
    threads = eData.loc[:, ["thread_num"]].drop_duplicates().reset_index(
        drop=True)

    # getting sentence position
    for thread in threads["thread_num"]:
        sentenceNumber = len(
            eData.loc[eData["thread_num"] == thread]) + 1
        positions = np.arange(1, sentenceNumber, 1).tolist()
        sentencePosition.extend(positions)

    sp = pd.DataFrame(sentencePosition)
    sp.rename(columns={0: "sentence_position"}, inplace=True)
    eData = pd.concat([eData, sp], axis=1)

    return eData


def wordsInSentence(eData):
    # ToDo remove stop words to reduce noise, also remove weird symbols

    # tokenizing and counting words per sentence
    words_in_sentence = []
    for sentence in eData["sentence_content"]:
        tokens = len(word_tokenize(sentence))
        words_in_sentence.append(tokens)

    wis = pd.DataFrame(words_in_sentence)
    wis.rename(columns={0: "words_in_sentence"}, inplace=True)
    eData = pd.concat([eData, wis], axis=1)

    return eData


def isQuestion(eData):
    # ToDo: Change this pleaseee
    # not fancy but works
    is_question = []
    for sentence in eData["sentence_content"]:
        if sentence.find("?") != -1:
            is_question.append(1)
        else:
            is_question.append(0)

    iq = pd.DataFrame(is_question)
    iq.rename(columns={0: "is_question"}, inplace=True)
    eData = pd.concat([eData, iq], axis=1)

    return eData


def positionMail(eData):
    threadMails = eData.loc[:, ["thread_num", "id", "received"]]. \
        drop_duplicates().reset_index(drop=True)

    threadMails["position_mail"] = threadMails.groupby(["thread_num", "id"]). \
                                       cumcount() + 1

    eData["position_mail"] = 0
    # ToDo: Simplify this assignment,
    # include the received date as condition in the query

    for mailDate in threadMails["received"]:
        position = threadMails.loc[
            threadMails["received"] == mailDate, "position_mail"].values[0]
        eData.loc[eData['received'] == mailDate, "position_mail"] = position

    return eData


def isMoney(eData):
    # regex to evaluate if the word is a number or an amount
    pattern = "^\$?(?=\(.*\)|[^()]*$)\(?\d{1,3}(,?\d{3})?(\.\d\d?)?\)?$"

    is_money = []
    for sentence in eData["sentence_content"]:
        words = sentence.split(" ")
        for w in words:
            result = re.match(pattern, w)
            if result:
                is_money.append(1)
                break
        else:
            is_money.append(0)

    im = pd.DataFrame(is_money, columns=["is_money"])
    eData = pd.concat([eData, im], axis=1)

    return eData

def isDate(eData):
    # regex to evaluate if the word is a date: mm/dd/yy, mm/dd/yyyy, dd/mm/yy, and dd/mm/yyyy
    pattern = "^(?:(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])|(3[01]|[12][0-9]" \
              "|0?[1-9])/(1[0-2]|0?[1-9]))/(?:[0-9]{2})?[0-9]{2}$"
    # months of the year
    months = ["january", "february", "march", "april", "may", "june", "july",
              "august", "september", "october", "november", "december",
                                                            "jan", "feb", "mar",
              "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    # weekdays
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
            "sunday", "mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    is_date = []
    for sentence in eData["sentence_content"]:
        words = sentence.split(" ")
        for w in words:
            resPattern = re.match(pattern, w)
            resMonth = np.isin(w.lower(), months)
            resWeekday = np.isin(w.lower(), days)

            if resPattern or resMonth or resWeekday:
                is_date.append(1)
                break
        else:
            is_date.append(0)

    idate = pd.DataFrame(is_date, columns=['is_date'])
    eData = pd.concat([eData, idate], axis=1)

    return eData


def isInTitle(eData):
    stop_words = set(stopwords.words('english'))

    is_in_title = []
    for index, row in eData.iterrows():
        subjectTokens = word_tokenize(row["subject"].lower())
        filteredSubject = [w for w in subjectTokens if not w in stop_words]
        sentenceTokens = word_tokenize(row["sentence_content"].lower())
        filteredSentence = [w for w in sentenceTokens if not w in stop_words]

        result = np.isin(filteredSentence, filteredSubject)
        fResult = np.isin(True, result)

        if fResult:
            is_in_title.append(1)
        else:
            is_in_title.append(0)

    it = pd.DataFrame(is_in_title, columns=['is_in_title'])
    eData = pd.concat([eData, it], axis=1)

    return eData


def tfidfMail(eData):
    tf_idf_score = tfidf(eData, "mailScore")
    tfScore = pd.DataFrame(tf_idf_score, columns=['tf_idf_score'])
    eData = pd.concat([eData, tfScore], axis=1)

    return eData

def tfidfThread(eData):
    tf_idf_total_score = tfidf(eData, "threadScore")
    tfTotalScore = pd.DataFrame(tf_idf_total_score,
                                columns=['tf_idf_total_score'])
    eData = pd.concat([eData, tfTotalScore], axis=1)

    return eData


def tfidf(data, typeScore):
    threadMails = pd.DataFrame()
    s = pd.DataFrame()

    if typeScore == "mailScore":
        threadMails = data.loc[:, ["thread_num", "id", "received"]].\
            drop_duplicates().reset_index(drop=True)
    elif typeScore == "threadScore":
        threadMails = data.loc[:, ["thread_num"]].drop_duplicates().\
            reset_index(drop=True)

    tf_idf_score = []
    for index, row in threadMails.iterrows():

        if typeScore == "mailScore":
            s = data.loc[(data["received"] == row["received"]) & (
                        data["thread_num"] == row["thread_num"])].iloc[:, [8]]
        elif typeScore == "threadScore":
            s = data.loc[(data["thread_num"] == row["thread_num"])].iloc[:, [8]]

        sentences = s["sentence_content"].tolist()
        normalizedSentences = [s.lower() for s in sentences]
        scoredSentences = scoreSentences(normalizedSentences)
        _, score = zip(*scoredSentences)
        tf_idf_score.extend(score)

    return tf_idf_score

def getFinalDataset(eData):
    dfTest = eData.drop(
        ["id", "name", "received", "from", "to", "subject", "sentence_content"],
        axis=1)

    return dfTest