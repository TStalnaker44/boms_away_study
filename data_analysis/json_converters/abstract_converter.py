
import os, json, itertools, copy, csv

class AbstractConverter():

    def __init__(self, file_name, parent):
        self._file_name = file_name
        self._parent = parent

        self._ids = {}
        self._ranked = []
        self._multi = []
    
    def filterByRole(self, data, targets, strict=False):
        targets = [self._ids[t] for t in targets]
        pids = list(data.keys())
        for pid in pids:
            roles = data[pid]["self_identification"]["ID"]
            if strict:
                matches = set(targets) == set(roles)
            else:
                matches = all([role in roles for role in targets])
            if not matches:
                data.pop(pid)

    def getValidIDs(self, data):
        """Get the list of valid response IDs"""
        path = os.path.join(self._parent, "files", "valid.txt")
        if os.path.isfile(path):
            with open(path, "r") as file:
                return [pid.strip() for pid in file.readlines()]
        else:
            return list(data.keys())
    
    def getData(self):
        """Read in and save the JSON data"""
        path = os.path.join(self._parent, "files", self._file_name)
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
        path = os.path.join(self._parent, "data", path) 
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

            print("-".join(roles).title(), "responses:", len(data))

            folder = "-".join(roles)
            if folder == "": 
                folder = "all"
                parent = ""
            else:
                if strict:
                    parent = "strict"
                    if not os.path.isdir(os.path.join(self._parent, "data", "strict")): 
                        os.mkdir(os.path.join(self._parent, "data", "strict"))
                else:
                    parent = "loose"
                    if not os.path.isdir(os.path.join(self._parent, "data", "loose")): 
                        os.mkdir(os.path.join(self._parent, "data", "loose"))

            if not os.path.isdir(os.path.join( self._parent,"data", parent, folder)):
                os.mkdir(os.path.join(self._parent, "data", parent, folder))
                os.mkdir(os.path.join(self._parent, "data", parent, folder, "rank"))
                os.mkdir(os.path.join(self._parent, "data", parent, folder, "multi_select"))
            self.generateFiles(data, os.path.join(parent, folder))

    def main(self):
        data = self.getData()
        print("Total responses:", len(data))
        self.removeInvalid(data)
        print("Valid responses:", len(data))
        print("Generated CSVs...")
        self.generateStrictFolder(data)
        self.generateLooseFolder(data)
        print("Done!")