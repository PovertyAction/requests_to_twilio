# Intro

Program to send SMS requests to twilio.

# Setup

1. Install python and pip

Use [this](https://phoenixnap.com/kb/how-to-install-python-3-windows) guide to install python3 on Windows. 

The last versions of python have pip already installed (in the first guide it is explained how to check whether pip is installed), but just in case it is not: Use [this](https://www.liquidweb.com/kb/install-pip-windows/) to install pip. 

2. Clone this repo inside Command Prompt(cmd) or, preferably, PowerShell. To open cmd or PowerShell, search in Start button from Windows.

`git clone https://github.com/PovertyAction/requests_to_twilio.git`

3. Install dependencies in Powershell after getting into the right directory.

`cd requests_to_twilio` </br>
`pip install -r requirements.txt`

## Twilio credentials

Please fill up `twilio_credentials_template.py`, and rename it as `twilio_credentials.py`. You have to open the file with any text editor (sublime or atom recommended)

# How to run

## Using python
From the cmd or Powershell, ask

`python twilio_launcher.py [input_file.xlsx] [batch_size] [seconds_between_batches]`

input_file.xlsx should have one column named 'Number', other columns may be added and piped into Twilio. Check out `input_example.xlsx`. If you add additional variables, you need to add them as well in the twilio_launcher.py code. 

## Using .exe

[Coming soon]
