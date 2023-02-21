beta = 0.2


def measuring(scoreDict, queries, rels):
    sortedDict = sortOrderOfKeysAndBests(scoreDict, queries)
    fp, tp, fn = calculateTpFpFn(sortedDict, rels)
    precision = getPrecision(tp, fp)
    recall = getRecall(tp, fn)
    f_measure = getF_measure(precision, recall)
    print("fp-> " + str(fp) + ", tp->" + str(tp) + ", fn->" + str(fn))
    print("precision-> " + str(precision) + ", recall->" + str(recall) + ", f_measure->" + str(f_measure))


def sortOrderOfKeysAndBests(scoreDict, queries):
    bests = {}
    for queryNumber in queries:
        queryToDocsRels = {}
        queryToDocsRelsKeys = [item for item in scoreDict if item[0] == queryNumber]
        for address in queryToDocsRelsKeys:
            queryToDocsRels[address] = scoreDict[address]
        sortedQueryToDocsRels = dict(sorted(queryToDocsRels.items(), reverse=True, key=lambda item: item[1]))
        for index in range(20):
            keys = list(sortedQueryToDocsRels.keys())
            values = list(sortedQueryToDocsRels.values())
            bests[keys[index]] = values[index]
    return bests


def calculateTpFpFn(sortedDict, relations):
    fp, tp, fn = 0, 0, 0
    queryNumber = 0
    for query_doc in sortedDict:
        queryID, docID = query_doc
        if str(queryID) not in relations:
            continue
        if queryNumber != str(queryID):
            if queryNumber != 0:
                fn += len(relations[queryNumber])
            queryNumber = str(queryID)
        listOfCisiRel = relations[str(queryID)]
        if str(docID) in listOfCisiRel:
            tp += 1
            relations[str(queryID)].remove(str(docID))
        elif str(docID) not in listOfCisiRel:
            fp += 1
    return fp, tp, fn


def getPrecision(tp, fp):
    return tp / (tp + fp)


def getRecall(tp, fn):
    return tp / (tp + fn)


def getF_measure(precision, recall):
    return (((beta**2)+1)*precision*recall)/(((beta**2)*precision)+recall)
