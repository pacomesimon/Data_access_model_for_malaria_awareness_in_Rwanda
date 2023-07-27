from db_models import * 
import pandas as pd

def table_querying(table_name="case_cache",
                        columns_to_drop=["name"],
                        ):
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        """
    )
    response_df=pd.DataFrame([i for i in response])
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    response_df=response_df.drop(columns=columns_to_drop)
    return response_df 

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

def table_querying_with_datetime_filters(early_date,late_date,
                                          table_name="case_cache",
                                          columns_to_drop=["name"]
                        ):
    
    early_date_id = datetime_index_detector(early_date)
    late_date_id = datetime_index_detector(late_date)
    
    indexes=range(early_date_id,late_date_id)
    
    indexes_sql_str = " or id=".join([str(i) for i in indexes])
            
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        where id={indexes_sql_str}
        """
    )

    response_df=pd.DataFrame([i for i in response])
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    response_df=response_df.drop(columns=columns_to_drop)
    return response_df


def entries_querying(key,table_name="patient",key_column="name"):
    response = db.engine.execute(
        f"""
        select * 
        from {table_name}
        where {key_column} = '{key}'
        """
    )

    response_df=pd.DataFrame([i for i in response])
    return response_df 

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
    
def create_resource(resource_table_name,details_dict):
    new_id = table_last_id(resource_table_name) + 1
    details_dict.update({"id":new_id})
    if resource_table_name=="patient":
        new_resource = Patient(**details_dict)
    elif resource_table_name=="health_center":
        new_resource = Health_center(**details_dict)
    elif resource_table_name=="blood_test":
        new_resource = Blood_test(**details_dict)
    elif resource_table_name=="malaria_results":
        new_resource = Malaria_results(**details_dict)
    elif resource_table_name=="case_cache":
        new_resource = Case_cache(**details_dict)
    else:
        return "Resource's table not found"
    
    db.session.add(new_resource)
    db.session.commit()

def update_resource(resource_table_name,id,details_dict):
    if resource_table_name=="patient":
        resource = Patient.query.filter_by(id=id).first()
    elif resource_table_name=="health_center":
        resource = Health_center.query.filter_by(id=id).first()
    elif resource_table_name=="blood_test":
        resource = Blood_test.query.filter_by(id=id).first()
    elif resource_table_name=="malaria_results":
        resource = Malaria_results.query.filter_by(id=id).first()
    elif resource_table_name=="case_cache":
        resource = Case_cache.query.filter_by(id=id).first()
    else:
        return "Resource's table not found"
    
    [setattr(resource,attr,val) for attr,val in details_dict.items()]
    db.session.commit()

def delete_resource(resource_table_name,id):
    if resource_table_name=="patient":
        resource = Patient.query.filter_by(id=id).first()
    elif resource_table_name=="health_center":
        resource = Health_center.query.filter_by(id=id).first()
    elif resource_table_name=="blood_test":
        resource = Blood_test.query.filter_by(id=id).first()
    elif resource_table_name=="malaria_results":
        resource = Malaria_results.query.filter_by(id=id).first()
    elif resource_table_name=="case_cache":
        resource = Case_cache.query.filter_by(id=id).first()
    else:
        return "Resource's table not found"
    
    db.session.delete(resource)
    db.session.commit()

