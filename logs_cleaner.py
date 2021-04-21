import sys
import pandas as pd
import ftfy
import json
import os
from datetime import datetime
import argparse
import twilio_data_getter

FLOW_NAME = 'flowname'
TWILIO_NUMBER = 'whatsappnumber'
QUESTIONS_OF_INTEREST = 'questionsofinterest'


def get_similarity_score(string_a, string_b):

    def jaccard_similarity(string_a, string_b):
        intersection = set(string_a).intersection(set(string_b))
        union = set(string_a).union(set(string_b))

        return len(intersection)/len(union)

    #Could use other if they prove to be better here.
    return jaccard_similarity(string_a, string_b)

def get_question_code(questions_dict, message, pool_questions_to_consider=None):

    #Return code associated to message
    #If pool_questions_to_consider is not False, we will return code of question only as long as it belongs to pool_questions_to_consider

    #We know that messages sent might contain information extracted from flow.data, and hence, wont exactly be found in questions_dict (which has raw messages, which literally contain {{flow.data.xxx}}
    #Hence, our strategy is to look fo which question in questions_dict has the highest similarity score with message.

    best_question_code = None
    best_similarity_score = 0

    for q_code, q_message in questions_dict.items():
        similarity_score = get_similarity_score(q_message, message)

        if similarity_score > best_similarity_score:
            best_question_code = q_code
            best_similarity_score = similarity_score

    if pool_questions_to_consider is not None:
        if best_question_code in pool_questions_to_consider:

            # if similarity_score !=1:
            #     print('///')
            #     print(f'best_question_code: {best_question_code}')
            #     print(f'best_similarity_score: {best_similarity_score}')
            #     print('message')
            #     print(message)
            #     print('raw message')
            #     print(questions_dict[best_question_code])
            #     print('***')
            #     print('')

            return best_question_code
        else:
            return None
    else:
        return best_question_code


def clean_raw_data_df(raw_data_df):
    #Encode to utf-8
    raw_data_df['Body'] = raw_data_df['Body'].astype(str).apply(lambda x: ftfy.fix_text(x))

    return raw_data_df

# DEPRECATED
# def load_questions_dict(questions_json_path):
#
#     q_code_to_message_dict = {}
#
#     with open(questions_json_path, encoding="utf8") as questions_json_file:
#         questions_dict = json.load(questions_json_file)
#
#         flow_states = questions_dict['states']
#         for flow_state in flow_states:
#             if 'properties' in flow_state and 'body' in flow_state['properties']:
#                 q_code_to_message_dict[flow_state['name']] = ftfy.fix_text(flow_state['properties']['body'])
#
#     return q_code_to_message_dict

def load_questions_dict(flow_json):

    q_code_to_message_dict = {}

    flow_states = flow_json['definition']['states']
    for flow_state in flow_states:
        if 'properties' in flow_state and 'body' in flow_state['properties']:
            q_code_to_message_dict[flow_state['name']] = ftfy.fix_text(flow_state['properties']['body'])

    return q_code_to_message_dict


def compute_duration(question_sent_date, answer_sent_date):

    print(question_sent_date, answer_sent_date)

    def to_date_format(raw_date):
        return datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")

    duration = str(answer_sent_date - question_sent_date)

    return duration

def create_and_export_report(rows_list, output_file_name):

    if not os.path.exists('reports'):
        os.makedirs('reports')

    #Create df
    report_df = pd.DataFrame(rows_list)
    print(report_df)
    #Export
    report_df.to_csv(os.path.join('reports', output_file_name), index=False)



def create_reports(account_sid, auth_token, date_sent_after, date_sent_before, flows):

    log_data = twilio_data_getter.get_messages(
                                    account_sid=account_sid,
                                    auth_token=auth_token,
                                    date_sent_after_str=date_sent_after,
                                    date_sent_before_str=date_sent_before)

    print(log_data)

    #Create one report for each flow
    for flow in flows:

        output_file_name = f'{flow[FLOW_NAME]}_{date_sent_after}_{date_sent_before}.csv'

        create_clean_report(account_sid, auth_token, log_data, flow, output_file_name)



