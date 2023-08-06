from flask import request, jsonify
from controllers import *
from config import cfg
from db_models import *
from authentication import authentication_function


@app.route("/", methods=['GET'])
def hello_world():
    return """
    <h1>Hello world! </h1>
    Welcome to the Data Access System
    for Malaria Awareness in Rwanda!
    """

@app.route("/tables/<table_name>", methods=['GET'])
def table_retrival(table_name):

    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (table_name not in ["patient","case_cache","malaria_results",
                       "blood_test","health_center", 
                       "village","sector","cell",
                      "district","province"]):
        return jsonify({"error":"table not found"}), 404
    
    if (user_details.role not in ["health_worker","sys_admin"]):
        columns_to_drop=["name"]
    else:
        columns_to_drop=[]
    return jsonify(table_querying(table_name=table_name,
                        columns_to_drop=columns_to_drop,
                        ).to_dict("index")), 200
    

@app.route("/tables/<table_name>/timefilter", methods=['GET'])
def table_retrival_timefilter(table_name):

    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (table_name not in ["case_cache","blood_test"]):
        return jsonify({"error":"table cannot be found on this endpoint"}), 404
    
    if (user_details.role not in ["health_worker","sys_admin"]):
        columns_to_drop=["name"]
    else:
        columns_to_drop=[]

    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()

            return jsonify(table_querying_with_datetime_filters(
                early_date=json_data["early_date"],
                late_date=json_data["late_date"],
                table_name=table_name,
                columns_to_drop=columns_to_drop
                        ).to_dict("index")), 200
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': 'Invalid JSON data'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400



@app.route("/tables/<table_name>/sampling", methods=['GET'])
def online_querying_api(table_name):

    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (table_name not in ["patient","case_cache","malaria_results",
                       "blood_test","health_center", 
                       "village","sector","cell",
                      "district","province"]):
        return jsonify({"error":"table not found"}), 404
    
    if (user_details.role not in ["health_worker","sys_admin"]):
        columns_to_drop=["name"]
    else:
        columns_to_drop=[]

        # Check if the content type is JSON
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()
    
            results = online_querying(
                table_name=table_name,
                batch_size=json_data["batch_size"],
                previous_indexes=json_data["previous_indexes"],
                columns_to_drop=columns_to_drop
                    )
            if (results["status"]==200):
                results["data"]= results["data"].to_dict("index")
            return jsonify(results), results["status"]
        
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': 'Invalid JSON data'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400

@app.route("/tables/<table_name>/<column_name>/<key>", methods=['GET'])
def entry_retrival(table_name,column_name,key):

    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (user_details.role not in ["health_worker","sys_admin"]):
        return jsonify({"response":"unauthorized"}), 401
    
    if (table_name not in ["patient","case_cache","malaria_results",
                       "blood_test","health_center", 
                       "village","sector","cell",
                      "district","province"]):
        return jsonify({"error":"table not found"}), 404
    
    return jsonify(entries_querying(key=key,table_name=table_name,
                        key_column=column_name,
                        ).to_dict("index")), 200


@app.route("/tables/<table_name>/add", methods=['POST'])
def create_resource_endpoint(table_name):
    
    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (user_details.role not in ["health_worker","sys_admin"]):
        return jsonify({"response":"unauthorized"}), 401
    if (user_details.role=="health_worker") and (table_name not in ["patient","blood_test","malaria_results"]):
        return jsonify({"response":"unauthorized"}), 401
# Check if the content type is JSON
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()
            create_resource(resource_table_name=table_name,
                            details_dict = json_data)

            return jsonify({"response":"resource created"}), 201
        
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': 'Invalid JSON data'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400

@app.route("/tables/<table_name>/update/<id>", methods=['PUT','PATCH'])
def update_resource_endpoint(table_name,id):
    
    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (user_details.role not in ["sys_admin"]):
        return jsonify({"response":"unauthorized"}), 404
# Check if the content type is JSON
    if request.content_type == 'application/json':
        try:
            # Access the JSON data from the request body
            json_data = request.get_json()
            update_resource(resource_table_name=table_name,
                            id=id,
                            details_dict = json_data)

            return jsonify({"response":"resource updated"}), 201
        
        except Exception as e:
            # If there is an error parsing the JSON data, return an error response
            return jsonify({'error': 'Invalid JSON data'}), 400
    
    # If the content type is not JSON, return an error response
    return jsonify({'error': 'Invalid content type. Expected JSON data.'}), 400

@app.route("/tables/<table_name>/delete/<id>", methods=['DELETE'])
def delete_resource_endpoint(table_name,id):
    
    auth_results = authentication_function()
    if(auth_results["error"]):
        return jsonify(auth_results), 400
    user_details = auth_results["response"]

    if (user_details.role not in ["sys_admin"]):
        return jsonify({"response":"unauthorized"}), 404
    delete_resource(resource_table_name=table_name,
                            id=id,)

    return jsonify({"response":"resource deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=cfg["SERVER_PORT"])