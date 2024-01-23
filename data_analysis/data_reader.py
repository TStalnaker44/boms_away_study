
import re, os, json, glob
from scripts.config import Config

FOLDERS = {"initial":"initial_survey"} # Ideally survey and folder names will match, else alias them here
INDENT = "    "

def main():
    getAvailableSurveys()
    dv = DataViewer()
    dv.main()

def getAvailableSurveys():
    surveys = []
    for survey in os.listdir("surveys"):
        surveys.append(survey.replace("_", " "))
    return surveys

def survey2folder(survey):
    if survey in FOLDERS: folder = FOLDERS[survey]
    else: folder = survey
    folder = os.path.join("surveys", folder)
    return folder.replace(" ", "_")

def getMostRecentData(folder):
    path = os.path.join(folder, "files", "*sanitized_*.json")
    return glob.glob(path)[-1].split(os.sep)[-1]

def getResponseData(survey):
    folder = survey2folder(survey)
    path = os.path.join(folder, "files", getMostRecentData(folder))
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def getValidQuestions(survey):
    folder = survey2folder(survey)
    path = os.path.join(folder, "questions.json")
    with open(path, "r", encoding="utf-8") as file:
        d = json.load(file)
    questions = {}
    for group_content in d.values():
        for q_name, question_content in group_content.items():
            questions[q_name] = question_content["question"]
    return questions
    
def getValidPIDs(response_data):
    return sorted([int(k) for k in response_data.keys()])

