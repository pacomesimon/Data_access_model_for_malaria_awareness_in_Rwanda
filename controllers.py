#!/usr/bin/env python
"""The Controllers functions' source code
DESCRIPTION:
------------
This file contains the controllers functions' source code.
Controllers are defined as the functions that interact directly with the database.
"""

import db_models
import pandas as pd
import numpy as np
import db_helpers
import datetime

def table_querying(table_name="case_cache",
                   columns_to_drop=["name"],
                   ):
    """
    Retrieve records from the specified table, convert them to a DataFrame,
    and drop specified columns from the resulting DataFrame.

    Args:
        table_name (str, optional): The name of the table to query. Defaults to "case_cache".
        columns_to_drop (list, optional): A list of column names to drop from the DataFrame. Defaults to ["name"].

    Returns:
        pandas.DataFrame: A DataFrame containing the queried records with specified columns dropped.
    """
    # Query the specified table using db_helpers.table_querying function
    response = db_helpers.table_querying(table_name)
    
    # Convert the query response into a DataFrame
    response_df = pd.DataFrame([i for i in response])
    
    # Determine which columns to drop from the DataFrame
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    
    # Drop the specified columns from the DataFrame
    response_df = response_df.drop(columns=columns_to_drop)
    
    # Return the resulting DataFrame
    return response_df

def table_querying_with_datetime_filters(early_date, late_date,
                                         table_name="case_cache",
                                         columns_to_drop=["name"]
                                         ):
    """
    Retrieve records from the specified table within a given datetime range, convert them to a DataFrame,
    and drop specified columns from the resulting DataFrame.

    Args:
        early_date (str): The start of the datetime range for querying records.
        late_date (str): The end of the datetime range for querying records.
        table_name (str, optional): The name of the table to query. Defaults to "case_cache".
        columns_to_drop (list, optional): A list of column names to drop from the DataFrame. Defaults to ["name"].

    Returns:
        pandas.DataFrame: A DataFrame containing the queried records within the specified datetime range
                          with specified columns dropped.
    """
    
    # Determine the index corresponding to the early and late dates
    early_date_id = db_helpers.datetime_index_detector(early_date)
    late_date_id = db_helpers.datetime_index_detector(late_date)
    
    # Generate a list of indexes within the specified datetime range
    indexes = range(early_date_id, late_date_id)
    
    # Create a SQL string to use in filtering based on indexes
    indexes_sql_str = " or id=".join([str(i) for i in indexes])
            
    # Query the specified table with index filtering using db_helpers.table_column_filter function
    response = db_helpers.table_column_filter(key=indexes_sql_str,
                                              table_name=table_name,
                                              key_column="id", is_num=True)

    # Convert the query response into a DataFrame
    response_df = pd.DataFrame([i for i in response])
    
    # Determine which columns to drop from the DataFrame
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    
    # Drop the specified columns from the DataFrame
    response_df = response_df.drop(columns=columns_to_drop)
    
    # Return the resulting DataFrame
    return response_df

def entries_querying(key, table_name="patient", key_column="name"):
    """
    Query records from the specified table based on a provided key value, convert them to a DataFrame.

    Args:
        key: The value to use for querying records in the specified column.
        table_name (str, optional): The name of the table to query. Defaults to "patient".
        key_column (str, optional): The name of the column to use for querying. Defaults to "name".

    Returns:
        pandas.DataFrame: A DataFrame containing the queried records based on the provided key value.
    """
    # Query the specified table using db_helpers.table_column_filter function
    response = db_helpers.table_column_filter(key=key,
                                              table_name=table_name,
                                              key_column=key_column
                                              )

    # Convert the query response into a DataFrame
    response_df = pd.DataFrame([i for i in response])
    
    # Return the resulting DataFrame
    return response_df

