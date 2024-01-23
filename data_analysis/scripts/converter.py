
import os, json, itertools, copy, csv
from .config import Config

class Converter():

    def __init__(self, survey_folder, file_name):
        self._file_name = file_name
        self._survey_folder = survey_folder
        self.config = Config(survey_folder)
        self.setConfigs()

    def setConfigs(self):
        self._ids = self.config.ids
        self._ranked = self.config.ranked
        self._multi = self.config.multi
        self._single = self.config.single
    
    def filterByRole(self, data, targets, strict=False):
        targets = [self._ids[t] for t in targets] #normalize targets to short form
        pids = list(data.keys())
        for pid in pids:
            group, question = self.config.id_path
            roles = data[pid][group][question]["answers"]
            if strict:
                matches = set(targets) == set(roles)
            else:
                matches = all([role in roles for role in targets])
            if not matches:
                data.pop(pid)

    def getValidIDs(self, data):
        """Get the list of valid response IDs"""        
        pids = set(data.keys())
        path = os.path.join(self._survey_folder, "files", "invalid.txt")
        if os.path.isfile(path): 
            with open(path, "r") as file:
                invalids = set([pid.strip() for pid in file.readlines()])
        else: invalids = set()
        return list(pids - invalids)
        
    def getData(self):
        """Read in and save the JSON data"""
        path = os.path.join(self._survey_folder, "files", self._file_name)
        with open(path, "r") as file:
            return json.load(file)

    def removeInvalid(self, data):
        """Remove invalid responses"""
        valid = self.getValidIDs(data)
        pids = list(data.keys())
        for pid in pids:
            if not pid in valid:
                data.pop(pid)

    def getCombos(self):
        combos = []
        for r in range(len(list(self._ids.keys())) + 1):
            combos.extend(list(itertools.combinations(self._ids.keys(), r)))
        return combos

    def generateStrictFolder(self, data):
        combos = self.getCombos()
        for r in combos:
            self.run(copy.deepcopy(data), list(r), True)

    def generateLooseFolder(self, data):
        for r in self._ids.keys():
            self.run(copy.deepcopy(data), [r], False)

    def writeToFile(self, participants, path, fieldnames):
        path = os.path.join(self._survey_folder, "data", path) 
        with open(path, "w", newline="", encoding="UTF-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in participants:
                writer.writerow(p)

    def generateFiles(self, data, role):
        for question in self._ranked:
            self.rankedAnswer(question, data, role)
        for question in self._multi:
            self.getMultiAnswer(question, data, role)
        self.getAllSingleAnswers(data, role)

    def run(self, data, roles=[""], strict=False):

        if roles != [""] and roles != []:
            self.filterByRole(data, roles, strict)

        if len(data) > 0:

            if len(roles) > 0 and roles[0].strip() != "":
                role = "-".join(roles).title()
            else:
                role = "All"

            folder = "-".join(roles)
            if folder == "": 
                folder = "all"
                parent = ""
            else:
                if strict: parent = "strict"
                else: parent = "loose"
                if not os.path.isdir(os.path.join(self._survey_folder, "data", parent)): 
                    os.mkdir(os.path.join(self._survey_folder, "data", parent))

            role_folder_path = os.path.join( self._survey_folder, "data", parent, folder)
            if not os.path.isdir(role_folder_path):
                os.mkdir(role_folder_path)
                os.mkdir(os.path.join(role_folder_path, "rank"))
                os.mkdir(os.path.join(role_folder_path, "multi_select"))
            self.generateFiles(data, os.path.join(parent, folder))

    def rankedAnswer(self, question, data, role):
        participants = []
        formats = set()
        for p in data.values():
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]    
            answer = eval("p" + self.config.types[question[:-1]])[question]
            for i, a in answer.items():
                if i != "other" and a != "":
                    full_answer = self.config.ranked_answers[question][int(i)-1]
                    d[full_answer] = a
                    formats.add(full_answer)
            participants.append(d)
        path = os.path.join(role, "rank", question + ".csv")
        self.writeToFile(participants, path, self.config.shared+list(formats))

    def getMultiAnswer(self, question, data, role):

        participants = []
        formats = set()
        
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            qtype = question[:-1]
            answer = eval("p" + self.config.types[qtype])[question]
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
        self.writeToFile(participants, path, self.config.shared+list(formats))


    def getAllSingleAnswers(self, data, role):

        participants = []

        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            for group, question in self._single:
                answer = p[group][question]
                if type(answer) == dict:
                    if answer["other"]:
                        d[question] = answer["other"]
                    else:
                        d[question] = answer["answers"]
                else:
                    d[question] = answer

            participants.append(d)

        path = os.path.join(role, "single.csv")
        field_names = self.config.shared + [x[1] for x in self._single]
        self.writeToFile(participants, path, field_names)

    def main(self):
        data = self.getData()
        print("Total responses:", len(data))
        self.removeInvalid(data)
        print("Valid responses:", len(data))
        print("Generated CSVs...")
        self.generateStrictFolder(data)
        self.generateLooseFolder(data)
        print("Done!")