
from scripts.csv2json import CSVConverter
from scripts.sanitize import sanitize
from scripts.json_converter import convert
from scripts.partition import partition
from scripts.plot import plot
import os, config

for survey in config.SURVEYS:

    survey_path = os.path.join("surveys", survey)
    print("Processing %s survey..." % (survey,))

    if config.PRE_PROCESS:

        if config.FROM_SOURCE:

            # Generate JSON Files from CSV
            CSVConverter(survey_path).convertCSV()

            # Sanitize JSON
            print("Sanitizing files...")
            sanitize(survey_path)

        # Make the data directory if it doesn't exist
        data_path = os.path.join(survey_path,"data")
        if not os.path.isdir(data_path):
            os.mkdir(data_path)

        ## Convert JSON to CSV
        print("Converting JSON to CSV...")
        convert(survey_path)

        if config.RESPONSE_CODING_DONE:
            ## Partition response coding
            print("Partitioning Response Coding Files...")
            partition(survey_path)

    if config.PLOT:

        # Make the figs directory if it doesn't exist
        fig_path = os.path.join(survey_path,"figs")
        if not os.path.isdir(fig_path):
            os.mkdir(fig_path)

        ## Plot the results
        print("Plotting Results (this may take awhile)...")
        for ft in config.FILE_TYPES:
            print(f"Plotting {survey} survey as {ft}...")
            plot(survey_path, ft)

print("All data processed!")