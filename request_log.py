#!/usr/bin/env python
"""The Requests logger
DESCRIPTION:
------------
This file contains the scripts that logs incomming requests.
"""

import datetime
import json
import re
import config

# Declaration of the path to where logs are stored
REQUEST_LOGS_PATH = config.cfg["REQUEST_LOGS_PATH"]

def replace_non_numbers_with_underscore(input_string):
    """
    Replace non-digit characters in the input string with underscores.

    Args:
        input_string (str): The input string to process.

    Returns:
        str: The input string with non-digit characters replaced by underscores.
    """
    # Define the regex pattern to match non-digit characters
    non_digit_pattern = re.compile(r'\D')

    # Replace non-digit characters with underscores
    output_string = non_digit_pattern.sub('_', input_string)

    return output_string

def log(user_details_dict,request,columns_to_drop):
    """
    Log user activity and request details into a JSON file.

    Args:
        user_details_dict (dict): Dictionary containing user details.
        request: The request object with information about the current request.
        columns_to_drop (list): List of column names to be dropped from the request.

    Returns:
        None
    """
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
