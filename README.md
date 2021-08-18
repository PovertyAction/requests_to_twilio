# Intro

This repo has all necessary code to:

a) Start, directly from your computer, SMS or whatsapp surveys using twilio and,
b) Configure an encryption/decryption system to receive answers from twilio into Google Sheets.

For a), run `twilio_launcher.py` to launch the survey.

For b), you must know how to publish data from Twilio into Google sheets, you can learn about this in Chapter 6 of [this guide](https://drive.google.com/file/d/1Emxcbo10MaNHD8uYjI8o2zMkD031ynti/view).
  Please copy and paste the code in `twilio_encrypt_fields.js` as a twilio function, include all the responses you want to encrypt as parameters in the function widget.Use whatever name you want as key, as long as this name matches the name you are using inside the function (the "variable_to_encrypt" part of "event.variable_to_encrypt"), and modify the secret key (it must have 16 characters). This will hash the variables selected to encrypt.

Once the data is collected in your google sheet, download it in `.csv` format, and run `csv_decryptor.py` to create a decrypted version of your `.csv`. The file to decrypt must be in a Boxcryptor location for it to work. 

# Setup

1. Install python, pip and git

Use [this](https://phoenixnap.com/kb/how-to-install-python-3-windows) guide to install python3 on Windows.

The last versions of python have pip already installed (in the first guide it is explained how to check whether pip is installed), but just in case it is not: Use [this](https://www.liquidweb.com/kb/install-pip-windows/) to install pip.

For installing git on windows, use [this](https://phoenixnap.com/kb/how-to-install-git-windows)

2. Install Microsoft Visual C++ 14.0. Get it from "Build Tools for Visual Studio". To download, click [here](https://download.visualstudio.microsoft.com/download/pr/3e542575-929e-4297-b6c6-bef34d0ee648/639c868e1219c651793aff537a1d3b77/vs_buildtools.exe) and select options like explained [here](https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat/55575792#55575792). We will need this for the encryption libraries to install later.

3. Clone this repo inside Command Prompt(cmd) or, preferably, PowerShell. To open cmd or PowerShell, search in Start button from Windows.

`git clone https://github.com/PovertyAction/requests_to_twilio.git`

4. Install python dependencies in Powershell after getting into the right directory.

`cd requests_to_twilio` </br>
`pip install --upgrade setuptools` </br>
`pip install -r requirements.txt`

# How to run

## Launch surveys from your computer: Running twilio_launcher.py*

From the cmd or Powershell, run:

`python twilio_launcher.py --account_sid your_account_sid --account_token your_account_token --twilio_number your_twilio_number --flow_id flow_id --input_file full_path_to_input_file --batch_size batch_size --sec_between_batches sec_between_batches --columns_with_info_to_send name,full_name,month,year,survey_intro,city,job,caseid`

input_file.xlsx must have one column named `Number`, which contains the numbers we want to send messages to. It can also have any other amount of columns with info that we want to send to twilio.  In order to send info from those columns, include those columns names in the `columns_with_info_to_send` arguments, separated by commas.

## Encrypting and decrypting collected answers

This step is not required if your survey or workflow does not receive any PII. If it does, encryption is required before publishing into Gsheets. 
Inside Twilio, go to "functions/services/create service". There, click on "add function". Copy the code in "twilio_encrypt_fields.js" from this repository and paste it in a new function in twilio (you can delete what appears by default). You need to modify the secret_key and store it in a safe place in your computer, and also the amount and names of the variables you want to encrypt. 

Create  a  function  widget  in  your  Twilio  Studio  flow  just  before  the function  widget  that  publishes  to  Gsheets.  In  this  encryption  widget,  select  the service you created, select “ui” as environment, select the name of the function  you created  and  then  put  as  function  parameters  all  the  variables  that should be encrypted. For this, use the key that you want as variable names in the function code and use {{widgets.widget_name.inbound.Body}} as the values.
After this, in the function that publishes to Gsheets,  instead  of  using {{widgets.variable_name.inbound.Body}} as value, you will use {{widgets.name_of_your_encryption_widget.parsed.name_of_the_variable}}.

You will receive undecipherable strings for all the variables you send encrypted to Gsheets. Download this file and save it as .csv into a Boxcryptor location and then run the following code that will generate a decrypted version in the same path as the encrypted one: 
`python .\csv_decryptor.py --encrypted_csv_path X:\path\to\your\csv\demo.csv --list_of_columns_to_decrypt col1,col2 --secret_key your_secret_key1`

[DEPRECATED]
We used to collect answers from a raw_log file. We dont do this anymore cause the log file is not reliable. But if someone is still using this, here is how to call that script:

*Running logs_cleaner.py*

`python .\logs_cleaner.py --account_sid your_account_sid --account_token your_account_token --date_sent_after 2021-03-31T22:15:24Z --date_sent_before 2021-04-01T22:15:24Z --outputs_directory X:\Box\CP_Projects\path\to\folder --flow flow_name:"flow_a" twilio_number:whatsapp:+xxxxx questions_of_interest:intro1,lab_1,lab_2,lab_3 --flow flow_name:"flow_b" twilio_number:whatsapp:+xxxxx questions_of_interest:intro1,lab_1,lab_2,lab_3`

be careful to respect exact same format of inputs
outputs directory must be in boxcryptor (start with X:)
