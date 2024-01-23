

import csv, json, os, glob

class CSVConverter():

    def __init__(self, surveyFolder):
        self._base_path     = os.path.join(surveyFolder, "files")
        self._survey_folder = surveyFolder
        self._questions     = self.getQuestions()
        self._metafields    = self.getMetaFields()
        self._file_date     = self.getDate()
        self._d = {}

    def getQuestions(self):
        path = os.path.join(self._survey_folder, "questions.json")
        with open(path) as file:
            return json.load(file)

    def getMetaFields(self):
        path = os.path.join(self._survey_folder, "metafields.json")
        with open(path) as file:
            return json.load(file)
        
    def extractMetaData(self, row):
        meta = {}
        for field, index in self._metafields.items():
            meta[field] = row[index]
        return meta
    
    def extractSectionData(self, row, index, column):
        for label, qs in self._questions.items():
            sec = {}
            for qid, qdata in qs.items():
                qtype = qdata["type"]
                if qtype in ("single-select", "single-text", "likert", "short-answer", "email", "multi-select"):
                    sec[qid] = row[column]
                    column += 1
                elif qtype == "single-select-with-other":
                    sec[qid] = {"answers":row[column], "other":row[column+1]}
                    column += 2
                elif qtype == "multi-select-with-other":
                    sec[qid] = {"answers":self.getLabels(row[column]), "other":row[column+1]}
                    column += 2
                elif qtype == "ranked":
                    options = qdata.get("options", None)
                    if options == None: raise ValueError("Questions of type 'ranked' require 'options' field")
                    sec[qid] = {i+1:row[column+i] for i in range(len(options))}
                    column += len(options)
                elif qtype == "ranked-with-other":
                    options = qdata.get("options", None)
                    if options == None: raise ValueError("Questions of type 'ranked-with-other' require 'options' field")
                    sec[qid] = {i+1:row[column+i] for i in range(len(options))}
                    sec[qid]["other"] = row[column+len(options)]
                    column += len(options) + 1
                else:
                    raise ValueError(f"Unknown qtype: {qtype}")
            self._d[index][label] = sec
        return column
    
    def getDate(self):
        path = os.path.join(self._base_path, "data_*.csv")
        return glob.glob(path)[-1].split(os.sep)[-1].replace("data_", "").replace(".csv","")
    
    def writeJSON(self):
        survey_name = self._survey_folder.split(os.sep)[1]
        file_name = os.path.join(self._base_path, f"{survey_name}_completers_{self._file_date}.json")
        with open(file_name, "w") as file:
            json.dump(self._d, file)

    def getLabels(self, temp):
        temp = temp.replace(", ", "||")
        return [t.replace("||", ", ") for t in temp.split(",")]
    
    def processRow(self, index, row):
        self._d[index] = {"meta":self.extractMetaData(row)}
        self._d[index]["consent"] = {"CF2":row[17]}
        column = self.extractSectionData(row, index, 18)
        # self._d[index]["contact_information"] = row[column]

    def convertCSV(self):
        path = os.path.join(self._base_path, f"data_{self._file_date}.csv")
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                not_header = i > 2
                if not_header:
                    index = i - 3 # Start indexing at 0
                    incomplete = int(row[4]) != 100
                    if not incomplete:
                        self.processRow(index, row)
        self.writeJSON()

                    


