# Data_access_model_for_malaria_awareness_in_Rwanda

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

