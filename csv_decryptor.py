import pandas as pd
import aes_decryptor
import os
import sys
import argparse

def aes_decrypt_csv(encrypted_csv_path, list_columns_to_decrypt, secret_key):
    '''
    Decrypts columns of a csv using aes encryption algorithm
    '''
    #Read csv
    df = pd.read_csv(encrypted_csv_path)

    for col in list_columns_to_decrypt:
        #Get values in column
        col_values = df[col].tolist()

        #Create list of decrypted values
        decrypted_col_values = [aes_decryptor.decrypt(value, secret_key) \
                                for value in col_values]

        #Replace column by decryted values
        df[col] = decrypted_col_values

    #Save csv
    csv_path_no_extension = os.path.splitext(encrypted_csv_path)[0]
    decrypted_file_path = csv_path_no_extension+'_decrypted.csv'
    df.to_csv(decrypted_file_path)
    print(f'Decrypted file can be found in {decrypted_file_path}')

def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="CSV Decryptor")

    #Add arguments
    for (argument, arg_help, arg_type, arg_required) in [
           ('--encrypted_csv_path', 'Path to csv encrypted file', str, True),
           ('--list_of_columns_to_decrypt', 'List of columns to decrypt separated by commas', str, True),
           ('--secret_key', 'Secret key used to decrypt (AES algorithm)',str, True)]:

        parser.add_argument(
            argument,
            help=arg_help,
            default=None,
            required=arg_required,
            type=arg_type
        )

    return parser.parse_args()

def file_in_boxcryptor(file_path):
    if os.path.abspath(file_path)[0] == 'X':
        return True
    else:
        return False

if __name__=='__main__':

    args = parse_args()

    #Validate that input file is in X:
    csv_in_boxcryptor = file_in_boxcryptor(args.encrypted_csv_path)

    if not csv_in_boxcryptor:
        print(f'Your file to decrypt must be in Boxcryptor, please fix that and run again')
        sys.exit(1)

    aes_decrypt_csv(args.encrypted_csv_path, args.list_of_columns_to_decrypt.split(','), args.secret_key)
