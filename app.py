#!/usr/bin/env python
"""The router
DESCRIPTION:
------------
This file contains routes to the server side."""

from flask import request, jsonify
from controllers import *
from config import cfg
from db_models import *
from authentication import authentication_function
import request_log

@app.route("/", methods=['GET'])
def hello_world():
    """
    Return a formatted welcome message as an HTML string.

    Returns:
        str: HTML string containing a welcome message.
    """
    return """
    <h1>Hello world! </h1>  <!-- Display a header with the welcome message -->
    Welcome to the Data Access System
    for Malaria Awareness in Rwanda!  <!-- Display a descriptive welcome message -->
    """

@app.route("/tables/<table_name>", methods=['GET'])
def table_retrival(table_name):
    """
    Retrieve data from a specified table based on user authentication and role.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response contains the retrieved data as a dictionary or an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the specified table name is valid
    if table_name not in ["patient", "case_cache", "malaria_results",
                          "blood_test", "health_center",
                          "village", "sector", "cell",
                          "district", "province"]:
        return jsonify({"error": "table not found"}), 404

    # Determine columns to drop based on user role
    if user_details.role not in ["health_worker", "sys_admin"]:
        columns_to_drop = ["name"]
    else:
        columns_to_drop = []

    # Log user activity and request details
    request_log.log(user_details_dict, request, columns_to_drop)

    # Retrieve and return the queried table data as JSON
    return jsonify(
        table_querying(table_name=table_name, columns_to_drop=columns_to_drop).to_dict("index")
    ), 200


@app.route("/tables/<table_name>/timefilter", methods=['GET'])
def table_retrival_timefilter(table_name):
    """
    Retrieve data from a specified table based on user authentication, role, and time filters.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response contains the retrieved data as a dictionary or an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the specified table name is valid for this endpoint
    if table_name not in ["case_cache", "blood_test"]:
        return jsonify({"error": "table cannot be found on this endpoint"}), 404

    # Determine columns to drop based on user role
    if user_details.role not in ["health_worker", "sys_admin"]:
        columns_to_drop = ["name"]
    else:
        columns_to_drop = []

    # Check the content type of the request
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()

            # Log user activity and request details
            request_log.log(user_details_dict, request, columns_to_drop)

            # Retrieve and return the queried table data with datetime filters as JSON
            return jsonify(
                table_querying_with_datetime_filters(
                    early_date=json_data["early_date"],
                    late_date=json_data["late_date"],
                    table_name=table_name,
                    columns_to_drop=columns_to_drop
                ).to_dict("index")
            ), 200
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': 'Invalid JSON data'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400


@app.route("/tables/<table_name>/sampling", methods=['GET'])
def online_querying_api(table_name):
    """
    Retrieve data from a specified table using online querying with batch processing and user authentication.

    Args:
        table_name (str): The name of the table to retrieve data from.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response contains the retrieved data as a dictionary or an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the specified table name is valid
    if table_name not in ["patient", "case_cache", "malaria_results",
                          "blood_test", "health_center",
                          "village", "sector", "cell",
                          "district", "province"]:
        return jsonify({"error": "table not found"}), 404

    # Determine columns to drop based on user role
    if user_details.role not in ["health_worker", "sys_admin"]:
        columns_to_drop = ["name"]
    else:
        columns_to_drop = []

    # Check if the content type is JSON
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()

            # Perform online querying with batch processing
            results = online_querying(
                table_name=table_name,
                batch_size=json_data["batch_size"],
                previous_indexes=json_data["previous_indexes"],
                columns_to_drop=columns_to_drop
            )

            # If the status code is 200, format the data dictionary
            if results["status"] == 200:
                results["data"] = results["data"].to_dict("index")

            # Log user activity and request details
            request_log.log(user_details_dict, request, columns_to_drop)

            # Return the results and corresponding status code
            return jsonify(results), results["status"]
        
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': 'Invalid JSON data'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400

@app.route("/tables/<table_name>/<column_name>/<key>", methods=['GET'])
def entry_retrival(table_name, column_name, key):
    """
    Retrieve entries from a specified table based on user authentication, role, and key.

    Args:
        table_name (str): The name of the table to retrieve entries from.
        column_name (str): The name of the column to use as the key for querying.
        key: The value of the key to search for in the specified column.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response contains the retrieved entries as a dictionary or an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the user has appropriate role for this operation
    if user_details.role not in ["health_worker", "sys_admin"]:
        return jsonify({"response": "unauthorized"}), 401

    # Check if the specified table name is valid
    if table_name not in ["patient", "case_cache", "malaria_results",
                          "blood_test", "health_center",
                          "village", "sector", "cell",
                          "district", "province"]:
        return jsonify({"error": "table not found"}), 404

    # Log user activity and request details
    request_log.log(user_details_dict, request, [])

    # Retrieve and return the queried entries as JSON
    return jsonify(
        entries_querying(key=key, table_name=table_name, key_column=column_name).to_dict("index")
    ), 200

