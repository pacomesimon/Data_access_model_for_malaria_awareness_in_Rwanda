from db_models import db

def table_querying(table_name="case_cache"):
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        """
    )
    return response

def datetime_index_detector(datetime_str):
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
    
