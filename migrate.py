#!/usr/bin/env python
"""The migration script
DESCRIPTION:
------------
This file contains the migration script, which initializes the database.
"""

from db_models import *  # Import your database models here
import pandas as pd
from config import cfg  # Import your configuration settings here

# Create all tables in the database schema
db.create_all()

if cfg["APP_ENVIRONMENT"] == "DEVELOPMENT":
    # Drop and recreate all tables if in development environment
    db.drop_all()
    db.create_all()

    # Define the location of dataset CSV files and their filenames
    datasets_folder_location = "datasets/"
    csv_filenames = ["provinces", "districts", "sectors",
                     "cells", "villages", "health_centers",
                     "patients", "blood_tests", "malaria_results", "users", "case_caches"]

    # Loop through the CSV filenames and read and import them into respective tables
    for i in csv_filenames:
        df = pd.read_csv(datasets_folder_location + i + ".csv")
        if i == "malaria_results":
            df.to_sql(con=db.engine, name=i, if_exists='append', index=False)
        else:
            df.to_sql(con=db.engine, name=i[:-1], if_exists='append', index=False)

if cfg["APP_ENVIRONMENT"] == "PRODUCTION":
    # Create all tables if in production environment
    db.create_all()
