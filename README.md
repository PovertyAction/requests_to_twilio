# Intro

This repo has all necessary code to:

a) Start SMS or whatsapp surveys using twilio
b) Collect answers from twilio

For a), run `twilio_launcher.py` to launch the survey.

For b), please include the code in `twilio_encrypt_fields.js` in your twilio widget that will send the data to gsheets. Remember to modify the `secret_key` in the first lines of the file, as well as `variable_to_encrypt`. This will send all collected answers to a google sheet, hashing variables selected to encrypt.

Once the data is collected in your google sheet, download it in `.csv` format, and run `csv_decryptor.py` to create a decrypted version of your `.csv`.

# Setup

1. Install python and pip

Use [this](https://phoenixnap.com/kb/how-to-install-python-3-windows) guide to install python3 on Windows.

The last versions of python have pip already installed (in the first guide it is explained how to check whether pip is installed), but just in case it is not: Use [this](https://www.liquidweb.com/kb/install-pip-windows/) to install pip.

2. Install Microsoft Visual C++ 14.0. Get it from "Build Tools for Visual Studio". To download, click [here](https://download.visualstudio.microsoft.com/download/pr/3e542575-929e-4297-b6c6-bef34d0ee648/639c868e1219c651793aff537a1d3b77/vs_buildtools.exe) and select options like explained [here](https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat/55575792#55575792). We will need this for the encryption libraries to install later.

3. Clone this repo inside Command Prompt(cmd) or, preferably, PowerShell. To open cmd or PowerShell, search in Start button from Windows.

`git clone https://github.com/PovertyAction/requests_to_twilio.git`

4. Install python dependencies in Powershell after getting into the right directory.

`cd requests_to_twilio` </br>
`pip install --upgrade setuptools` </br>
`pip install -r requirements.txt`

# How to run

## Sending surveys: Running twilio_launcher.py*

From the cmd or Powershell, run:

`python twilio_launcher.py --account_sid your_account_sid --account_token your_account_token --twilio_number your_twilio_number --flow_id flow_id --input_file full_path_to_input_file --batch_size batch_size --sec_between_batches sec_between_batches --columns_with_info_to_send name,full_name,month,year,survey_intro,city,job,caseid`

input_file.xlsx must have one column named `Number`, which contains the numbers we want to send messages to. It can also have any other amount of columns with info that we want to send to twilio.  In order to send info from those columns, include those columns names in the `columns_with_info_to_send` arguments, separated by commas.

## Collecting answers

[@Carlos, add instructions on adding .js code to twilio widget]

`python .\csv_decryptor.py --encrypted_csv_path X:\path\to\your\csv\demo.csv --list_of_columns_to_decrypt col1,col2 --secret_key your_secret_key1`

[DEPRECATED]
We used to collect answers from a raw_log file. We dont do this anymore cause the log file is not reliable. But if someone is still using this, here is how to call that script:

*Running logs_cleaner.py*

`python .\logs_cleaner.py --account_sid your_account_sid --account_token your_account_token --date_sent_after 2021-03-31T22:15:24Z --date_sent_before 2021-04-01T22:15:24Z --outputs_directory X:\Box\CP_Projects\path\to\folder --flow flow_name:"flow_a" twilio_number:whatsapp:+xxxxx questions_of_interest:intro1,lab_1,lab_2,lab_3 --flow flow_name:"flow_b" twilio_number:whatsapp:+xxxxx questions_of_interest:intro1,lab_1,lab_2,lab_3`

be careful to respect exact same format of inputs
outputs directory must be in boxcryptor (start with X:)
