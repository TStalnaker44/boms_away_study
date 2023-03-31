
import csv, json, os, glob

def getDate(survey):
    path = os.path.join(survey, "files", "data_*.csv")
    return glob.glob(path)[-1].split(os.sep)[-1].replace("data_", "").replace(".csv","")

def convertCSV():

    survey = "key_projects"

    file_date = getDate(survey)

    file_name = os.path.join(survey, "files", f"key_completers_{file_date}.json")

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

                # Self Identification
                ident = {}
                ident["ID"] = getLabels(row[18])
                ident["other"] = row[19]
                d[index]["self_identification"] = ident

                # Shared
                shared = {}
                shared["S1"]  = row[20]
                shared["S2"]  = row[21]
                shared["S3"]  = row[22]
                shared["S4"]  = row[23]            
                shared["S5"]  = row[24]
                d[index]["shared"] = shared

                # Familiar
                familiar = {}

                ## Shared
                shared = {}
                shared["FS1"] = {"answers":getLabels(row[25]), "other":row[26]}
                shared["FS2"] = row[27]
                shared["FS3"] = row[28]
                shared["FS4"] = {"answers":getLabels(row[29]), "other":row[30]}
                shared["FS5"] = row[31]
                shared["FS6"] = row[32]
                shared["FS7"] = row[33]
                shared["FS8"] = {"answers":getLabels(row[34]), "other":row[35]}
                shared["FS9"] = row[36]
                shared["FS10"] = row[37]
                familiar["shared"] = shared

                ## Producers
                producers = {}

                ### Shared
                shared = {}
                shared["P1"] = row[40]
                shared["P2"] = {"answers":getLabels(row[41]), "other":row[42]}
                shared["P3"] = {"answers":getLabels(row[43]), "other":row[44]}
                shared["P4"] = {"answers":getLabels(row[45]), "other":row[46]}
                shared["P5"] = row[47]
                shared["P6"] = row[48]
                shared["P7"] = row[49]
                shared["P8"] = {"answers":getLabels(row[50]), "other":row[51]}

                ### Internal
                internal = {}
                internal["IP1"] = row[52]
                internal["IP2"] = row[53]

                ### External
                external = {}
                external["EP1"] = {"answers":getLabels(row[54]), "other":row[55]}

                producers["shared"] = shared
                producers["internal"] = internal
                producers["external"] = external
                familiar["producers"] = producers

                ## Consumers
                consumers = {}
                consumers["C1"] = {"answers":getLabels(row[56]), "other":row[57]}
                consumers["C2"] = {"answers":getLabels(row[58]), "other":row[59]}
                consumers["C3"] = {"answer":row[60], "other":row[61]}
                consumers["C4"] = row[62]
                consumers["C5"] = row[63]
                consumers["C6"] = {"answers":getLabels(row[64]), "other":row[65]}
                consumers["C7"] = {
                    1: row[66],
                    2: row[67],
                    3: row[68],
                    4: row[69],
                    5: row[70],
                    6: row[71],
                    "other": row[72]
                    }
                familiar["consumers"] = consumers

                ## Non-User
                nonusers = {}
                nonusers["FN1"] = {"answers":getLabels(row[73]), "other":row[74]}
                nonusers["FN2"] = row[75]
                nonusers["FN3"] = row[76]
                familiar["non_users"] = nonusers

                d[index]["familiar"] = familiar
                
                # Non-User
                nonusers = {}
                nonusers["NU1"] = row[38]
                nonusers["NU2"] = row[39]
                d[index]["non_users"] = nonusers

                # OBOMs
                oboms = {}
                oboms["O1"] = row[77]
                oboms["O2"] = row[78]
                oboms["O3"] = row[79]
                oboms["O4"] = row[80]
                d[index]["oboms"] = oboms

                # Demographics
                demo = {}
                demo["Q1"] = row[81]
                demo["Q2"] = {"answer":row[82], "other":row[83]}
                demo["Q3"] = {"answer":row[84], "other":row[85]}
                demo["Q4"] = {"answers":getLabels(row[86]), "other":row[87]}
                demo["Q5"] = {"answers":getLabels(row[88]), "other":row[89]}
                demo["Q7"] = row[90]
                demo["Q6"] = row[91]
                demo["Q8"] = row[92]
                demo["Q9"] = row[93]
                demo["Q10"] = row[94]
                demo["Q11"] = row[95]
                demo["Q12"] = row[96]
                d[index]["demographics"] = demo

    with open(file_name, "w") as file:
        json.dump(d, file)
