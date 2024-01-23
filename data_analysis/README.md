# Survey Analysis Tool Support

## Required Libraries
In order to run the data cleaning and analysis tools, the following libraries will need to be installed.

```
pip install pandas
pip install matplotlib
```

## Getting Started
To start analyzing your first survey, you will need to create the `surveys` directory and populate it with your Qualtrics survey. See "Adding a New Survey" below.

The `run_all.py` file is the main hub for processing and analysis.  Once everything has been configured, the pipeline should work seemlessly (from Qualtics data conversion all the way through to plotting figures).

Specific functionality can be toggled on and off by adjusting the `config.py` file.  This file will also allow you to select one or more surveys to work with.  Further explanation of the adjustable parameters is available within the `config.py` file.

### Adding a New Survey
Note: If this is your first time using the tool, you will also need to create the `surveys` directory.  Put this at the top-level.

Adding a new survey for analysis is as simple as adding a few files.  First create a new folder in the `surveys` directory.  This is where you will store all of your survey related files.  You can name the folder however you like, but it is advised to avoid spaces.  You will use this folder name to identify your survey in the `config.py` file.

Now that you have your main survey folder, it's time to add some files. First, add a `files` folder to your survey directory.

### Preparing the Data
You will need to manually download and place the Qualtrics data export of the responses to your survey in your `files` directory.  Within the Qualtrics system, navigate to the "Data and Analysis" tab of your survey and click on the "Export & Import" button to open the "Download a data table" menu. From here, on the "CSV" tab, ensure that the "Download all fields" and "Use choice text" options are selected, then click "Download" to export your data. To ensure compatibility with this system, rename the downloaded file according to this format: `data_MM_DD_YY.csv`. 

You can store multiple files in this format. The scripts are smart enough to use the date information to determine the most recent file and use it for processing.

When the provided CSV file is converted into a more readable JSON, the tool also automatically filters out partial or incomplete survey responses.  You should notice two new files generated in the `files` directory: `completers_MM_DD_YY.json` and `sanitized_MM_DD_YY.json`.  `completers` contains all the information from the CSV export, including PII and contact information.  `sanitized` on the other hand has all content marked as PII removed as well as removing all responses identified as invalid (see `invalid.txt`).  These files are safe to upload to public repositories or replication packages.  By default, this repository's `.gitignore` is set to filter out both the `data` and `completer` type files.  They can be safely stored locally without fear of accidentally pushing them to remote.

### Required files
The survey infrastructure package is designed to work out of the box as much as possible, but does require some manual set-up.  A few files are required before the program can run successfully.  We now explore each required file.

#### questions.json 
Should be placed at the top-level of your survey folder.  This file is used to specify the survey sections, question ids, question text, question types, and other relevant information.  The structure you provide will also inform how your data JSON files will be created. Within the Qualtrics system, navigate to the "Survey" tab of your survey and click on "Tools" > "Import/Export" > "Export Survey" to download a *.qsf file of your survey's structure. Place this file within your survey's `files` directory. From your survey directory, run `scripts/qualtrics_reader.py` to generate the `questions.json` file for your survey. Details of the structure of this file are included below.

You should not include an initial question asking for user consent in your `questions.json`.

The names assigned to questions should be distinct, even across groups.  Assigned names do not have to match those you assigned in Qualtrics, but it is good practice to keep them synced.

An example has been provided below.

Recognized Question Types:
- `single-select`
- `single-select-with-other`
- `multi-select-with-other`
- `ranked`
- `ranked-with-other`
- `likert`
- `short-answer` (for longer form responses)
- `single-text` (for short form textual answers)
- `email`

