import csv
import re


def cisiToCsv(address, destination):
    createDict = {}
    if destination == "data/cisi_rel.csv":
        return relToCsv(address, destination)
    with open(address) as file:
        with open(destination, "w", newline='') as cisiAll:
            row = 0
            csvwriter = csv.writer(cisiAll)
            firstRow = ["I", "W"]
            csvwriter.writerow(firstRow)
            inpt = ""
            arr = []
            print("splitting....")
            writeI = False
            writeW = False
            for line in file:
                if str(line)[:2] == ".I":
                    writeI = True
                elif str(line)[:2] == ".W":
                    inpt = ""
                    writeI = False
                    writeW = True
                    continue
                elif address == "data/CISI.QRY" and str(line)[:2] == ".B":
                    writeW = False
                    arr.append(inpt)
                if (address == "data/CISI.ALL" and str(line)[:2] == ".X") or (address == "data/CISI.QRY" and writeI):
                    if row != 0:
                        writeW = False
                        if len(arr) == 1:
                            arr.append(inpt)
                        createDict[arr[0]] = arr[1]
                        csvwriter.writerow(arr)
                        arr.clear()

                if writeI:
                    row += 1
                    arr.append(row)
                    writeI = False
                elif writeW:
                    inpt += str(line)
            if address == "data/CISI.QRY":
                csvwriter.writerow(arr)
    return createDict


def relToCsv(address, destination):
    rels = {}
    with open(address) as file:
        with open(destination, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            firstRow = ["query", "doc"]
            csvwriter.writerow(firstRow)
            for line in file:
                cells = re.sub(r"\s+", " ", str(line)).split(" ")
                csvwriter.writerow([cells[1], cells[2]])
                if cells[1] not in rels.keys():
                    rels[cells[1]] = [cells[2]]
                else:
                    rels[cells[1]].append(cells[2])
    return rels
