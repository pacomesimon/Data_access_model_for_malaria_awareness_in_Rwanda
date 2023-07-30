from db_models import *
import pandas as pd
from config import cfg

db.create_all()

if (cfg["APP_ENVIRONMENT"] == "DEVELOPMENT"): 
    db.drop_all()
    db.create_all()
    datasets_folder_location = "datasets/"
    csv_filenames=["provinces","districts","sectors",
                "cells","villages","health_centers",
                "patients","blood_tests","malaria_results","users","case_caches"
                ]
    for i in csv_filenames:
        df = pd.read_csv(datasets_folder_location + i +".csv")
        # df=df.dropna()
        if i == "malaria_results":
            df.to_sql(con=db.engine, name=i, if_exists='append', index=False)
        else:
            df.to_sql(con=db.engine, name=i[:-1], if_exists='append', index=False)

if (cfg["APP_ENVIRONMENT"] == "PRODUCTION"):
    db.create_all()