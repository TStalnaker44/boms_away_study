
from .. import AbstractConverter
from .config import *
import os

class AIConverter(AbstractConverter):

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

            if question == "AI6":
                answer = p["aibom_fields"]["AI6"]
                options = ranked_answers[question.lower()]
            else:
                answer = p["databom_fields"]["D6"]
                options = ranked_answers[question.lower()]

            for i, a in answer.items():
                if i != "other" and a != "":
                    full_answer = options[int(i)-1]
                    
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

            d["B1"] = p["background"]["B1"]
            d["B3"] = p["background"]["B3"]["answer"]

            d["AI1"] = p["aibom_fields"]["AI1"]
            d["AI3"] = p["aibom_fields"]["AI3"]
            d["AI5"] = p["aibom_fields"]["AI5"]["answer"]

            d["D1"] = p["databom_fields"]["D1"]
            d["D2"] = p["databom_fields"]["D2"]["answer"]
            d["D4"] = p["databom_fields"]["D4"]["answer"]

            d["C4"] = p["challenges"]["C4"]
            d["C3"] = p["challenges"]["C3"]["answer"]
            d["C5"] = p["challenges"]["C5"]["answer"]
            d["C6"] = p["challenges"]["C6"]
                    
            d["Q1"] = p["demographics"]["Q1"]
            q2 = p["demographics"]["Q2"]
            d["Q2"] = q2["other"].title() if q2["other"] != "" else q2["answer"]
            q3 = p["demographics"]["Q3"]
            d["Q3"] = q3["other"] if q3["other"] != "" else q3["answer"]
            q5 = p["demographics"]["Q5"]
            d["Q5"] = q5["other"] if q5["other"] != "" else q5["answer"]
            d["Q6"] = p["demographics"]["Q6"]
            d["Q8"] = p["demographics"]["Q8"]
            d["Q9"] = p["demographics"]["Q9"]
            d["Q10"] = p["demographics"]["Q10"]
            
            participants.append(d)

        path = os.path.join(role, "single.csv")
        self.writeToFile(participants, path, shared+single)

    def getMultiAnswer(self, question, data, role):
            
        participants = []
        formats = set()
    
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            qtype = types[question[:-1]]
            answer = p[qtype][question]
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


