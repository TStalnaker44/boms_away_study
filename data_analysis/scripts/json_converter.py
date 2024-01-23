import os, glob, importlib
from .converter import Converter

# def getConverter(survey_folder, file_name):
#     survey = survey_folder.split(os.sep)[1]
#     full_module_path = f"surveys.{survey}.utils.converter"
#     try:
#         module = importlib.import_module(full_module_path)
#         return module.Converter(survey_folder, file_name)
#     except ImportError as e:
#         print(f"Error importing module {full_module_path}: {e}")
#         return None

def getMostRecent(survey):
    path = os.path.join(survey, "files", "*sanitized_*.json")
    return glob.glob(path)[-1].split(os.sep)[-1]

def convert(survey):
    file_name = getMostRecent(survey)
    conv = Converter(survey, file_name)
    conv.main()