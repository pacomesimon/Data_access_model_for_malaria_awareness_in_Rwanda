from flask import Flask, request, jsonify
from controllers import *
from config import cfg
from db_models import *
import json

# app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello world!"

@app.route("/tables/<table_name>", methods=['GET'])
def table_retrival(table_name):
    if (table_name in ["patient","case_cache","malaria_results",
                       "blood_test","health_center", 
                       "village","sector","cell",
                      "district","province"]): 
        return jsonify(table_querying(table_name=table_name,
                        columns_to_drop=[],
                        ).to_dict("index")), 200


@app.route("/tables/<table_name>/add", methods=['POST'])
def create_resource_endpoint(table_name):
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

    update_resource(resource_table_name=table_name,
                            id=id,)

    return jsonify({"response":"resource deleted"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=cfg["SERVER_PORT"])