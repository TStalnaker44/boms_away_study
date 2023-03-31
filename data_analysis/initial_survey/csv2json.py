
import csv, json, os, glob

def getDate(survey):
    path = os.path.join(survey, "files", "data_*.csv")
    return glob.glob(path)[-1].split(os.sep)[-1].replace("data_", "").replace(".csv","")

def convertCSV():

    survey = "initial_survey"

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
                if index >= 203: index += 1

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

                # Self Identification
                ident = {}
                ident["ID"] = getLabels(row[18])
                ident["other"] = row[19]
                d[index]["self_identification"] = ident

                # Shared
                shared = {}
                shared["S1"]  = row[20]
                shared["S2"]  = {"formats":getLabels(row[21]), "other":row[22]}
                shared["S3"]  = row[23]
                shared["S4"]  = row[24]
                shared["S5"]  = row[25]
                shared["S6"]  = row[26]
                shared["S7"]  = row[27]
                shared["S8"]  = row[28]
                shared["S9"] = {
                    1: row[29],
                    2: row[30],
                    3: row[31],
                    4: row[32],
                    5: row[33],
                    6: row[34],
                    "other": row[35]
                    }
                shared["S10"] = row[36]
                d[index]["shared"] = shared

                # Producers
                producers = {}
                producers["P2"] = {"answers":getLabels(row[37]), "other":row[38]}
                producers["P3"] = {"answers":getLabels(row[39]), "other":row[40]}
                producers["P4"] = row[41]
                producers["P5"] = row[42]
                producers["P7"] = row[43]
                producers["P8"] = row[44]
                producers["P9"] = row[45]
                d[index]["producers"] = producers

                # Consumers
                consumers = {}
                consumers["C2"] = {"answers":getLabels(row[46]), "other":row[47]}
                consumers["C3"] = row[48]
                consumers["C4"] = {"answer":row[49], "other":row[50]}
                consumers["C5"] = row[51]
                consumers["C6"] = row[52]
                consumers["C7"] = row[53]
                d[index]["consumers"] = consumers

                # Tool Developers
                devs = {}
                devs["T2"] = {"answers":getLabels(row[54]), "other":row[55]}
                devs["T3"] = {"answers":getLabels(row[56]), "other":row[57]}
                devs["T4"] = {"answers":getLabels(row[58]), "other":row[59]}
                devs["T5"] = row[60]
                devs["T6"] = row[61]
                d[index]["developers"] = devs

                # Standard Makers
                stan = {}
                stan["SM2"] = {"answers":getLabels(row[62]), "other":row[63]}
                stan["SM3"] = row[64]
                d[index]["standard_makers"] = stan

                # Educators
                ed = {}
                ed["E2"] = row[65]
                ed["E3"] = row[66]
                ed["E4"] = {"answers":getLabels(row[67]), "other":row[68]}
                ed["E5"] = {
                    1: row[69],
                    2: row[70],
                    3: row[71],
                    4: row[72],
                    5: row[73],
                    6: row[74],
                    7: row[75],
                    "other": row[76]
                    }
                d[index]["educators"] = ed

                # Security
                sec = {}
                sec["SC1"] = row[77]
                sec["SC2"] = row[78]
                sec["SC3"] = row[79]
                sec["SC4"] = row[80]
                sec["SC5"] = row[81]
                sec["SC6"] = row[82]
                sec["SC7"] = row[83]
                sec["SC8"] = row[84]
                sec["SC9"] = row[85]
                d[index]["security"] = sec

                # Demographics
                demo = {}
                demo["Q1"] = row[86]
                demo["Q2"] = {"answer":row[87], "other":row[88]}
                demo["Q3"] = {"answer":row[89], "other":row[90]}
                demo["Q4"] = {"answers":getLabels(row[91]), "other":row[92]}
                demo["Q5"] = {"answers":getLabels(row[93]), "other":row[94]}
                demo["Q7"] = row[95]
                demo["Q6"] = row[96]
                demo["Q8"] = row[97]
                demo["Q9"] = row[98]
                demo["Q10"] = row[99]
                demo["Q11"] = row[100]
                demo["Q12"] = row[101]
                d[index]["demographics"] = demo

    with open(file_name, "w") as file:
        json.dump(d, file)
