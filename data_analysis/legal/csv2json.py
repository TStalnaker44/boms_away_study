
import csv, json, os, glob


def getDate(survey):
    path = os.path.join(survey, "files", "data_*.csv")
    return glob.glob(path)[-1].split(os.sep)[-1].replace("data_", "").replace(".csv","")

def convertCSV():

    survey = "legal"

    file_date = getDate(survey)

    file_name = os.path.join(survey, "files", f"completers_{file_date}.json")

    def getLabels(temp):
        temp = temp.replace(", ", "||")
        return [t.replace("||", ", ") for t in temp.split(",")]

    d = {}

    path = os.path.join(survey, "files", f"data_{file_date}.csv")
    with open(path, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, row in enumerate(reader):

            if i > 2:

                index = i - 3

                # Meta Data
                meta = {}
                meta["StartDate"] = row[0]
                meta["EndDate"] = row[1]
                meta["Status"] = row[2]
                meta["IPAddress"] = row[3]
                meta["Progress"] = row[4]
                if int(row[4]) != 100:
                    continue
                meta["Duration"] = row[5]
                meta["Finished"] = row[6]
                meta["RecordedDate"] = row[7]
                meta["ResponseID"] = row[8]
                meta["LocationLatitude"] = row[13]
                meta["LocationLongitude"] = row[14]
                meta["UserLanguage"] = row[16]
                d[index] = {"meta":meta}

                # Consent Form
                d[index]["consent"] = {"CF2":row[17]}

                # Definition
                definition = {}
                definition["D1"] = row[18]
                definition["D2"] = row[19]
                definition["D3"] = row[20]
                definition["D4"] = row[21]
                d[index]["definition"] = definition

                # Legal
                legal = {}
                legal["L1"] = row[22]
                legal["L2"] = {"answer":row[23], "list":row[24]}
                legal["L3"] = row[25]
                legal["L4"] = row[26]
                legal["L5"] = row[27]
                legal["L6"] = row[28]
                legal["L7"] = row[29]
                legal["L8"] = row[30]
                d[index]["legal"] = legal

                # AI
                ai = {}
                ai["AI2"] = row[31]
                ai["AI3"] = row[32]
                d[index]["AI"] = ai

                # Demographics
                demo = {}
                demo["Q1"] = row[33]
                demo["Q2"] = row[34]
                demo["Q3"] = row[35]
                demo["Q4"] = row[36]
                d[index]["demographics"] = demo

    with open(file_name, "w") as file:
        json.dump(d, file)
