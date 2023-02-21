import csvCreator
import preprocess
import weighting
import measure

if __name__ == '__main__':
    cisiALlDict = csvCreator.cisiToCsv("data/CISI.ALL", "data/cisi_all.csv")
    cisiQryDict = csvCreator.cisiToCsv("data/CISI.QRY", "data/cisi_qry.csv")
    cisiRelDict = csvCreator.cisiToCsv("data/CISI.REL", "data/cisi_rel.csv")
    documents, docs_count, postingList, wordfrequencyList = preprocess.normalizer(cisiALlDict, 'data/ppCisiAll.csv')
    queries = preprocess.normalizer(cisiQryDict, 'data/ppCisiQry.csv')
    print("tf=====================================")
    tfDict = weighting.PerformingQuery(queries, "tf", postingList, documents, docs_count)
    measure.measuring(tfDict, queries, cisiRelDict.copy())
    # print("tfIdf========================================")
    # tfIdfDict = weighting.PerformingQuery(queries, "tfidf", postingList, documents, docs_count)
    # print(tfIdfDict)
    # measure.measuring(tfIdfDict, queries, cisiRelDict.copy())

