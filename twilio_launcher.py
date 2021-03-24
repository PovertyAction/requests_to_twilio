import requests
import json
import pandas as pd
import sys
import os
import time
import twilio_credentials
from datetime import datetime

def launch_twilio_messages(input_file, batch_size, sec_between_batches):
    #Read excel
    phones_df = pd.read_excel(input_file)

    #Add empty columns
    for column_to_add in ['status_code', 'Date', 'Status', 'Execution', 'Contact', 'Url']:
        phones_df[column_to_add] = ""

    #Get twilio credentials
    account_sid = twilio_credentials.get_account_sid()
    account_token = twilio_credentials.get_account_token()
    from_number = twilio_credentials.get_twilio_number()
    flow_id = twilio_credentials.get_flow_id()

    #Build api url
    twilio_api_url = "https://studio.twilio.com/v1/Flows/" + flow_id + "/Executions"

    #Iterate through numbers in df and send a post request for each
    #Do this in batches
    messages_sent_in_this_batch = 0

    for index, row in phones_df.iterrows():

        to_number = str(row['Number'])
        request_payload = {'To': to_number, 'From': from_number}

        response = requests.post(twilio_api_url, data=request_payload, auth=(account_sid, account_token))

        response_json = json.loads(response.text)

        phones_df.at[index, 'status_code'] = response.status_code

        if response.status_code == 200:
            phones_df.at[index,'Date'] = datetime.now()
            phones_df.at[index,'Status'] = response_json['status']
            phones_df.at[index,'Execution'] = response_json['sid']
            phones_df.at[index,'Contact'] = response_json['contact_channel_address']
            phones_df.at[index,'Url'] = response_json['url']

        messages_sent_in_this_batch += 1

        #Sleep every time we finish a batch
        if messages_sent_in_this_batch == batch_size:
            print(f'Batch finished, sleeping for {sec_between_batches}')
            time.sleep(sec_between_batches)
            messages_sent_in_this_batch = 0

    #Output file
    dir_path = os.path.dirname(os.path.realpath(input_file))
    input_file_basename = os.path.basename(input_file)
    input_file_name, input_file_extension = os.path.splitext(input_file_basename)
    output_file_basename = input_file_name+"_output"+input_file_extension
    output_file = os.path.join(dir_path, output_file_basename)

    #Save df
    phones_df.to_excel(output_file, index=False)

    print(phones_df)
    print(f'Result written to: {output_file}')


if __name__=='__main__':
    input_file = sys.argv[1]
    batch_size = int(sys.argv[2])
    sec_between_batches = int(sys.argv[3])
    launch_twilio_messages(input_file, batch_size, sec_between_batches)