class DataViewer():

    def __init__(self):
        self.survey = None
        self.question_index = 0
        self.pid_index = 0
        self.valid_pids = None
        self.valid_questions = None
        self.response_data = None
        self.surveys = getAvailableSurveys()
        self.triple_regex = self.makeTripleRegex()
        self.double_regex = self.makeDoubleRegex()

    def main(self):
        self.printHelloMessage()
        self.mainloop()

    def makeTripleRegex(self):
        surveys = [s.replace(" ", "[ _]") for s in self.surveys]
        regex = "(" + "|".join(surveys) + ")"
        regex += r"( survey)? ([A-Z]{1,2}\d+) (\d+)"
        return re.compile(regex, re.IGNORECASE)
    
    def makeDoubleRegex(self):
        surveys = [s.replace(" ", "[ _]") for s in self.surveys]
        regex = "(" + "|".join(surveys) + ")"
        regex += r"( survey)? ([A-Z]{1,2}\d+)"
        return re.compile(regex, re.IGNORECASE)

    def printHelloMessage(self):
        print("Welcome to the Survey Data Viewer!")
        print("Type 'help' for more information and a full list of commands")

    def mainloop(self):

        commands = {"surveys":self.printSurveys,
            "questions":self.printQuestions,
            "responses":self.printPIDs,
            "current":self.printCurrent,
            "next":self.nextPID,
            "prev":self.prevPID,
            "help":self.printHelp,
            "nextq":self.nextQuestion,
            "prevq":self.previousQuestion}
                
        while True:
            selection = input(">>> ")
            if selection == "":
                if self.survey: 
                    self.nextPID()
            elif selection.lower().replace("_", " ") in self.surveys:
                self.selectSurvey(selection)
                self.printResponse()
            elif re.match(r"([A-Za-z]{1,2})\d+", selection):
                self.selectQuestion(selection)
                self.printResponse()
            elif selection.isdigit():
                self.selectResponse(selection)
                self.printResponse()
            elif self.triple_regex.match(selection):
                self.selectByAll(selection)
                self.printResponse()
            elif self.double_regex.match(selection):
                self.selectByTwo(selection)
                self.printResponse()
            elif selection.lower() == "exit" or selection.lower() == "quit":
                print(INDENT + "Good-bye.")
                break
            elif re.match(r"show (([A-Za-z]{1,2})\d+)", selection, re.IGNORECASE):
                self.printQuestionText(selection)
            elif selection.lower() in commands:
                commands[selection.lower()]()
            else:
                print(INDENT + "Unknown command.")

    def getResponse(self, question, pid):
        config = Config(survey2folder(self.survey))
        qtype = re.search(r"([A-Z]{1,2})\d+", question).group(1)
        if self.survey in ("initial", "machine learning", "legal"):
            return self.response_data[str(pid)][config.types[qtype]][question]
        else:
            return eval("self.response_data[str(pid)]" + config.types[qtype])[question]

    def printResponse(self):
        if self.survey:
            question = self.getQuestion(self.question_index)
            pid = self.getPID(self.pid_index)
            resp = str(self.getResponse(question, pid)).strip()
            if resp == "": resp = "<No Response>"
            fields = (self.survey.title(), question, 
                    self.valid_questions[question], str(pid), resp)
            output = INDENT + "Survey: %s\nQuestion: %s - %s\nParticipant: %s\nResponse:\n%s" % fields
            print(output.replace("\n", "\n" + INDENT))

    def printCurrent(self):
        if self.survey:
            print(INDENT + "Survey:", self.survey.title())
            print(INDENT + "Question:", self.getQuestion(self.question_index))
            print(INDENT + "Participant:", self.getPID(self.pid_index))
        else:
            print(INDENT + "First select content to view.")

    def printQuestionText(self, question):
        q = re.match(r"show ([A-Za-z]{1,2}\d+)", question, re.IGNORECASE).group(1)
        if q.upper() in self.valid_questions:
            print(INDENT + f"{self.valid_questions[q.upper()]}")
        else:
            print(INDENT + "Unknown question ID.")

    def printQuestions(self):
        if self.valid_questions:
            questions = list(self.valid_questions.keys())
            print(INDENT + ", ".join(questions))
        else:
            print(INDENT + "No survey selected.  Please select a survey to continue.")

    def printPIDs(self):
        if self.valid_pids:
            pids = ", ".join(str(pid) for pid in self.valid_pids)
            print(INDENT + pids)
        else:
            print(INDENT + "No survey selection.  Please select a survey to continue.")

    def printSurveys(self):
        print(INDENT + ", ".join(self.surveys).title())

    def selectSurvey(self, survey):
        survey = survey.lower().replace("_", " ")
        print(INDENT + f"{survey.capitalize()} survey selected.")
        self.survey = survey
        self.question_index = 0
        self.pid_index = 0
        self.update()

    def update(self):
        self.response_data = getResponseData(self.survey)
        self.valid_questions = getValidQuestions(self.survey)
        self.valid_pids = getValidPIDs(self.response_data)

    def incrementPID(self):
        self.pid_index = min(self.pid_index+1,
                             len(self.valid_pids))
        
    def decrementPID(self):
        self.pid_index = max(0, self.pid_index-1)

    def nextQuestion(self):
        self.question_index = min(self.question_index+1,
                               len(self.valid_questions))
        if self.question_index == len(self.valid_questions):
            print("There is no next question.")
            self.question_index -= 1
        else:
            self.printResponse()

    def previousQuestion(self):
        self.question_index = max(-1, self.question_index-1)
        if self.question_index == -1:
            print("There is no previous question.")
            self.question_index += 1
        else:
            self.printResponse()

    def nextPID(self):
        if self.pid_index == len(self.valid_pids) - 1:
            print("There are no more valid responses.")
        else:
            self.incrementPID()
            self.printResponse()

    def prevPID(self):
        if self.pid_index == 0:
            print("There is no previous response.")
        else:
            self.decrementPID()
            self.printResponse()

    def getQuestion(self, index):
        return list(self.valid_questions.keys())[index]
    
    def getPID(self, index):
        return self.valid_pids[index]
    
    def selectByTwo(self, selection):
        m = self.double_regex.match(selection)
        survey = m.group(1).replace("_", " ").lower() 
        if survey in self.surveys:
            question = m.group(3).upper()
            possible_questions = getValidQuestions(survey)
            if question in possible_questions.keys():
                pid = 0
                self.survey = survey
                self.update()
                self.selectQuestion(question)
                self.selectResponse(pid)
            else:
                print("Invalid question ID.")
        else:
            print("Unknown survey.")
    
    def selectByAll(self, selection):
        m = self.triple_regex.match(selection)
        survey = m.group(1).replace("_", " ").lower() 
        if survey in self.surveys:
            response_data = getResponseData(survey)
            question = m.group(3).upper()
            possible_questions = getValidQuestions(survey)
            if question in possible_questions.keys():
                pid = int(m.group(4))
                possible_pids = getValidPIDs(response_data)
                if pid in possible_pids: 
                    self.survey = survey
                    self.update()
                    self.selectQuestion(question)
                    self.selectResponse(pid)
                else:
                    print("Invalid participant ID")
            else:
                print("Invalid question ID.")
        else:
            print("Unknown survey.")
        
    def selectQuestion(self, question):
        question = question.upper()
        questions = list(self.valid_questions.keys())
        if question in questions:
            self.question_index = questions.index(question)
        else:
            print(INDENT + "Unknown question ID.")

    def selectResponse(self, pid):
        pid = int(pid)
        if pid in self.valid_pids:
            self.pid_index = self.valid_pids.index(pid)
        else:
            print(INDENT + "Unknown participant ID.")

    def printHelp(self):
        print(INDENT + "Type a survey name, question ID, or participant ID to navigate.")
        print(INDENT + "Type two like '<survey> <question id>' for fast navigation.")
        print(INDENT + "Type all three like '<survey> <question id> <participant id>' for faster navigation.")
        print(INDENT + "Hit enter to see the next valid response.")
        print(INDENT + "Type 'questions' to see available question IDs.")
        print(INDENT + "Type 'responses' to see available response IDs.")
        print(INDENT + "Type 'surveys' to see available surveys.")
        print(INDENT + "Type 'current' to see current selections.")
        print(INDENT + "Type 'show <question id>' to see that question's text.")
        print(INDENT + "Type 'prev' to navigate to the previous response.")
        print(INDENT + "Type 'next' to navigate to the next response.")
        print(INDENT + "Type 'prevq' to navigate to the previous question.")
        print(INDENT + "Type 'nextq' to navigate to the next question.")
        print(INDENT + "Type 'exit' or 'quit' to quit.")
        print(INDENT + "Type 'help' to see this page.")

if __name__ == "__main__":
    main()

    


