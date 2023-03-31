
from .. import AbstractConverter
from .config import *
import os

class CyberConverter(AbstractConverter):

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
              
            answer = eval("p" + types[question[:-1]])[question]

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

            "SB1", "HB1", "HB2", "L1", "L2", "L3", "L4", "L5", "L6"
            
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            d["SB1"] = p["background"]["sbom"]["SB1"]
            d["HB1"] = p["background"]["hbom"]["HB1"]
            d["HB2"] = p["background"]["hbom"]["HB2"]

            d["L1"] = p["likert"]["L1"]
            d["L2"] = p["likert"]["L2"]
            d["L3"] = p["likert"]["L3"]
            d["L4"] = p["likert"]["L4"]
            d["L5"] = p["likert"]["L5"]
            d["L6"] = p["likert"]["L6"]
         
            d["Q1"] = p["demographics"]["Q1"]
            d["Q2"] = p["demographics"]["Q2"]
            q3 = p["demographics"]["Q3"]
            d["Q3"] = q3["other"] if q3["other"] != "" else q3["answer"]
            d["Q8"] = p["demographics"]["Q8"]
            d["Q9"] = p["demographics"]["Q9"]
            d["Q10"] = p["demographics"]["Q10"]
            
            participants.append(d)

        path = os.path.join(role, "single.csv")
        self.writeToFile(participants, path, shared+single)