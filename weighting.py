import math


def PerformingQuery(queries, method, postingList, documents, docs_count):
    if method == "tf":
        return queriesTf(queries, postingList, documents)
    else:
        return queriesTfIdf(queries, postingList, documents, docs_count)


def queriesTf(queries, postingList, documents):
    tf_dict = {}
    tf_all = getTf(postingList, documents)
    for queryValue, queryKey in zip(queries.values(), queries.keys()):
        for word in [word for word in queryValue.split("/") if word in postingList]:
            for tf_result in tf_all[word]:
                docID, tf = tf_result
                if (queryKey, docID) in tf_dict.keys():
                    tf_dict[(queryKey, docID)] += tf
                else:
                    tf_dict[(queryKey, docID)] = tf
    return tf_dict


def queriesTfIdf(queries, postingList, documents, docs_count):
    tfIdf_dict = {}
    tfIdf = tf_idf(postingList, documents, docs_count)
    for queryValue, queryKey in zip(queries.values(), queries.keys()):
        for word in [word for word in queryValue.split("/") if word in postingList]:
            docs = postingList[word]
            for doc in docs:
                tfIdfWordOfQueryInDoc = tfIdf[(doc, word)]
                if (queryKey, doc) in tfIdf_dict:
                    tfIdf_dict[(queryKey, doc)] += tfIdfWordOfQueryInDoc
                else:
                    tfIdf_dict[(queryKey, doc)] = tfIdfWordOfQueryInDoc
    return tfIdf_dict


def tf_idf(postingList, documents, docs_count):
    tf_idf_all = {}
    tf_all = getTf(postingList, documents)
    idf_all = getIdf(postingList, docs_count)
    for word in postingList:
        tfs = tf_all[word]
        for tf_result in tfs:
            docID, tf = tf_result
            tf_idf_all[docID, word] = idf_all[word] * tf[docID]
    return tf_idf_all


def getTf(postingList, documents):
    tf_all = {}
    for word in postingList:
        for doc in postingList[word]:
            word_frequently = documents[doc].split("/").count(word)
            if word_frequently != 0:
                tf = 1 + math.log(word_frequently, 10)
            else:
                tf = 0
            tf_all.setdefault(word, [])
            tf_all[word].append((doc, tf))
    return tf_all


def getIdf(postingList, docs_count):
    idf_all = {}
    for word in postingList:
        doc_frequency = len(postingList[word])
        idf = math.log((docs_count / doc_frequency), 10)
        idf_all[word] = idf
    return idf_all
