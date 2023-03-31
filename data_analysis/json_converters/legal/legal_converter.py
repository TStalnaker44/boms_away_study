
from .. import AbstractConverter
from .config import *
import os

class LegalConverter(AbstractConverter):

    def __init__(self, parent, file_name=""):
        AbstractConverter.__init__(self, file_name, parent)
        self.setConfigs()

    def setConfigs(self):
        self._ids = ids
        self._ranked = ranked
        self._multi = multi

    def rankedAnswer(self, question, data, role):
        pass

    def getAllSingleAnswers(self, data, role):
        participants = []
        
        for p in data.values():
            
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            d["D1"] = p["definition"]["D1"]
            d["D2"] = p["definition"]["D2"]
            d["D3"] = p["definition"]["D3"]
            d["D4"] = p["definition"]["D4"]

            d["L1"] = p["legal"]["L1"]
            d["L2"] = p["legal"]["L2"]["answer"]
            d["L3"] = p["legal"]["L3"]
            d["L4"] = p["legal"]["L4"]
            d["L5"] = p["legal"]["L5"]
            d["L6"] = p["legal"]["L6"]
            d["L7"] = p["legal"]["L7"]
            d["L8"] = p["legal"]["L8"]

            d["AI2"] = p["AI"]["AI2"]
            d["AI3"] = p["AI"]["AI3"]

            d["Q1"] = p["demographics"]["Q1"]
            d["Q4"] = p["demographics"]["Q4"]
            
            participants.append(d)

        path = os.path.join(role, "single.csv")
        self.writeToFile(participants, path, shared+single)

    def getMultiAnswer(self, question, data, role):
         pass


