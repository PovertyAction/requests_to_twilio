# Intro

This repo has 2 files.
1. twilio_launcher.py: Program to send SMS requests to twilio.
2. logs_cleaner.py: Program to transform raw twilio data form survey responses to a desired output.

# Setup

1. Install python and pip

Use [this](https://phoenixnap.com/kb/how-to-install-python-3-windows) guide to install python3 on Windows.

The last versions of python have pip already installed (in the first guide it is explained how to check whether pip is installed), but just in case it is not: Use [this](https://www.liquidweb.com/kb/install-pip-windows/) to install pip.

2. Clone this repo inside Command Prompt(cmd) or, preferably, PowerShell. To open cmd or PowerShell, search in Start button from Windows.

`git clone https://github.com/PovertyAction/requests_to_twilio.git`

3. Install dependencies in Powershell after getting into the right directory.

`cd requests_to_twilio` </br>
`pip install -r requirements.txt`

# How to run

## Using python

*Running twilio_launcher.py*

From the cmd or Powershell, run:

`python twilio_launcher.py [input_file.xlsx] [batch_size] [seconds_between_batches]`

`python twilio_launcher.py --account_sid your_account_sid --account_token your_account_token --twilio_number your_twilio_number --flow_id flow_id --input_file full_path_to_input_file --batch_size batch_size --sec_between_batches sec_between_batches --columns_with_info_to_send name,full_name,month,year,survey_intro,city,job,caseid`


input_file.xlsx should have one column named 'Number', and all other columns specified as inputs (columns_with_info_to_send). Check out `input_example.xlsx` for an example.

*Running logs_cleaner.py*

`python logs_cleaner.py [raw_log_data.xlsx] [questions_data.json] [questions_to_consider_separated_by_commas] [twilio_number]`

*Running logs_cleaner.py*

`python logs_cleaner.py [raw_log_data.xlsx] [questions_data.json] [questions_to_consider_separated_by_commas] [twilio_number]`

## Using .exe

[Coming soon]
