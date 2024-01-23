
import os, json, glob

def getFilePath(directory):
    return os.path.join(directory, "files")

def getLatest(directory):
    path = os.path.join(getFilePath(directory), "*completers_*.json")
    files = glob.glob(path)
    files = sorted([f.split(os.sep)[-1][:-5] for f in files])
    return files[-1] + ".json"

def getJSON(directory):
    path = os.path.join(getFilePath(directory), 
                        getLatest(directory))
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def getValid(d, directory):
    pids = set(d.keys())
    path = os.path.join(getFilePath(directory), "invalid.txt")
    if os.path.isfile(path): 
        with open(path, "r") as file:
            invalids = set([pid.strip() for pid in file.readlines()])
    else: invalids = set()
    return list(pids - invalids)
    
def removeInvalid(d, directory):
    valid = getValid(d, directory)
    pids = list(d.keys())
    for pid in pids:
        if not pid in valid:
            d.pop(pid)

def removePII(d, marked):
    for resp in d.values():
        resp.pop("consent")
        resp["meta"].pop("IPAddress")
        resp["meta"].pop("LocationLatitude")
        resp["meta"].pop("LocationLongitude")
        removeMarkedQuestions(resp, marked)

def saveJSON(d, directory):
    path = os.path.join(getFilePath(directory), 
                        getLatest(directory).replace("completers","sanitized"))
    with open(path, "w", encoding="utf-8") as file:
        json.dump(d, file)

def sanitize(directory):
    d = getJSON(directory)
    marked = locateMarkedQuestions(directory)
    removeInvalid(d, directory)
    removePII(d, marked)
    saveJSON(d, directory)

def getQuestions(directory):
    path = os.path.join(directory, "questions.json")
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def locateMarkedQuestions(directory):
    questions = getQuestions(directory)
    marked = []
    for group_name, group_contents in questions.items():
        for question_name, question_contents in group_contents.items():
            if "contains_pii" in question_contents and \
                question_contents["contains_pii"]:
                marked.append((group_name, question_name))
    return marked

def removeMarkedQuestions(resp, marked):
    for group, question in marked:
        resp[group].pop(question)


if __name__ == "__main__":
    sanitize("survey")