Important note: `short-answer` should be used for questions where users are unlikely to provide duplicate answers to questions, whereas `single-text` should be used where duplicated answers are possible (e.g. "How old are you?). `short-anwer` questions will not be included in figures generated, as it is expected that such answers would all be unique.

Additional Fields:
- `contains_pii`
    - Denotes that a question contains sensitive information which should be sanitized.
    - Values: boolean
    - Optional field
- `options`
    - Specifies the ranking options provided to survey participants.
    - IMPORTANT: must be in the order presented / recorded
    - Values: List of strings
    - Required for `ranked` and `ranked-with-other` type questions.
- `identifier`
    - Denotes that a question allows participants to self-identify.
    - Used to automatically segment data for analysis across roles.
    - Values: boolean
    - Optional field
- `roles`
    - Provides a mapping of roles that participants can identify as.
    - Values: dictionary of key/value pairs
    - Format: "\<abbreviated form>":"\<selection as appears in survey>"
    - Required when `identifier` tag has been used.

Example:
```
{
"main":{
    "M1":
        {"question":"Please describe which role(s) best describe you.",
        "type":"multi-select-with-other",
        "identifier":true,
        "roles":{"developer":"software developer",
                "engineer":"software engineer",
                "tester":"software tester"}},
    "M2":
        {"question":"Please order these programming languages from your most to least used.",
        "type":"ranked",
        "options":["Java", "C/C++", "Python", "JavaScript", "Ruby"]
},
"demographics":{
    "D1": 
        {"question":"Do you have a background in computer security? Formal (college classes, degree, certification) or informal (self-learning or other training)?",
        "type":"single-select"},
    "D2": 
        {"question":"Which country / countries are you and / or your organization based in?", 
        "type":"short-answer",
        "contains_pii":true},
    "D3": 
        {"question":"Please enter your email address. This will be used to contact you for compensation. If we are interested in your responses, we may contact you for a follow-up interview, if you are willing.", 
        "type":"email",
        "contains_pii":true}
}
}
```

#### metafields.json
This file is what allows the tool to store the survey metadata that is relevant to your usecase.  It is a simple JSON file containing key/value pairs.  The keys are the names you wish to give the fields and the values provide the location (column number) of the metadata in the qualtrics data export.

You can add or remove fields to this file as you wish.  Though it is recommended to start with the provided sample and modify from there.

Sample:
```
{"StartDate":0, 
 "EndDate":1, 
 "Status":2, 
 "IPAddress":3,
 "Progress":4, 
 "Duration":5, 
 "Finished":6, 
 "RecordedDate":7, 
 "ResponseID":8, 
 "LocationLatitude":13, 
 "LocationLongitude":14,
 "UserLanguage":16}
```

#### invalid.txt 
This file is optional, but if included, it will exclude PIDs from the produced sanitized JSON.  Each invalid PID should be written on it's own line.  No commas or other delimiters are necessary. This should also be placed in the `files` directory of your survey.

### Response Coding
For survey questions that ellicit longer responses, you will likely want to employ some form of coding methodology (e.g. CITATION).  Once you have assigned codes to these responses, you can add the `response_coding.csv` file to the `data` directory and have the script produce figures and also split the data across any roles you've specified.

You can run the tool without including `response_coding.csv`, but ensure that you set `RESPONSE_CODING_DONE` to `False` in `config.py`.

Note: Additional tooling is available to facilitate the coding process and the creation of the `response_coding.csv`.

## Generated Files
### Data Files
Cleaned and partitioned data will be stored in the `data` directory. If the directory does not already exist, the tool will create it.  Data is stored in CSV form and is split by the roles specified previously.  Any manual changes made to these files will be overwritten the next time the scripts are run. 

### Figures
Automatically generated figures are found in the `figs` directory. If the directory does not already exist, the tool will create it.  Figures can be generated in a variety of formats (PNG and PDF for example) and are additionally plotted by role.  These figures are intended to give you quick insights into your data and are not paper ready.

## Directory Structure
Below is a directory map that should help you easily determine where to place your files.
```
├── scripts
│   ├── ...
├── surveys
│   ├── sample_survey
│       ├── data
│       │   │── ...
│       ├── figs
│       │   │── ...
│       ├── files
│       │   │── data_01-22-24.csv
│       │   │── sample_survey_completers_01-22-24.json
│       │   │── sanmple_survey_sanitized_01-22-24.json
│       │   │── invalid.txt
│       ├── metafields.json
│       ├── questions.json
├── config.py
├── data_reader.py
├── run_all.py
├── README.md
└── .gitignore
```

## Easy Analysis with the Data Reader
Running `data_reader.py` will allow you to explore the processed data from all the surveys stored in your `surveys` directory.  The program provides an easy, human readable way to navigate your data through a terminal window.  This is particularly useful for response coding related tasks, allowing the user to move between responses easily and quickly.

You will need to type the name of a survey to get started.  Further information on navigation and the full list of accepted commands is found below:

- **surveys**: shows the list of available surveys
- **questions**: shows the list of valid question IDs
- **responses**: shows the list of valid response IDs
- **current**: shows the current configuration of the system
- **prev**: navigate to the previous response, if there is one
- **next**: navigate to the next response, if there is one
- **prevq**: navigate to the previous question, if there is one
- **nextq**: navigate to the next question, if there is one
- **quit**: quits the program
- **exit**: quits the program
- **help**: shows the help menu
- **show \<question ID>**: displays question text for that question ID
- **\<survey>**: navigates to the provided survey
- **\<question ID>**: navigates to the provided question
- **\<response ID>**: navigates to the provided response
- **\<survey> \<question ID>**: provides rapid navigation control
- **\<survey> \<question ID> \<response ID>**: provides rapid navigation control
- **\<hitting enter>**: short-hand for the `next` command; navigates to next response

## Scripts

The `run_all.py` file calls all relevant scripts for data analysis, including cleaning, converting, and plotting data. The scripts it relies on are held in the `scripts` directory:

- The `plot.py` file can be run to generate plots for a given survey (this doesn't work with the roles functionality yet).

- The `sanitize.py` file is run to clean the produced JSON and remove any PII before pushing to GitHub.

- The `json_converter.py` file populates the data folder for a survey using the most recent, respective JSON file (located in the `files` directory).

- The `converter.py` file contains functions which can populate the data folder of a survey.

- The `partition.py` file reads and partitions the `response_coding.csv` file by group for a survey.  The result is multiple `response_coding.csv` files each containing only responses from a particular group.

- The `pathmanager.py` file provides an abstraction of the directory structure for the `plot.py` file.

- The `qualtrics_reader.py` file reads a *.qsf file from Qualtrics and extracts relevant information into a `questions.json` file.

- The `config.py` file stores and manages data about surveys in the system.

- The `csv2json.py` file manages conversion of survey output data into the correct JSON format.
