# Data_access_model_for_malaria_awareness_in_Rwanda


Before running this, create a .env file with this configuration:

# ENVIRONMENT_STATE
APP_ENVIRONMENT = DEVELOPMENT  #can also be PRODUCTION

# DEVELOPMENT VARIABLES
DB_DIALECT_DEV = "postgresql"
DB_USERNAME_DEV = "..."
DB_PASSWORD_DEV = "******"
DB_HOST_DEV = "localhost"
DB_PORT_DEV = "5432"
DB_NAME_DEV = "malaria_draft"

SERVER_PORT_DEV = 3000

# PRODUCTION VARIABLES
DB_HOST_PRODUCTION = 198.234.27.1
DB_PASSWORD_PRODUCTION = 75a9cd234ef
