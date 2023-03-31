
import csv, json, os, glob

def getDate(survey):
    path = os.path.join(survey, "files", "data_*.csv")
    return glob.glob(path)[-1].split(os.sep)[-1].replace("data_", "").replace(".csv","")

def convertCSV():

    survey = "cyber_physical"

    file_date = getDate(survey)

    file_name = os.path.join(survey, "files", f"cyber_completers_{file_date}.json")

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

                # General
                general = {}
                general["G1"] = row[18]
                general["G2"] = row[19]
                d[index]["general"] = general

                # Background
                background = {}
                
                sbom = {}
                sbom["SB1"]  = row[20]

                hbom = {}
                hbom["HB1"] = row[21]
                hbom["HB2"] = row[22]
                hbom["HB3"] = {"answers":getLabels(row[23]), "other":row[24]}
                
                background["sbom"] = sbom
                background["hbom"] = hbom
                d[index]["background"] = background

                # Likert
                likert = {}
                likert["L1"] = row[25]
                likert["L2"] = row[26]
                likert["L3"] = row[27]
                likert["L4"] = row[28]
                likert["L5"] = row[29]
                likert["L6"] = row[30]
                d[index]["likert"] = likert

                # Open
                open_q = {}
                open_q["O1"] = row[31]
                open_q["O2"] = row[32]
                open_q["O3"] = row[33]
                open_q["O4"] = {
                    1: row[34],
                    2: row[35],
                    3: row[36],
                    4: row[37],
                    5: row[38],
                    6: row[39],
                    "other": row[40]
                    }
                open_q["O5"] = row[41]
                d[index]["open"] = open_q

                # Demographics
                demo = {}
                demo["Q1"] = row[42]
                demo["Q2"] = row[43]
                demo["Q3"] = {"answer":row[44], "other":row[45]}
                demo["Q4"] = {"answers":getLabels(row[46]), "other":row[47]}
                demo["Q5"] = row[48]
                demo["Q7"] = row[49]
                demo["Q8"] = row[50]
                demo["Q9"] = row[51]
                demo["Q10"] = row[52]
                demo["Q11"] = row[53]
                demo["Q12"] = row[54]
                d[index]["demographics"] = demo

    with open(file_name, "w") as file:
        json.dump(d, file)
