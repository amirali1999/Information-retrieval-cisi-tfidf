import re
import nltk
import csv
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def normalizer(fileDict, destination,
               lowerCaseFlag=True,
               removingNumbersFlag=True,
               removingPunctuationFlag=True,
               removingWhiteSpaceFlag=True,
               removingStopWordsFlag=True,
               stemmingFlag=True,
               lemmatizationFlag=False):
    with open(destination, 'w', newline='') as csvOutPut:
        postingList = {}
        wordfrequencyList = {}
        rowNumber = 1
        field_names = ["I", "result"]
        writer = csv.writer(csvOutPut)
        writer.writerow(field_names)
        for doc in fileDict.keys():
            if lowerCaseFlag:
                fileDict[doc] = convertToLowerCase(fileDict[doc])

            if removingNumbersFlag:
                fileDict[doc] = deleteNumbers(fileDict[doc])

            if removingPunctuationFlag:
                fileDict[doc] = deletePunctuation(fileDict[doc])

            if removingWhiteSpaceFlag:
                fileDict[doc] = deleteWhiteSpace(fileDict[doc])

            if removingStopWordsFlag:
                fileDict[doc] = deleteStopWords(fileDict[doc])

            words = word_tokenize(fileDict[doc])
            countOfWords = 0
            for word in words:
                if lemmatizationFlag:
                    word = lemmatization(word)
                if stemmingFlag:
                    word = stemming(word)
                words[countOfWords] = word
                countOfWords += 1
                postingList = updatePostingList(postingList, word, rowNumber)
                wordfrequencyList = updateWordfrequencyList(wordfrequencyList, word)
            rowNumber += 1
            fileDict[doc] = "/".join(words)
            writer.writerow([doc, fileDict[doc]])
    # print(fileDict)
    if destination == 'data/ppCisiQry.csv':
        return fileDict
    return fileDict, rowNumber, postingList, wordfrequencyList


def convertToLowerCase(row):
    return row.lower()


def deleteNumbers(row):
    return re.sub(r'\d+', '', row)


def deletePunctuation(row):
    return re.sub(r'[^\w\s]', '', row)


def deleteWhiteSpace(row):
    return row.strip()


def deleteStopWords(row):
    stopWords = set(stopwords.words('english'))
    words = [row][0].split()
    sentence = ""
    for i in words:
        if not i in stopWords:
            sentence += i + ' '
    return sentence[:-1]


def updatePostingList(posting_list, word, rowNumber):
    if word in posting_list.keys():
        if rowNumber not in posting_list[word]:
            posting_list[word].append(rowNumber)
    else:
        posting_list[word] = [rowNumber]
    return posting_list


def updateWordfrequencyList(frequency_List, word):
    if word in frequency_List.keys():
        frequency_List[word] += 1
    else:
        frequency_List[word] = 1
    return frequency_List


def stemming(word):
    return PorterStemmer().stem(word)


def lemmatization(word):
    return WordNetLemmatizer().lemmatize(word)
