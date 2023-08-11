import datetime
import json
import os
import re
import config

REQUEST_LOGS_PATH = config.cfg["REQUEST_LOGS_PATH"]

def replace_non_numbers_with_underscore(input_string):
    # Define the regex pattern to match non-digit characters
    non_digit_pattern = re.compile(r'\D')

    # Replace non-digit characters with underscores
    output_string = non_digit_pattern.sub('_', input_string)

    return output_string

def log(user_details_dict,request,columns_to_drop):
    print(user_details_dict)
    user_details_dict.pop('_sa_instance_state')
    request_dictionary=vars(request).copy()
    request_dictionary = {key:str(val) for (key,val) in request_dictionary.items()}
    timestamp=str(datetime.datetime.now())
    json_log_data = json.dumps(([
                    {"timestamp":timestamp},
                    {"user_details":user_details_dict},
                    {"request":request_dictionary},
                    {"columns_to_drop":columns_to_drop}
                ])
                , indent = 8) 

    # Writing to a json file
    json_file_path = f"{REQUEST_LOGS_PATH}{replace_non_numbers_with_underscore(timestamp)}{'.json'}"
    with open(json_file_path, "a+") as outfile:
        outfile.write(json_log_data)
