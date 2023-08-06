import db_models
import pandas as pd
import numpy as np
import db_helpers
import datetime

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

    db_model = getattr(db_models,str.capitalize(resource_table_name))
    
    if resource_table_name=="malaria_results":
        new_resource = db_model(**details_dict)
        db_models.db.session.add(new_resource)
        db_models.db.session.commit()

        patient_id = db_models.Blood_test.query.filter_by(id=details_dict["blood_test_id"]).first().patient_id
        current_patient = db_helpers.table_column_filter(key=patient_id,table_name="patient",key_column="id")
        current_patient_dict = pd.DataFrame(current_patient).to_dict('records')[0] 
        current_patient_dict["patient_id"] = current_patient_dict.pop('id')
        case_cache_dict = details_dict.copy()
        case_cache_dict.update({"date":datetime.datetime.now()})
        case_cache_dict.update(current_patient_dict)
        new_resource = db_models.Case_cache(**case_cache_dict)
    else:
        new_resource = db_model(**details_dict)

    db_models.db.session.add(new_resource)
    db_models.db.session.commit()

def update_resource(resource_table_name,id,details_dict):
    db_model = getattr(db_models,str.capitalize(resource_table_name))
    resource = db_model.query.filter_by(id=id).first()
    [setattr(resource,attr,val) for attr,val in details_dict.items()]
    db_models.db.session.commit()

def delete_resource(resource_table_name,id):
    db_model = getattr(db_models,str.capitalize(resource_table_name))
    resource = db_model.query.filter_by(id=id).first()
    db_models.db.session.delete(resource)
    db_models.db.session.commit()


        
            
        