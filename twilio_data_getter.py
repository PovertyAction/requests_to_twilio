import os
from twilio.rest import Client
from datetime import datetime
import json
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth


#Reference: https://www.twilio.com/docs/sms/api/message-resource?code-sample=code-read-list-messages-filter-by-a-period-of-time&code-language=Python&code-sdk-version=6.x


def get_messages(account_sid, auth_token, date_sent_after_str, date_sent_before_str):
    client = Client(account_sid, auth_token)


    date_sent_after = datetime.strptime(date_sent_after_str, '%Y-%m-%dT%H:%M:%SZ')
    date_sent_before = datetime.strptime(date_sent_before_str, '%Y-%m-%dT%H:%M:%SZ')

    print(f'date_sent_after: {date_sent_after}')
    print(f'date_sent_before: {date_sent_before}')

    messages = client.messages.list(date_sent_after=date_sent_after,
                                   date_sent_before=date_sent_before)

    clean_messages = []
    for message in messages:
        clean_message={}

        for key in ['from_','to','body','status','date_sent']:
            clean_message[key.replace('_','')]= message._properties[key]

        clean_messages.append(clean_message)



    return pd.DataFrame(clean_messages)


# get_messages(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
def get_flow_json(account_sid, auth_token, flow_friendly_name):

    client = Client(account_sid, auth_token)

    #Get all flows
    flows = client.studio.flows.list()

    #Look for flow with given friendly_name
    for record in flows:
        if record.friendly_name == flow_friendly_name:
            #Query flow url
            response = requests.get(record.url, auth = HTTPBasicAuth(account_sid, auth_token))
            #Parse to json and return
            # print(json.loads(response.text))
            return json.loads(response.text)
    return None