def create_clean_report(account_sid, auth_token, raw_data_df, flow, output_file_name):

    #Get flow parameters
    flow_friendly_name = flow[FLOW_NAME]
    twilio_number = flow[TWILIO_NUMBER]
    questions_to_consider = flow[QUESTIONS_OF_INTEREST].split(',')

    # raw_data_df = clean_raw_data_df(raw_data_df)

    flow_json = twilio_data_getter.get_flow_json(account_sid=account_sid,
                                        auth_token=auth_token,
                                        flow_friendly_name=flow_friendly_name)

    if flow_json is None:
        print('Couldnt find flow json')
        sys.exit(1)

    questions_dict = load_questions_dict(flow_json)
    print(questions_dict.keys())


    #Get list of phone_numbers
    phone_numbers = raw_data_df['from'].unique().tolist()

    #Remove twilio_number from phone_numbers
    if twilio_number not in phone_numbers:
        print(f'twilio number {twilio_number} not in list of phones found in data')
        sys.exit(1)

    phone_numbers.remove(twilio_number)

    #Track of rows of report
    answers_report_rows = []
    durations_report_rows = []

    for phone_number_index, phone_number in enumerate(phone_numbers):

        #Filter data to only messages sent to this sender or sent by this sender
        phone_number_df = raw_data_df[(raw_data_df['to'] == phone_number) | (raw_data_df['from'] == phone_number)]

        #Reset index to facilitate iteration
        phone_number_df.reset_index(inplace=True, drop=True)

        print('//')
        print(phone_number)
        print(phone_number_df[['from','to','body']])

        #Now we will traverse data related to this phone number buttom to top to reconstruct the conversation
        #Keep record of last seen question code and time sent
        last_question_code = None
        last_question_sent_date = None

        #Keep record of question and its answer and questions and their time-to-responde.
        #Dicts will help given that some questions will be asked more than once (when there are errors), so we can override them

        #First lets create empty dict with all keys, cause we want them all in the .csv output as columns
        question_to_answer = {}
        question_to_duration = {}

        for index, dict in enumerate([question_to_answer, question_to_duration]):
            dict['Number']=''
            #Add SentDate only to question_to_answer dict
            if index==0:
                dict['Last message date_sent']=''

            for q in questions_to_consider:
                dict[q]=''

            #Add number to dict
            dict['Number']=phone_number


        for index, row in phone_number_df[::-1].iterrows():
            sender = row['from']
            message = row['body']
            question_to_answer['Last message date_sent'] = str(row['datesent'])

            message_from_twilio = True if sender==twilio_number else False

            #Keep track of all answers to questions we care about
            if message_from_twilio:

                #Keep track of first message status by twilio
                if index+1 == phone_number_df.shape[0]:
                    question_to_answer['First message'] = get_question_code(questions_dict, message)
                    question_to_answer['Status first message'] = row['status']

                #Record answers and durations of ony questions_to_consider
                current_question_code = get_question_code(questions_dict, message, questions_to_consider)

                last_question_sent_date = row['datesent'] #Change for current_question_sent_date if we want to keep track of first time we asked question*

                #current_question_code will be none if it was not in the list of questions_to_consider
                if current_question_code is not None:
                    last_question_code = current_question_code

                    #Erase response for given question, case we have recorded it before (a bad answer)
                    question_to_answer[last_question_code]=''

                    #last_question_sent_date = current_question_sent_date. Uncomment if we want to keep track of first time we asked question*

                #Keep track of last message status by twilio
                question_to_answer['Last message code by twilio'] = get_question_code(questions_dict, message)
                question_to_answer['Last message by twilio'] = message
                question_to_answer['Status last message'] = row['status']

            else:
                if last_question_code is not None:
                    answer_sent_date = row['datesent']

                    #Save only first response to the question
                    if question_to_answer[last_question_code]=='':
                        question_to_answer[last_question_code] = message
                        question_to_duration[last_question_code] = compute_duration(last_question_sent_date, answer_sent_date)
                    else:
                        print(f'Participant response {message} will not be recorded because {last_question_code} already has a recorded answer: {question_to_answer[last_question_code]}')
                else:
                    print(f"WARNING: We are reading a user answer '{message}' from '{sender}', but did not kept record of to which question this answer responds. This is probably because you did not include the respective question code as one of your questions of interest when calling this script. Finishing program here")



        print(question_to_answer)
        answers_report_rows.append(question_to_answer)
        durations_report_rows.append(question_to_duration)

    for (rows_list, output_file_name) in [(answers_report_rows, f'{output_file_name}-answers.csv'),(durations_report_rows, f'{output_file_name}-durations.csv')]:
        create_and_export_report(rows_list, output_file_name)


def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Logs cleaner")

    parser.add_argument(
        "--account_sid",
        help="Twilio account SID",
        default=None,
        required=True,
        type=str
    )

    parser.add_argument(
        "--account_token",
        help="Twilio account token",
        default=None,
        required=True,
        type=str
    )

    parser.add_argument(
        "--date_sent_after",
        help="Only messages after this date will be considered",
        default=None,
        required=True,
        type=str
    )

    parser.add_argument(
        "--date_sent_before",
        help="Only messages before this date will be considered",
        default=None,
        required=True,
        type=str
    )

    parser.add_argument(
        "--flow",
        help="json_file:json_file_path whatsapp_number:whatsapp_number questions_of_interest:[q0,q1]",
        nargs='+',
        action='append',
        default=None,
        required=True,
        type=str
    )

    return parser.parse_args()

def parse_flows_data(list_flows, expected_flow_inputs = [FLOW_NAME, TWILIO_NUMBER, QUESTIONS_OF_INTEREST]):

    flows_data_dicts = []

    for flow_inputs in list_flows:

        #Structured way of keeping flow data
        flow_data_dict = {}

        #Validate that flow_inputs are the necessary
        # jsonfile:a whatsappnumber:1 questionsofinterest:[3,5]
        if len(flow_inputs)!=3:
            print('Each flow_input should have 3 arguments (jsonfile:xxx, whatsappnumber:xxx, questionsofinterest:xxx')
            sys.exit(1)

        for flow_input in flow_inputs:
            if not ':' in flow_input:
                print('flow_inputs should be specified as key:value')
                sys.exit(1)

            flow_input_k = flow_input.split(':')[0]
            flow_input_v = ':'.join(flow_input.split(':')[1:])

            if not flow_input_k in expected_flow_inputs:
                print(f'{flow_input_k} should be one of the following: jsonfile, whatsappnumber, questionsofinterest')
                sys.exit(1)

            flow_data_dict[flow_input_k] = flow_input_v

        flows_data_dicts.append(flow_data_dict)

    return flows_data_dicts



#python .\logs_cleaner.py --account_sid 1 --account_token 2 --date_sent_after 1 --date_sent_before 2 --flow jsonfile:a whatsappnumber:1 questionsofinterest:q0,q1
if __name__=='__main__':

    args = parse_args()

    flows = parse_flows_data(args.flow)

    create_reports(account_sid=args.account_sid,
                        auth_token=args.account_token,
                        date_sent_after=args.date_sent_after,
                        date_sent_before=args.date_sent_before,
                        flows=flows)
