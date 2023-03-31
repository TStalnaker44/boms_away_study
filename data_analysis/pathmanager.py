
import os

class PathManager():

    def __init__(self, directory):
        self.dir = directory
        self.role = ""
        self.strict = False

    def getDataPath(self):
        if self.dir in ("initial_survey", "key_projects", "machine_learning", "cyber_physical", "legal") :
            if self.role == "":
                return os.path.join(self.dir, "data", "all")
            else:
                if self.strict:
                    return os.path.join(self.dir, "data", "strict", self.role)
                else:
                    return os.path.join(self.dir, "data", "loose", self.role)
        else:
            return os.path.join(self.dir, "data")
                
    def getFigPath(self):
        if self.dir in ("initial_survey", "key_projects", "machine_learning", "cyber_physical", "legal"):
            if self.role == "":
                self.mkdir("all")
                return os.path.join(self.dir, "figs", "all")
            else:
                if self.strict:
                    self.mkdir("strict", self.role)
                    return os.path.join(self.dir, "figs", "strict", self.role)
                else:
                    self.mkdir("loose", self.role)
                    return os.path.join(self.dir, "figs", "loose", self.role)
        else:
            return os.path.join(self.dir, "figs")
        
    def mkdir(self, *path):
        folders = os.path.sep.join(path).split(os.path.sep) ## Path components may themselves be paths
        for i in range(1, len(folders)+1):
            temp = os.path.join(self.dir, "figs", os.path.join(*folders[:i]))
            if not os.path.isdir(temp):
                os.mkdir(temp)