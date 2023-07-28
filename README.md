# Data_access_model_for_malaria_awareness_in_Rwanda


Before running this, create a .env file with this configuration:

```python
# ENVIRONMENT_STATE
APP_ENVIRONMENT = DEVELOPMENT  #can also be PRODUCTION

# DEVELOPMENT VARIABLES
DB_DIALECT_DEV = [SQL database being used, e.g: "postgresql"]
DB_USERNAME_DEV = [username ]
DB_PASSWORD_DEV = [password]
DB_HOST_DEV = "localhost"
DB_PORT_DEV = "5432"
DB_NAME_DEV = [existing database name, e.g: "malaria_draft"]

SERVER_PORT_DEV = 3000

# PRODUCTION VARIABLES
DB_HOST_PROD = [production database url]
DB_PASSWORD_PROD = [production database password]

```

Endpoint's documentation is on this link (will be updated):
https://documenter.getpostman.com/view/21729470/2s9XxsWGep
