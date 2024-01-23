
import json, re, os

class Config():

    def __init__(self, survey):
        self.ranked_answers = {}
        self.loadData(survey)
        self.setTypes()
        self.setQTypes()
        self.ids, self.id_path = self.getIDs(survey)
        self.shared = ["ResponseID"]

    def loadData(self, survey):
        path = os.path.join(survey, "questions.json")
        with open(path, "r") as file:
            self.data = json.load(file)

    def getIDs(self, survey):
        questions = self.loadQuestions(survey)
        for gname, group in questions.items():
            for qname, question in group.items():
                if question.get("identifier"):
                    ids = question.get("roles", None)
                    if ids == None: 
                        raise ValueError("The 'identifier' tag must be accompanied by the 'roles' tag")
                    path_to_ids = (gname, qname)
                    return ids, path_to_ids
        else: return {}, ()

    def loadQuestions(self, survey):
        path = os.path.join(survey, "questions.json")
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def setTypes(self):
        self.types = {}
        for label, questions in self.data.items():
            first_qid = list(questions.keys())[0]
            short_label = re.sub(r'[^A-Za-z]', '', first_qid)
            self.types[short_label] = f"['{label}']"
        
    def setQTypes(self):
        self.ranked, self.multi, self.single = [], [], []
        self.likert = []
        for label, questions in self.data.items():
            for qid, qdata in questions.items():
                qtype = qdata["type"]
                if not qdata.get("contains_pii"):
                    if qtype in ("single-select", "single-select-with-other", "likert", "single-text"):
                        self.single.append((label, qid))
                    elif qtype in ("short-answer", "email"): pass
                    elif qtype == "multi-select-with-other":
                        self.multi.append(qid)
                    elif qtype == "likert":
                        self.likert.append(qid)
                    elif qtype in ("ranked", "ranked-with-other"):
                        self.ranked.append(qid)
                        self.ranked_answers[qid] = qdata["options"]