def online_querying(table_name="patient", batch_size=1000,
                    previous_indexes=[], columns_to_drop=["name"]):
    """
    Perform online querying of records from the specified table, considering batch processing,
    previously queried indexes, and optionally dropping specified columns.

    Args:
        table_name (str, optional): The name of the table to query. Defaults to "patient".
        batch_size (int, optional): The number of records to retrieve in each batch. Defaults to 1000.
        previous_indexes (list, optional): List of indexes already queried. Defaults to an empty list.
        columns_to_drop (list, optional): A list of column names to drop from the DataFrame. Defaults to ["name"].

    Returns:
        dict: A dictionary containing query response details including the DataFrame of queried records,
              the original table length, the number of samples returned, the returned indexes,
              and the status code.
    """
    # Get the size of the specified table
    table_size = db_helpers.count_table_size(table_name)
    
    # Check if the provided list of indexes is longer than the table
    if table_size <= len(previous_indexes):
        return {"response": "provided indexes list is longer than the table",
                "status": 400}

    # Get the last ID in the specified table
    last_id = db_helpers.table_last_id(table_name)
    
    # Generate a list of possible indexes based on previously queried indexes
    possible_indexes = list(set(range(last_id+1)) - set(previous_indexes))
    
    # Randomly sample indexes based on batch size and available possible indexes
    indexes = np.random.choice(possible_indexes, size=len(possible_indexes), replace=False)
    
    # Create a SQL string to use for filtering based on the sampled indexes
    if (batch_size >= len(indexes)):
        indexes_sql_str = " or id=".join([str(i) for i in indexes])
    else:
        indexes_sql_str = " or id=".join([str(i) for i in indexes[:batch_size]])
    
    # Query the specified table with index filtering using db_helpers.table_column_filter function
    response = db_helpers.table_column_filter(key=indexes_sql_str,
                                              table_name=table_name,
                                              key_column="id", is_num=True)
    
    # Convert the query response into a DataFrame
    response_df = pd.DataFrame([i for i in response])
    
    # Determine which columns to drop from the DataFrame
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    
    # Drop the specified columns from the DataFrame
    response_df = response_df.drop(columns=columns_to_drop)

    # Return a dictionary containing query response details
    return {"data": response_df,
            "original_table_length": table_size,
            "number_of_samples": len(response_df),
            "returned_indexes": response_df["id"].tolist(),
            "status": 200
            }

def create_resource(resource_table_name, details_dict):
    """
    Create a new resource in the specified database table using the provided details.

    Args:
        resource_table_name (str): The name of the table where the new resource will be created.
        details_dict (dict): A dictionary containing the details of the new resource.

    Returns:
        None
    """
    # Generate a new ID for the resource by incrementing the last ID in the specified table
    new_id = db_helpers.table_last_id(resource_table_name) + 1
    
    # Add the new ID to the details dictionary
    details_dict.update({"id": new_id})

    # Get the database model class for the specified resource table
    db_model = getattr(db_models, str.capitalize(resource_table_name))
    
    # Condition to handle specific resource creation process for "malaria_results" table
    if resource_table_name == "malaria_results":
        # Create a new resource object
        new_resource = db_model(**details_dict)
        
        # Add the new resource to the database session and commit the transaction
        db_models.db.session.add(new_resource)
        db_models.db.session.commit()

        # Get the patient ID associated with the blood test
        patient_id = db_models.Blood_test.query.filter_by(id=details_dict["blood_test_id"]).first().patient_id
        
        # Query the patient details based on the patient ID
        current_patient = db_helpers.table_column_filter(key=patient_id, table_name="patient", key_column="id")
        current_patient_dict = pd.DataFrame(current_patient).to_dict('records')[0]
        
        # Update the patient ID field and create a new resource for Case_cache
        current_patient_dict["patient_id"] = current_patient_dict.pop('id')
        case_cache_dict = details_dict.copy()
        case_cache_dict.update({"date": datetime.datetime.now()})
        case_cache_dict.update(current_patient_dict)
        new_resource = db_models.Case_cache(**case_cache_dict)
    else:
        # Create a new resource object
        new_resource = db_model(**details_dict)

    # Add the new resource to the database session and commit the transaction
    db_models.db.session.add(new_resource)
    db_models.db.session.commit()

def update_resource(resource_table_name, id, details_dict):
    """
    Update an existing resource in the specified database table with the provided details.

    Args:
        resource_table_name (str): The name of the table where the resource to be updated resides.
        id: The ID of the resource to be updated.
        details_dict (dict): A dictionary containing the details to update in the resource.

    Returns:
        None
    """
    # Get the database model class for the specified resource table
    db_model = getattr(db_models, str.capitalize(resource_table_name))
    
    # Query the resource to be updated based on the provided ID
    resource = db_model.query.filter_by(id=id).first()
    
    # Iterate through the details dictionary and set the updated attributes for the resource
    [setattr(resource, attr, val) for attr, val in details_dict.items()]
    
    # Commit the transaction to save the changes to the resource
    db_models.db.session.commit()

def delete_resource(resource_table_name, id):
    """
    Delete an existing resource from the specified database table based on the provided ID.

    Args:
        resource_table_name (str): The name of the table where the resource to be deleted resides.
        id: The ID of the resource to be deleted.

    Returns:
        None
    """
    # Get the database model class for the specified resource table
    db_model = getattr(db_models, str.capitalize(resource_table_name))
    
    # Query the resource to be deleted based on the provided ID
    resource = db_model.query.filter_by(id=id).first()
    
    # Delete the queried resource from the database
    db_models.db.session.delete(resource)
    
    # Commit the transaction to remove the resource from the database
    db_models.db.session.commit()

     