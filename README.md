# Intro

Program to send SMS requests to twilio.

# Setup

1. Install python and pip

Use [this](https://phoenixnap.com/kb/how-to-install-python-3-windows) guide to install python3 on Windows.

Use [this](https://www.liquidweb.com/kb/install-pip-windows/) to install pip.

2. Clone this repo

`git clone https://github.com/PovertyAction/requests_to_twilio.git`

3. Install dependencies

`pip install -r requirements.txt`

## Twilio credentials

Please fill up `twilio_credentials_template.py`, and rename is as `twilio_credentials.py`.

# How to run

## Using python

`python twilio_launcher.py [input_file.xlsx] [batch_size] [seconds_between_batches]`

input_file.xlsx should only have one column named 'Number'. Check out `input_example.xlsx`.

## Using .exe

[Coming soon]
