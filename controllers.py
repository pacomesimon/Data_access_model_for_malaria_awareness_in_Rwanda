from db_models import * 
import pandas as pd
import numpy as np
import db_helpers

def table_querying(table_name="case_cache",
                        columns_to_drop=["name"],
                        ):
    response = db_helpers.table_querying(table_name)
    response_df=pd.DataFrame([i for i in response])
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    response_df=response_df.drop(columns=columns_to_drop)
    return response_df 

def table_querying_with_datetime_filters(early_date,late_date,
                                          table_name="case_cache",
                                          columns_to_drop=["name"]
                        ):
    
    early_date_id = db_helpers.datetime_index_detector(early_date)
    late_date_id = db_helpers.datetime_index_detector(late_date)
    
    indexes=range(early_date_id,late_date_id)
    
    indexes_sql_str = " or id=".join([str(i) for i in indexes])
            
    response = db_helpers.table_column_filter(key=indexes_sql_str,
                                              table_name=table_name,
                                              key_column="id",is_num=True)

    response_df=pd.DataFrame([i for i in response])
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    response_df=response_df.drop(columns=columns_to_drop)
    return response_df


def entries_querying(key,table_name="patient",key_column="name"):
    response = db_helpers.table_column_filter(key=key,
                                              table_name=table_name,
                                              key_column=key_column
                                              )

    response_df=pd.DataFrame([i for i in response])
    return response_df

def online_querying(table_name="patient",batch_size=1000,
                    previous_indexes=[],
                    columns_to_drop=["name"]
                        ):
    table_size = db_helpers.count_table_size(table_name)
    if table_size <= len(previous_indexes):
        return {"response": "provided indexes list is longer than the table",
                "status" : 400}

    last_id = db_helpers.table_last_id(table_name)
    possible_indexes= list(set(range(last_id)) - set(previous_indexes))
    indexes = np.random.choice(possible_indexes, size=len(possible_indexes), replace=False)
    
    if((batch_size)>=len(indexes)):
        indexes_sql_str = " or id=".join([str(i) for i in indexes])
    else:
        indexes_sql_str = " or id=".join([str(i) for i in indexes[:batch_size+1]])
    response = db_helpers.table_column_filter(key=indexes_sql_str,
                                              table_name=table_name,
                                              key_column="id",is_num=True)
    
    response_df=pd.DataFrame([i for i in response])
    columns_to_drop = list(set(response_df.columns) & set(columns_to_drop))
    response_df=response_df.drop(columns=columns_to_drop)

    return {"data": response_df,
            "original_table_length": table_size,
            "number_of_samples" : len(response_df),
            "returned_indexes": response_df["id"].tolist(),
            "status": 200
            }

def create_resource(resource_table_name,details_dict):
    new_id = db_helpers.table_last_id(resource_table_name) + 1
    details_dict.update({"id":new_id})
    if resource_table_name=="patient":
        new_resource = Patient(**details_dict)
    elif resource_table_name=="health_center":
        new_resource = Health_center(**details_dict)
    elif resource_table_name=="blood_test":
        new_resource = Blood_test(**details_dict)
    elif resource_table_name=="malaria_results":
        new_resource = Malaria_results(**details_dict)
        db.session.add(new_resource)
        db.session.commit()
        patient_id = Blood_test.query.filter_by(id=details_dict["id"]).first().patient_id
        current_patient =Patient.query.filter_by(id=patient_id).first()
        case_cache_dict = {
            "id": details_dict["id"],
            "date": details_dict["date"],
            "patient_id": patient_id,
            "Name": current_patient.name,
            "date_of_birth": current_patient.date_of_birth,
            "gender": current_patient.gender,
            "village_id": current_patient.village_id,
            "malaria_status": details_dict["malaria_status"],
            "parasite_type": details_dict["parasite_type"],
            "blood_test_id": details_dict["id"],
        }
        new_resource = Case_cache(**case_cache_dict)   
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
        [setattr(resource,attr,val) for attr,val in details_dict.items()]
        resource = Case_cache.query.filter_by(id=id).first()
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


        
            
        