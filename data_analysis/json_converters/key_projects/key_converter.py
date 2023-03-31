
from .. import AbstractConverter
from .config import *
import os

class KeyConverter(AbstractConverter):

    def __init__(self, parent, file_name=""):
        AbstractConverter.__init__(self, file_name, parent)
        self.setConfigs()

    def setConfigs(self):
        self._ids = ids
        self._ranked = ranked
        self._multi = multi

    def rankedAnswer(self, question, data, role):

        participants = []
        formats = set()
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]            
            answer = p["familiar"]["consumers"][question]

            for i, a in answer.items():
                if i != "other" and a != "":
                    full_answer = ranked_answers[question.lower()][int(i)-1]
                    
                    d[full_answer] = a
                    formats.add(full_answer)

            participants.append(d)

        path = os.path.join(role, "rank", question + ".csv")
        self.writeToFile(participants, path, shared+list(formats))

    def getMultiAnswer(self, question, data, role):

        participants = []
        formats = set()
        
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            if question == "ID":
                answer = p["self_identification"]
                keyword = "ID"  
            else:
                qtype = question[:-1]
                answer = eval("p" + types[qtype])[question]
                keyword = "answers"

            if answer[keyword] == [""]:
                d["No Answer"] = 1
                formats.add("No Answer")
            else:
                for a in answer[keyword]:
                    d[a] = 1
                    formats.add(a)
                if answer["other"] != "":
                    d[answer["other"]] = 1
                    formats.add(answer["other"])

            participants.append(d)

        path = os.path.join(role, "multi_select", f"{question}.csv")
        self.writeToFile(participants, path, shared+list(formats))


    def getAllSingleAnswers(self, data, role):

        participants = []
        
        for p in data.values():
            
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            d["S1"] = p["shared"]["S1"]
            d["S2"] = p["shared"]["S2"]
            d["S3"] = p["shared"]["S3"]

            d["FS2"] = p["familiar"]["shared"]["FS2"]
            d["FS3"] = p["familiar"]["shared"]["FS3"]
            d["FS6"] = p["familiar"]["shared"]["FS6"]
            d["FS9"] = p["familiar"]["shared"]["FS9"]

            d["P1"] = p["familiar"]["producers"]["shared"]["P1"]
            d["P6"] = p["familiar"]["producers"]["shared"]["P6"]

            d["IP1"] = p["familiar"]["producers"]["internal"]["IP1"]

            c3 = p["familiar"]["consumers"]["C3"]
            d["C3"] = c3["other"] if c3["other"] != "" else c3["answer"]
            d["C4"] = p["familiar"]["consumers"]["C4"]

            d["FN2"] = p["familiar"]["non_users"]["FN2"]

            d["O1"] = p["oboms"]["O1"]
            d["O2"] = p["oboms"]["O2"]
                    
            d["Q1"] = p["demographics"]["Q1"]
            q2 = p["demographics"]["Q2"]
            d["Q2"] = q2["other"] if q2["other"] != "" else q2["answer"]
            q3 = p["demographics"]["Q3"]
            d["Q3"] = q3["other"] if q3["other"] != "" else q3["answer"]
            d["Q6"] = p["demographics"]["Q6"]
            d["Q8"] = p["demographics"]["Q8"]
            d["Q9"] = p["demographics"]["Q9"]
            d["Q10"] = p["demographics"]["Q10"]
            
            participants.append(d)

        path = os.path.join(role, "single.csv")
        self.writeToFile(participants, path, shared+single)