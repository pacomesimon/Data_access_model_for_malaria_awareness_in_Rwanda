from dotenv import load_dotenv
import os
load_dotenv()

if (os.environ["APP_ENVIRONMENT"]=="DEVELOPMENT"):
    cfg = {
        "APP_ENVIRONMENT" : "DEVELOPMENT",
        'DB_DIALECT' : os.environ["DB_DIALECT_DEV"],
        "DB_USERNAME" : os.environ["DB_USERNAME_DEV"],
        "DB_PASSWORD" : os.environ["DB_PASSWORD_DEV"],
        "DB_HOST" : os.environ["DB_HOST_DEV"],
        "DB_PORT" : os.environ["DB_PORT_DEV"],
        "DB_NAME" : os.environ["DB_NAME_DEV"],
        "SERVER_PORT": os.environ["SERVER_PORT_DEV"],
    }

if (os.environ["APP_ENVIRONMENT"]=="PRODUCTION"):
    cfg = {
        "APP_ENVIRONMENT" : "PRODUCTION",
        'DB_DIALECT' : os.environ["DB_DIALECT_PROD"],
        "DB_USERNAME" : os.environ["DB_USERNAME_PROD"],
        "DB_PASSWORD" : os.environ["DB_PASSWORD_PROD"],
        "DB_HOST" : os.environ["DB_HOST_PROD"],
        "DB_PORT" : os.environ["DB_PORT_PROD"],
        "DB_NAME" : os.environ["DB_NAME_PROD"],
        "SERVER_PORT": os.environ["SERVER_PORT_PROD"],
    }