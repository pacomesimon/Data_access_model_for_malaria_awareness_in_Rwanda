#!/usr/bin/env python
"""The Helper functions (used in the controllers.py file)
DESCRIPTION:
------------
This file contains the helper functions used in the controllers.py file.
"""

from db_models import db

def table_querying(table_name="case_cache"):
    """
    Execute a SQL query to retrieve all records from the specified table.

    Args:
        table_name (str, optional): The name of the table to query. Defaults to "case_cache".

    Returns:
        sqlalchemy.engine.ResultProxy: The query response containing the retrieved records.
    """
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        """
    )
    return response

def datetime_index_detector(datetime_str):
    """
    Detect the index of the first record in the "blood_test" table with a date greater than or equal to the given datetime.

    Args:
        datetime_str (str): The datetime string to compare against the "date" column in the "blood_test" table.

    Returns:
        int: The index of the first record meeting the condition, or None if no such record is found.
    """
    response = db.engine.execute(
        f"""
        select *    
        from blood_test
        where date >= '{datetime_str}'
        limit 1
        """
    )
    return [i for i in response][0][0]

def table_column_filter(key,table_name="patient",key_column="name",is_num=False):
    """
    Filter records from the specified table based on the provided key value.

    Args:
        key: The value to use for filtering records in the specified column.
        table_name (str, optional): The name of the table to filter. Defaults to "patient".
        key_column (str, optional): The name of the column to use for filtering. Defaults to "name".
        is_num (bool, optional): Whether the key is a numeric value. Defaults to False.

    Returns:
        sqlalchemy.engine.ResultProxy: The query response containing the filtered records.
    """
    if is_num:
        response = db.engine.execute(
            f"""
            select * 
            from {table_name}
            where {key_column} = {key}
            """
        )
        return response
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        where {key_column} = '{key}'
        """
    )
    return response

def count_table_size(table_name):
    """
    Count the number of records in the specified table.

    Args:
        table_name (str): The name of the table to count records from.

    Returns:
        int: The number of records in the specified table.
    """
    global table_size_dict
    response = db.engine.execute(
        f"""
        select count(id) 
        from {table_name}
        """
    )
    for i in response:
        return i[0]

def table_last_id(table_name):
    """
    Retrieve the last (maximum) ID value from the specified table.

    Args:
        table_name (str): The name of the table to retrieve the last ID from.

    Returns:
        int: The last (maximum) ID value in the specified table.
    """
    global table_size_dict
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        order by id desc limit 1
        """
    )
    for i in response:
        return i[0]
    
