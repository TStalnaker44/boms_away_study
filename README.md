# Data Analysis for SBOM Surveys

All data in this repository has been sanitized and anonymized.

Below describes the ideal structure of this repo, but it is still a work in progress.  Not all folders are available or complete.

## Required Modules
- `pip install pandas`
- `pip install matplotlib`

## Directory Structure

The `survey_questions` folder contains the questions asked in the various surveys administered.

The `codes.json` file lists and defines the codes assigned to the responses to open-ended questions.

The `Interview_Protocol.pdf` file describes the process followed during follow-up interviews with participants.

The `data_analysis` folder contains aggregated survey results and code used to analyze these results.


## Data Analysis

- The `run_all.py` file is the one stop solution to clean, convert, and plot data for all surveys.  Be warned that generating all the plots will take some time.  It could take up to 5 minutes to run this file.

- The `plot.py` file can be run to generate plots for a given survey (this doesn't work with the roles functionality yet).

- The `sanitize.py` file is run to clean the produced JSON and remove any PII before pushing to GitHub.

- The `json_converter.py` file populates the data folder for a survey using the most recent, respective JSON file (located in the `files` directory).

- The `partition.py` file reads and partitions the `response_coding.csv` file by group for a survey.  The result is multiple `response_coding.csv` files each containing only responses from a particular group.

- The `pathmanager.py` file provides an abstraction of the directory structure for the `plot.py` file.

### Survey Results

Within the `data_analysis` folder, there is a parent folder for each of the surveys:
- `initial_survey`
- `key_projects`
- `machine_learning`
- `cyber-physical`
- `legal`

Each parent folder has three nested folders:
- `data`: contains folders with the csv data for responses
- `figs`: contains figures plotting the collected data
- `files`: contains the raw, sanitized JSON files and a file listing valid response IDs

Each parent folder also has a few files:
- `csv2json.py`: converts raw Qualtrics data into a human-readable JSON representation
- `likert.txt`: lists the likert scale questions in the survey
- `questions.json`: A JSON file mapping question IDs to text

## Exploring the Data with the Data Reader

Running the `data_reader.py` file allows the user to explore the data from all surveys in an easy and human readable way through a terminal window.  When the program starts, it will prompt the user for a survey, a question ID, and a participant ID.  Once these are supplied, the user is given more control over how they navigate.

Here is the list of accepted commands:
- surveys: shows the list of available surveys
- questions: shows the list of valid question IDs
- responses: shows the list of valid response IDs
- current: shows the current configuration of the system
- quit: quits the program
- exit: quits the program
- help: shows the help menu
- show \<question ID>: displays question text for that ID
- \<survey>: navigates to the provided survey
- \<question ID>: navigates to the provided question
- \<response ID>: navigates to the provided response
- \<survey> \<question ID> \<response ID>: provides rapid navigation control
- hitting enter: proceeds to the next response, if one is available 

### The Data Folder

The data folder for each survey is further sub-divided into three additional folders:
- `all`: the most useful, contains all response data for questions
- `loose`: provides response data by role (i.e. producer).  Filtering is loose, so a producer + consumer is still considered a producer. 
- `strict`: provides response data by specific role.  Filtering is strict, so a producer + consumer is not considered a consumer.  That is, all combinations of roles are represented in distinct CSV files.

### CSV Files
There are two CSV files at the top level:
- `single`: contains the responses to all single answer questions
- `response_coding`: contains the results of our collective coding process

There are two sub-folders that contain exclusively CSV files:
- `multi_select`: contains a CSV for each multiple select question
- `ranked`: contains a CSV for each rank by preference question

### JSON Converters
Files responsible for the conversion of JSON information into the necessary CSV.  Differences across surveys create a need (at least until more refactoring is possible) to have multiple classes inherit from a common abstract class, where a majority of the logic is held.  Here is the overall structure:
- Folders for each survey
- `__init__.py`: handles import logic
- `abstract_converter.py`: abstract class that contains logic shared by all json to csv converters

This is the structure for a survey folder:
- `__init__.py`: handles import logic
- `config.py`: stores configurations for the conversion
- `*_converter.py`: the instantiation of the abstract class with logic specific to the particular survey

### Response Coding Files
Files used for the analysis of response coding are found in the `response_coding` folder.  These files include:
- `comparer.py` which looks for differences between two sets of codings.  It generates a file `temp.csv` that marks an 'X' where a difference is detected.