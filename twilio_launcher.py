import requests
import json
import pandas as pd
import sys
import os
import time
from datetime import datetime
import argparse

def launch_twilio_messages(account_sid, account_token, twilio_number, flow_id, input_file, batch_size, sec_between_batches, columns_with_info_to_send):

    #Read excel
    phones_df = pd.read_excel(input_file)

    #Add empty columns to df to start generating ouput
    for column_to_add in ['status_code', 'Date', 'Status', 'Execution', 'Contact', 'Url']:
        phones_df[column_to_add] = ""

    #Build api url
    twilio_api_url = "https://studio.twilio.com/v2/Flows/" + flow_id + "/Executions"

    #Iterate through numbers in df and send a post request for each
    #Do this in batches
    messages_sent_in_this_batch = 0

    for index, row in phones_df.iterrows():

        to_number = str(row['Number'])

        #Create dictionary with additional variables to send to twilio
        parameters={}
        for c in columns_with_info_to_send:
            parameters[c]=str(row[c])

        #When sending the additional variables to Twilio, they need to be strings in json.
        request_payload = {'To': to_number, 'From': twilio_number, 'Parameters':json.dumps(parameters)}

        #The following print helps you see what you are sending to Twilio
        print(request_payload)
        response = requests.post(twilio_api_url, data=request_payload, auth=(account_sid, account_token))
        print(response)
        print(response.content)
        response_json = json.loads(response.text)

        phones_df.at[index, 'status_code'] = response.status_code

        if response.status_code == 200 or response.status_code == 201:
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

def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Twilio launcher")

    #Add arguments
    for (argument, arg_help, arg_type, arg_required) in [
           ('--account_sid', 'Twilio account SID', str, True),
           ('--account_token', 'Twilio account token', str, True),
           ('--twilio_number', 'Twilio phone number',str, True),
           ('--flow_id','Flow id to which to send the messages', str, True),
           ('--input_file','Path to file with inputs',str, True),
           ('--batch_size','Batch size',int, True),
           ('--sec_between_batches','Seconds between batches',int, True),
           ('--columns_with_info_to_send','Columns from input file that we want to be included in message to twilio, separated by commas',str, False)]:

        parser.add_argument(
            argument,
            help=arg_help,
            default=None,
            required=arg_required,
            type=arg_type
        )

    return parser.parse_args()

if __name__=='__main__':

    args = parse_args()


    launch_twilio_messages(account_sid = args.account_sid,
                            account_token = args.account_token,
                            twilio_number = args.twilio_number,
                            flow_id = args.flow_id,
                            input_file = args.input_file,
                            batch_size = args.batch_size,
                            sec_between_batches = args.sec_between_batches,
                            columns_with_info_to_send = args.columns_with_info_to_send.split(','))
