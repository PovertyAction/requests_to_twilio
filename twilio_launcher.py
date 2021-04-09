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
    twilio_api_url = "https://studio.twilio.com/v2/Flows/" + flow_id + "/Executions"

    #Iterate through numbers in df and send a post request for each
    #Do this in batches
    messages_sent_in_this_batch = 0

    for index, row in phones_df.iterrows():

        to_number = str(row['Number'])
        #Create additional variables for piping into twilio (Customize as needed)
        partic_name = str(row["name"])
        partic_month = str(row["month"])
        partic_year = str(row["year"])
        partic_survey_intro = str(row["survey_intro"])
        partic_city = str(row["city"])
        partic_job = str(row["job"])
        partic_full_name = str(row["full_name"])
        #Create parameter variable that compiles all the extra variables to be piped in. 
        parameters_1={"name":partic_name,"month":partic_month,"year":partic_year,"survey_intro":partic_survey_intro,"city":partic_city,"job":partic_job,"full_name":partic_full_name}
        #When sending the additional variables to Twilio, they need to be strings in json. 
        request_payload = {'To': to_number, 'From': from_number, 'Parameters':json.dumps(parameters_1)}
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


if __name__=='__main__':
    input_file = sys.argv[1]
    batch_size = int(sys.argv[2])
    sec_between_batches = int(sys.argv[3])
    launch_twilio_messages(input_file, batch_size, sec_between_batches)
