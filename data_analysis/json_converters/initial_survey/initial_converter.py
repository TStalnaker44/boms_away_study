
from .. import AbstractConverter
from .config import *
import os

class InitialConverter(AbstractConverter):

    def __init__(self, parent, file_name=""):
        AbstractConverter.__init__(self, file_name, parent)
        self.setConfigs()

    def setConfigs(self):
        self._ids = ids
        self._ranked = ranked
        self._multi = multi

    def rankedAnswer(self, question, data, role):

        qtype = question[:-1]

        participants = []
        formats = set()
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]
            
            answer = p[types[qtype]][question]

            for i, a in answer.items():
                if i != "other" and a != "":
                    full_answer = ranked_answers[question.lower()][int(i)-1]                    
                    d[full_answer] = a
                    formats.add(full_answer)

            participants.append(d)

    
        path = os.path.join(role, "rank", question + ".csv")
        self.writeToFile(participants, path, shared+list(formats))

    def getAllSingleAnswers(self, data, role):
        participants = []
        
        for p in data.values():
            
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            d["S4"] = p["shared"]["S4"]
            d["S7"] = p["shared"]["S7"]
            d["P7"] = p["producers"]["P7"]
            
            c4 = p["consumers"]["C4"]
            d["C4"] = c4["other"] if c4["other"] != "" else c4["answer"]
            
            d["C5"] = p["consumers"]["C5"]
            d["T5"] = p["developers"]["T5"]
            d["E2"] = p["educators"]["E2"]
            d["E3"] = p["educators"]["E3"]

            d["SC1"] = p["security"]["SC1"]
            d["SC2"] = p["security"]["SC2"]
            d["SC3"] = p["security"]["SC3"]
            d["SC4"] = p["security"]["SC4"]
            d["SC5"] = p["security"]["SC5"]
            d["SC6"] = p["security"]["SC6"]

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

    def getMultiAnswer(self, question, data, role):

        qtype = question[:-1]
        
        keyword = "formats" if qtype == "S" else "answers"
        participants = []
        formats = set()
        for p in data.values():
            
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            answer = p[types[qtype]][question]

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


