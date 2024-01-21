import json, os, glob, re
from json_converters.initial_survey import config as in_config
from json_converters.machine_learning import config as ai_config
from json_converters.cyber_physical import config as cp_config
from json_converters.key_projects import config as kp_config
from json_converters.legal import config as lg_config

surveys = ("initial", "key projects", "machine learning", "cyber physical", "legal")

regex = re.compile("(initial|machine[ _]learning|cyber[ _]physical|legal|key[ _]projects)( survey)? ([A-Z]{1,2}\d+) (\d+)",
                    re.IGNORECASE)

def getConfig(survey):
    if survey == "initial": return in_config
    elif survey == "machine learning": return ai_config
    elif survey == "cyber physical": return cp_config
    elif survey == "key projects": return kp_config
    elif survey == "legal": return lg_config
    else: return {}

def getSurvey():
    while True:
        survey = input(">>> Enter a survey: ").lower().replace("_", " ")
        survey = survey.replace("survey", "").strip()
        if survey in surveys:
            print(f"{survey.capitalize()} survey selected.")
            return survey
        else:
            print(f"{survey} is not a valid survey name.")

def getValidQuestions(survey):
    survey = survey.replace(" ", "_")
    if survey == "initial": survey = "initial_survey"
    path = os.path.join(survey, "questions.json")
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
        
def getMostRecent(survey):
    path = os.path.join(survey, "files", "*sanitized_*.json")
    return glob.glob(path)[-1].split(os.sep)[-1]

def getData(survey):
    survey = survey.replace(" ", "_")
    if survey == "initial": survey = "initial_survey"
    path = os.path.join(survey, "files", getMostRecent(survey))
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def getValidUserIDs(data):
    return sorted([int(k) for k in data.keys()])
    
def getQuestion(survey, valid):
    while True:
        qid = input(">>> Enter a question ID: ").upper().strip()
        if qid in valid:
            print(f"Question {qid} selected.")
            return qid
        else:
            print(f"{qid} is not a valid question ID for the {survey} survey.")

def getUserID(survey, valid):
    while True:
        pid = int(input(">>> Enter a participant ID: ").strip())
        if pid in valid:
            print(f"Participant {pid} selected.")
            return pid
        else:
            print(f"{pid} is not a valid participant ID for the {survey} survey.")

def getResponse(data, survey, question, user):
    config = getConfig(survey)
    qtype = re.search("([A-Z]{1,2})\d+", question).group(1)
    if survey in ("initial", "machine learning", "legal"):
        return data[str(user)][config.types[qtype]][question]
    else:
        p = data[str(user)]
        return eval("p" + config.types[qtype])[question]
    
def getNextValidIndex(valid_pids, user):
    new = valid_pids.index(user) + 1
    if new >= len(valid_pids): return -1
    else: return new

def selectSurvey():
    survey = getSurvey()
    data = getData(survey)
    question, user, valid_pids, valid_questions = selectQuestion(survey, data)
    return data, survey, question, user, valid_pids, valid_questions

def selectQuestion(survey, data):
    valid_questions = getValidQuestions(survey)
    question = getQuestion(survey, valid_questions.keys())
    user, valid_pids = selectUser(survey, data)
    return question, user, valid_pids, valid_questions

def selectUser(survey, data):
    valid_pids = getValidUserIDs(data)
    user = getUserID(survey, valid_pids)
    return user, valid_pids

def printResponse(data, survey, question, user, valid_pids, valid_questions):
    resp = getResponse(data, survey, question, user)
    if resp == "": resp = "<No Response>"
    fields = (survey.title(), question, valid_questions[question], str(user), resp)
    print("\nSurvey: %s\nQuestion: %s - %s\nParticipant: %s\nResponse:\n\n%s\n" % fields)
    return getNextValidIndex(valid_pids, user)

def main():

    print()
    print("Welcome to the Survey Data Viewer!")
    print("Type 'help' for more information and a full list of commands")
    print()

    #data, survey, question, user, valid_pids, valid_questions = selectSurvey()
    #printResponse(data, survey, question, user, valid_pids, valid_questions)
    #index = getNextValidIndex(valid_pids, user)

    survey = None

    while True:

        if survey != None:
            user = valid_pids[index]

        selection = input(">>> ")
        
        if selection == "":
            if survey == None:
                pass
            else:
                if index < 0:
                    print("There are no more valid responses.")
                else:
                    index = printResponse(data, survey, question, user, valid_pids, valid_questions)

        elif selection.lower().replace("_", " ") in surveys:
            survey = selection.lower().replace("_", " ")
            data = getData(survey)
            question, user, valid_pids, valid_questions = selectQuestion(survey, data)
            index = printResponse(data, survey, question, user, valid_pids, valid_questions)

        elif re.match("([A-Za-z]{1,2})\d+", selection):
            if selection.upper() in valid_questions.keys():
                question = selection.upper()
                user, valid_pids = selectUser(survey, data)
                index = printResponse(data, survey, question, user, valid_pids, valid_questions)
            else:
                print("Unknown question ID.")

        elif selection.isdigit():
            if int(selection) in valid_pids:
                user = int(selection)
                index = printResponse(data, survey, question, user, valid_pids, valid_questions)
            else:
                print("Unknown participant ID.")

        elif regex.match(selection):

            m = regex.match(selection)

            s = m.group(1).replace("_", " ").lower() 
            if s in surveys: 
                d = getData(s)
                q = m.group(3).upper()
                possible_questions = getValidQuestions(s)
                if q in possible_questions.keys(): 
                    u = int(m.group(4))
                    possible_ids = getValidUserIDs(d)
                    if u in possible_ids: 
                        survey = s
                        question = q
                        user = u
                        valid_pids = possible_ids
                        valid_questions = possible_questions
                        data = d
                        index = printResponse(data, survey, question, user, valid_pids, valid_questions)
                    else:
                        print("Invalid participant ID")
                else:
                    print("Invalid question ID.")
            else:
                print("Unknown survey.")

        elif selection.lower() == "exit" or selection.lower() == "quit":
            print("Good-bye.")
            break

        elif selection.lower() == "help":
            print()
            print("Type a survey name, question ID, or participant ID to navigate.")
            print("Type all three like '<survey> <question id> <participant id>' for fast navigation.")
            print("Hit enter to see the next valid response.")
            print("Type 'questions' to see available question IDs.")
            print("Type 'responses' to see available response IDs.")
            print("Type 'surveys' to see available surveys.")
            print("Type 'current' to see current selections.")
            print("Type 'show <question id>' to see that question's text.")
            print("Type 'exit' or 'quit' to quit.")
            print("Type 'help' to see this page.")
            print()

        elif selection.lower() == "current":
            print()
            print("Survey:", survey.title())
            print("Question:", question)
            print("Participant:", user)
            print()

        elif re.match("show (([A-Za-z]{1,2})\d+)", selection, re.IGNORECASE):
            q = re.match("show ([A-Za-z]{1,2}\d+)", selection, re.IGNORECASE).group(1)
            print(f"\n{valid_questions[q.upper()]}\n")

        elif selection.lower() == "questions":
            print(sorted(list(valid_questions.keys())))

        elif selection.lower() == "responses":
            print(valid_pids)

        elif selection.lower() == "surveys":
            print(surveys)

        else:
            print("Unknown command.")
        
main()