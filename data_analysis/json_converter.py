import os, glob
from json_converters.initial_survey import InitialConverter
from json_converters.key_projects import KeyConverter
from json_converters.machine_learning import AIConverter
from json_converters.cyber_physical import CyberConverter
from json_converters.legal import LegalConverter

def main():
    survey = "cyber_physical"
    assert survey in ("key_projects", "initial_survey", "machine_learning", "cyber_physical", "legal")
    convert(survey)

def getMostRecent(survey):
    path = os.path.join(survey, "files", "*sanitized_*.json")
    return glob.glob(path)[-1].split(os.sep)[-1]

def convert(survey):

    file_name = getMostRecent(survey)

    if survey == "initial_survey":
        conv = InitialConverter(survey, file_name)
    elif survey == "key_projects":
        conv = KeyConverter(survey, file_name)
    elif survey == "machine_learning":
        conv = AIConverter(survey, file_name)
    elif survey == "cyber_physical":
        conv = CyberConverter(survey, file_name)
    elif survey == "legal":
        conv = LegalConverter(survey, file_name)
        
    conv.main()

if __name__ == "__main__":
    main()