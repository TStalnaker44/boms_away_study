
import os
from scripts.qualtrics_reader import makeQJSON

OVERWRITE = False
SURVEYS = ["YOUR SURVEY HERE"]

for survey in SURVEYS:
    survey_path = os.path.join("surveys", survey)
    path = os.path.join(survey_path, "questions.json")
    if (not os.path.exists(path)) or OVERWRITE:
        makeQJSON(survey_path)

print("Remember to review the generated file! Some manual edits may be needed.")
print("IMPORTANT: Question IDs must be unique, even across groups.")
print("Be sure to add the 'contains_pii' tag were necessary")
