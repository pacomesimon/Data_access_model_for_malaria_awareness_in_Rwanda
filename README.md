# Data_access_model_for_malaria_awareness_in_Rwanda
This repository has been designed for demonstrational purposes for [this ongoing research project](https://drive.google.com/file/d/1dps8J_RSjVfLxSNQgXv6QEFGfBnSMVZK/view). Anyone from CMU/Cylab is free to inspect it and provide suggestions to the owner. 
## Files & folders structure:

```python
│   .env  # Configuration file for environment variables
│   .gitignore  # File specifying which files and directories to ignore in Git version control
│   app.py  # Main application file
│   authentication.py  # File containing the authentication function source code
│   config.py  # Configuration file for application settings
│   controllers.py  # File containing the controller functions for handling API requests
│   db_helpers.py  # File containing helper functions for interacting with the database
│   db_models.py  # File containing the database models (READ ITS CONTENTS TO KNOW THE DB STRUCTURE)
│   LICENSE  # License file
│   migrate.py  # File for handling database migrations
│   README.md  # Readme file with project documentation (THIS FILE)
│   request_log.py  # File for logging API requests
│   requirements.txt  # File specifying the required Python packages for the project
│
│
├───api_docs  # Folder containing API documentation (the contained file can be imported as a POSTMAN collection)
│       Data_access_model_for_malaria_awareness_in_Rwanda.postman_collection.json  # JSON file (API docs)
│
├───datasets  # Folder containing datasets
│       blood_tests.csv  # CSV file containing blood test data
│       case_caches.csv  # CSV file containing case cache data
│       cells.csv  # CSV file containing cell data
│       districts.csv  # CSV file containing district data
│       health_centers.csv  # CSV file containing health center data
│       malaria_results.csv  # CSV file containing malaria result data
│       patients.csv  # CSV file containing patient data
│       provinces.csv  # CSV file containing province data
│       sectors.csv  # CSV file containing sector data
│       users.csv  # CSV file containing user data
│       villages.csv  # CSV file containing village data
│
├───demo  # Folder containing demo files
│       accessing_the_endpoints_demo.ipynb  # Jupyter notebook (demo: how to access the API endpoints)
│       sampling_demo.ipynb  # Jupyter notebook (demo: data sampling techniques)
│
└───requests_logs  # Folder that will contain request logs
         2023_08_23_09_23_47_420296.json  # example of a JSON file containing an example request log

```

## How to run this app:
### Step 0: Before running this, create a .env file with this configuration:

```python
# ENVIRONMENT_STATE
APP_ENVIRONMENT = DEVELOPMENT  # can also be PRODUCTION

# DEVELOPMENT VARIABLES
DB_DIALECT_DEV = "postgresql"   # this system was configured to run on postgresql
DB_USERNAME_DEV =               # your database username
DB_PASSWORD_DEV = *****         # your database password
DB_HOST_DEV = "localhost"       # or your database domain name
DB_PORT_DEV = "5432"            # or your database port
DB_NAME_DEV = "malaria_db"      # or any other existing database
REQUEST_LOGS_PATH_DEV= "./requests_logs/"     # path to the logs' folder

SERVER_PORT_DEV = 3000          # server/API port

# PRODUCTION VARIABLES
DB_DIALECT_PROD = "postgresql"   # this system was configured to run on postgresql
DB_USERNAME_PROD =               # your database username
DB_PASSWORD_PROD = *****         # your database password
DB_HOST_PROD = "localhost"       # or your database domain name
DB_PORT_PROD = "5432"            # or your database port
DB_NAME_PROD = "malaria_db"      # or any other existing database
REQUEST_LOGS_PATH_PROD = "./requests_logs/"     # path to the logs' folder

SERVER_PORT_PROD = 3000          # server/API port

```
### Step 1: Next, using the terminal, cd to this repository's root directory and run this to install required packages:
`pip install -r requirements.txt`

### Step 2: Next, run this to migrate CSV files from the [./datasets](./datasets) folder to the DEVELOPMENT POSTGRESQL database:
`python migrate.py`
(this works if your `APP_ENVIRONMENT` variable was set to `DEVELOPMENT`. See your `.env` file mentioned above.)

### Step 3: Next, run this to start the DEVELOPMENT server:
`python app.py`

### Step 4: Use POSTMAN software to test the endpoints.
Here you can import [this JSON file](api_docs\Data_access_model_for_malaria_awareness_in_Rwanda.postman_collection.json) in POSTMAN as a collection of requests.
You can also refer to the endpoint's documentation [on this link](https://documenter.getpostman.com/view/21729470/2s9XxsWGep) (will be updated).

#### Demo (simpler alternative):
You can also read the Jupyter notebooks saved in [the demo folder](./demo/) to get the main ideas on how to access the server's endpoints.

