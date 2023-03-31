
from initial_survey.csv2json import convertCSV as initial_convertCSV
from machine_learning.csv2json import convertCSV as ai_convertCSV
from key_projects.csv2json import convertCSV as key_convertCSV
from cyber_physical.csv2json import convertCSV as cyber_convertCSV
from legal.csv2json import convertCSV as legal_convertCSV
from partition import partition
from sanitize import sanitize
from json_converter import convert
from plot import plot

FROM_SOURCE = False # Code to run if building from original csv files (not included with remote)
PRE_PROCESS = False # pre-process the data before plotting
PLOT = True # plot figures for all surveys

all_surveys = ("initial_survey", "key_projects", "machine_learning", "cyber_physical", "legal")

if PRE_PROCESS:
    if FROM_SOURCE:

        ## Generate JSON Files from CSV
        initial_convertCSV()
        ai_convertCSV()
        key_convertCSV()
        cyber_convertCSV()
        legal_convertCSV()

        ## Sanitize JSON
        print("Sanitizing files...")
        for survey in all_surveys:
            sanitize(survey)

    ## Convert JSON to CSV
    print("Converting JSON to CSV...")
    for survey in all_surveys:
        convert(survey)

    ## Partition response coding
    print("Partitioning Response Coding Files...")
    for survey in ("initial_survey", "key_projects"):
        partition(survey)

if PLOT:
    ## Plot the results
    print("Plotting Results (this may take awhile)...")
    for survey in all_surveys:
        print(f"Plotting {survey} survey...")
        plot(survey)

print("All Data Processed!")