@app.route("/tables/<table_name>/create", methods=['POST'])
def create_resource_endpoint(table_name):
    """
    Create a resource in a specified table based on user authentication, role, and request data.

    Args:
        table_name (str): The name of the table to create a resource in.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response confirms resource creation or returns an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the user has appropriate role for this operation
    if user_details.role not in ["health_worker", "sys_admin"]:
        return jsonify({"response": "unauthorized"}), 401

    # Check if the user's role and the table name are compatible
    if user_details.role == "health_worker" and table_name not in ["patient", "blood_test", "malaria_results"]:
        return jsonify({"response": "unauthorized"}), 401

    # Check if the content type is JSON
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()

            # Create the resource using specified details
            create_resource(resource_table_name=table_name, details_dict=json_data)
            
            # Log user activity and request details
            request_log.log(user_details_dict, request, [])

            return jsonify({"response": "resource created"}), 201
        
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': f'Invalid JSON data, {e}'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400

@app.route("/tables/<table_name>/update/<id>", methods=['PUT','PATCH'])
def update_resource_endpoint(table_name, id):
    """
    Update a resource in a specified table based on user authentication, role, resource ID, and request data.

    Args:
        table_name (str): The name of the table to update a resource in.
        id: The ID of the resource to be updated.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response confirms resource update or returns an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the user has appropriate role for this operation
    if user_details.role not in ["sys_admin"]:
        return jsonify({"response": "unauthorized"}), 401

    # Check if the content type is JSON
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()

            # Update the resource using specified details and ID
            update_resource(resource_table_name=table_name, id=id, details_dict=json_data)
            
            # Log user activity and request details
            request_log.log(user_details_dict, request, [])

            return jsonify({"response": "resource updated"}), 201
        
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': f'Invalid JSON data, {e}'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400

@app.route("/tables/<table_name>/delete/<id>", methods=['DELETE'])
def delete_resource_endpoint(table_name, id):
    """
    Delete a resource from a specified table based on user authentication, role, and resource ID.

    Args:
        table_name (str): The name of the table to delete a resource from.
        id: The ID of the resource to be deleted.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
               The JSON response confirms resource deletion or returns an error message.
    """
    # Authenticate user and handle authentication errors
    auth_results = authentication_function()
    if auth_results["error"]:
        return jsonify(auth_results), 400

    # Extract user details from authentication results
    user_details = auth_results["response"]
    user_details_dict = vars(user_details).copy()

    # Check if the user has appropriate role for this operation
    if user_details.role not in ["sys_admin"]:
        return jsonify({"response": "unauthorized"}), 401

    try:
        # Delete the resource using specified table name and ID
        delete_resource(resource_table_name=table_name, id=id)
    except Exception as e:
        # If there is an error in the deletion process, return an error response
        return jsonify({'error': f'error in deletion process: {e}'}), 400
    
    # Log user activity and request details
    request_log.log(user_details_dict, request, [])

    return jsonify({"response": "resource deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=cfg["SERVER_PORT"])