import nltk
import sklearn


# ToDo: Add more features like order in the sentence, question mark, when words.
# ToDo: Add LSA functionality


# scoring sentences
def scoreSentences(sentences):
    scores = []

    # define the vectorizer function
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(
        max_features=1024, stop_words='english')
    # encode sentences
    # output (sentence number, word index in vocabulary)
    # and word score in the whole vocabulary
    X = vectorizer.fit_transform(sentences)

    # NEXT --- scoring the sentence:
    # according the score, decide whether include it in the
    # final summary or not

    # ----------- Approaches ------------ #
    # formula 1:
    # sentence score = total terms values in the sentence
    # / total of terms in the sentence

    # formula 2:
    # sentence score = total terms values in the sentence
    # / total of words in the sentence

    # formula 3:
    # sentence score = total terms values in the sentence

    # formula 4:
    # sentence score = total terms values in the sentence
    # / total of terms in the text

    for idx, v in enumerate(X):
        # print("Sentence number: ", idx)
        # print(v)

        totalTermSentenceValue = v.sum(axis=None)
        # print("Total sentence term value: ", totalTermSentenceValue)
        termSentenceLength = v.getnnz()
        # print("Number terms in the sentence: ", termSentenceLength)

        # formula 1:
        # sentenceScore = totalTermSentenceValue / termSentenceLength

        #formula 2:
        #numWordsPerSentence = len(sentences[idx])
        # sentenceScore = totalTermSentenceValue / numWordsPerSentence

        # formula 3:
        # sentenceScore = totalTermSentenceValue

        # formula 4:
        sentenceScore = totalTermSentenceValue / X.sum(axis=None)

        # print("Sentence score: ", sentenceScore)
        # print("\n")

        scores.append((idx, round(sentenceScore,2)))

    return scores

def getTextSummary(txt):
    # get the sentences in the txt
    sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
    # normalizing sentences to lowercase
    normalizedSentences = [s.lower() for s in sentences]

    scoredSentences = scoreSentences(normalizedSentences)

    #
    #     # Summarization Approach 1:
    #     # Filter out nonsignificant sentences by using the average score plus a
    #     # fraction of the std dev as a filter
    #
    #     avg = np.mean([s[1] for s in scored_sentences])
    #     std = np.std([s[1] for s in scored_sentences])
    #     mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences
    #                    if score > avg + 0.5 * std]
    #
    #     # Summarization Approach 2:
    #     # Another approach would be to return only the top N ranked sentences
    #
    n = 5

    topSentences = sorted(scoredSentences, reverse=True, key=lambda s: s[1])[:n]
    topSentences = sorted(topSentences, key=lambda s: s[0])
    summary = [sentences[idx] for idx, score in topSentences]

    return {"summary": summary}
