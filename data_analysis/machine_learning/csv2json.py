
import csv, json, os, glob


def getDate(survey):
    path = os.path.join(survey, "files", "data_*.csv")
    return glob.glob(path)[-1].split(os.sep)[-1].replace("data_", "").replace(".csv","")

def convertCSV():

    survey = "machine_learning"

    file_date = getDate(survey)

    file_name = os.path.join(survey, "files", f"ai_completers_{file_date}.json")

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

                # Background
                background = {}
                background["B1"] = row[18]
                background["B2"] = {"answers":getLabels(row[19]), "other":row[20]}
                background["B3"] = {"answer":row[21], "list":row[22]}
                d[index]["background"] = background

                # AIBOM Fields
                aibom = {}
                aibom["AI1"] = row[23]
                aibom["AI2"] = {"answers":getLabels(row[24]), "other":row[25]}
                aibom["AI3"] = row[26]
                aibom["AI4"] = row[27]
                aibom["AI5"] = {"answer":row[28], "list":row[29]}
                aibom["AI6"] = {
                    1: row[30],
                    2: row[31],
                    3: row[32],
                    4: row[33],
                    5: row[34],
                    6: row[35],
                    "other": row[36]
                    }
                aibom["AI7"] = row[37]
                d[index]["aibom_fields"] = aibom

                # DataBOM Fields
                databom = {}
                databom["D1"] = row[38]
                databom["D2"] = {"answer":row[39], "list":row[40]}
                databom["D3"] = {"answers":getLabels(row[41]), "other":row[42]}
                databom["D4"] = {"answer":row[43], "list":row[44]}
                databom["D5"] = row[45]
                databom["D6"] = {
                    1: row[46],
                    2: row[47],
                    3: row[48],
                    4: row[49],
                    5: row[50],
                    "other": row[51]
                    }
                databom["D7"] = row[52]
                databom["D8"] = row[53]
                databom["D9"] = row[54]
                d[index]["databom_fields"] = databom

                # Challenges
                challenges = {}
                challenges["C1"] = row[55]
                challenges["C2"] = row[56]
                challenges["C3"] = {"answer":row[57], "list":row[58]}
                challenges["C4"] = row[59]
                challenges["C5"] = {"answer":row[60], "list":row[61]}
                challenges["C6"] = row[62]
                challenges["C7"] = row[63]
                d[index]["challenges"] = challenges

                # Demographics
                demo = {}
                demo["Q1"] = row[64]
                demo["Q2"] = {"answer":row[65], "other":row[66]}
                demo["Q3"] = {"answer":row[67], "other":row[68]}
                demo["Q4"] = {"answers":getLabels(row[69]), "other":row[70]}
                demo["Q5"] = {"answer":row[71], "other":row[72]}
                demo["Q6"] = row[73]
                demo["Q7"] = row[74]
                demo["Q8"] = row[75]
                demo["Q9"] = row[76]
                demo["Q10"] = row[77]
                demo["Q11"] = row[78]
                demo["Q12"] = row[79]
                d[index]["demographics"] = demo

    with open(file_name, "w") as file:
        json.dump(d, file)
