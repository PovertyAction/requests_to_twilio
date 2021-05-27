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

2. Clone this repo inside Command Prompt(cmd) or, preferably, PowerShell. To open cmd or PowerShell, search in Start button from Windows.

`git clone https://github.com/PovertyAction/requests_to_twilio.git`

3. Install dependencies in Powershell after getting into the right directory.

`cd requests_to_twilio` </br>
`pip install -r requirements.txt`

# How to run

## Sending surveys: Running twilio_launcher.py*

From the cmd or Powershell, run:

`python twilio_launcher.py --account_sid your_account_sid --account_token your_account_token --twilio_number your_twilio_number --flow_id flow_id --input_file full_path_to_input_file --batch_size batch_size --sec_between_batches sec_between_batches --columns_with_info_to_send name,full_name,month,year,survey_intro,city,job,caseid`

input_file.xlsx must have one column named `Number`, which contains the numbers we want to send messages to. It can also have any other amount of columns with info that we want to send to twilio.  In order to send info from those columns, include those columns names in the `columns_with_info_to_send` arguments, separated by commas.

## Collecting answers: Running twilio_launcher.py*

[@Carlos, add instructions on adding .js code to twilio widget]

`python .\csv_decryptor.py --encrypted_csv_path C:\path\to\your\csv\demo.csv --list_of_columns_to_decrypt col1,col2 --secret_key your_secret_key1`
