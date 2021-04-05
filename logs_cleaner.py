import sys
import pandas as pd
import ftfy


def get_question_code(questions_df, message):

    question_code_serie = questions_df[questions_df['Question message']==message]['Question code']

    if question_code_serie.shape[0]>0:
        question_code = question_code_serie.iloc[0]
    else:
        question_code = None
        print(f'Couldnt find question code for {message}')

    return question_code

def get_question_message(questions_df, question_code):

    question_message_serie = questions_df[questions_df['Question code']==question_code]['Question message']

    if question_message_serie.shape[0]>0:
        question_message = question_message_serie.iloc[0]
    else:
        question_message = None
        print(f'Couldnt find question message for {question_code}')

    return question_message


def clean_questions_df(questions_df):

    #Remove any {..} from messages
    questions_df['Question message'] = questions_df['Question message'].map(lambda x: x.replace('{{flow.data.name_1}}', ''))

    return questions_df

def clean_raw_data_df(raw_data_df):
    #Encode to utf-8
    raw_data_df['Body'] = raw_data_df['Body'].astype(str).apply(lambda x: ftfy.fix_text(x))

    #Fix sorting by date, so that if theres 2 messages with same date, they show up interchanged (so that it doesnt happen two twilio message come together).

    #We assume dates are already sorted

    return raw_data_df


def create_clean_report(input_file, twilio_number, whatsapp):

    raw_data_df = clean_raw_data_df(pd.read_excel(input_file))
    questions_df = clean_questions_df(pd.read_excel(input_file, sheet_name=1))


    #Get list of phone_numbers
    phone_numbers = raw_data_df['From'].unique().tolist()

    #Remove twilio_number from phone_numbers
    phone_numbers.remove(twilio_number)

    #Track of rows of report
    report_rows = []

    for phone_number_index, phone_number in enumerate(phone_numbers):

        print(phone_number)

        #Filter data to only messages sent to this sender or sent by this sender
        phone_number_df = raw_data_df[(raw_data_df['To'] == phone_number) | (raw_data_df['From'] == phone_number)]

        #Reset index to facilitate iteration
        phone_number_df.reset_index(inplace=True)

        #Now we will traverse data related to this phone number buttom to top to reconstruct the conversation
        #Keep record of last seen question code
        last_question_code = None

        # if phone_number =='whatsapp:+573103085897':
        print('phone_number_df')
        print(phone_number_df[['From','To','Body','SentDate']])

        #Keep record of question and its answer. Dict will help given that some questions will be asked more than once (when there are errors), so we can override them
        question_to_answer = {}
        question_to_answer['number']=phone_number

        for index, row in phone_number_df[::-1].iterrows():
            sender = row['From']
            message = row['Body']
            date = row['SentDate']
            question_to_answer['date']=date

            message_from_twilio = True if sender==twilio_number else False

            if message_from_twilio:
                this_question_code = get_question_code(questions_df, message)
                if this_question_code is not None:
                    last_question_code = this_question_code
            else:
                last_question_message = get_question_message(questions_df, last_question_code)
                question_to_answer[last_question_code] = message


        print(question_to_answer)
        report_rows.append(question_to_answer)

    report_df = pd.DataFrame(report_rows)
    print(report_df)
    #Export
    report_df.to_csv('clean_log.csv', index=False)


if __name__=='__main__':
    input_file = sys.argv[1]
    twilio_number = sys.argv[2]
    whatsapp = True#True if sys.argv[3] == '1' else False
    create_clean_report(input_file, twilio_number, whatsapp)
