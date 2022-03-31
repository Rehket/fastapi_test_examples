import os
import tempfile
from pathlib import Path
import ssl

try:
    import loguru

    logger = loguru.logger
except ImportError as e:
    import logging as logger


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/api/v1"
LOCAL_DEV = getenv_boolean("LOCAL_DEV", False)
IS_TESTING = getenv_boolean("IS_TESTING", False)
API_QUERY_LIMIT = os.getenv("API_QUERY_LIMIT")

if os.supports_bytes_environ:
    SECRET_KEY = os.getenvb(b"SECRET_KEY", str(os.urandom(32)).encode())
else:
    SECRET_KEY = os.getenv("SECRET_KEY", str(os.urandom(32))).encode()


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVICE_NAME = os.getenv("SERVICE_NAME", None)
OPEN_API_PREFIX = "" if SERVICE_NAME is None else f"/services/{SERVICE_NAME}"

# a string of origins separated by commas, e.g:
# "http://localhost, http://localhost:4200, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "*")
PROJECT_NAME = os.getenv("PROJECT_NAME")

# Postgres Credentials and Configuration

FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA")

RDS_CERTIFICATE_PATH = os.getenv(
    "RDS_CERTIFICATE_PATH", "/app_dir/rds-cert-chain-2019.pem"
)
USE_DATABASE_SSL = getenv_boolean("USE_DATABASE_SSL")

RDS_SSL_CONTEXT = (
    ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH, cafile=RDS_CERTIFICATE_PATH
    )
    if USE_DATABASE_SSL
    else None
)

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?options=-csearch_path={POSTGRES_SCHEMA}"

PUBLIC_TABLES = []
SCHEMA_QUERY = f"SELECT s.nspname AS schema_name FROM pg_catalog.pg_namespace;"

# AWS Credentials And Configuration

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET = os.getenv("AWS_BUCKET")
KMS_KEY = os.getenv("KMS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_SQS_QUEUE_NAME = os.getenv("AWS_SQS_QUEUE_NAME")

AWS_READY = (
    AWS_ACCESS_KEY_ID is not None
    and AWS_SECRET_ACCESS_KEY is not None
    and AWS_BUCKET is not None
    and AWS_REGION is not None
    and KMS_KEY is not None
)

SERVICE_ENVIRONMENT = os.getenv("SERVICE_ENVIRONMENT", None)

# SalesForce Credentials & Configuration

SFDC_ENVIRONMENT = os.getenv("SFDC_ENVIRONMENT", None)
SFDC_API_VERSION = (
    os.getenv("SFDC_API_VERSION", "v51.0")
    if "v" in os.getenv("SFDC_API_VERSION", "v51.0")
    else f"v{os.getenv('SFDC_API_VERSION', 'v51.0')}"
)
SFDC_CONSUMER_KEY = os.getenv("SFDC_CONSUMER_KEY", None)
SFDC_USERNAME = os.getenv("SFDC_USERNAME", None)
SFDC_PRIVATE_KEY = os.getenv("SFDC_PRIVATE_KEY", None)

SFDC_LINE_ENDING = os.getenv("SFDC_LINE_ENDING", None)

if os.name == "nt" and SFDC_LINE_ENDING is None:
    SFDC_LINE_ENDING = "CRLF"
else:
    SFDC_LINE_ENDING = "LF"

# DNB Credentials & Configuration
DNB_HOST_URL = os.getenv("DNB_HOST_URL", "https://plus.dnb.com")
DNB_KEY = os.getenv("DNB_KEY", None)
DNB_SECRET = os.getenv("DNB_SECRET", None)

# Lead Scoring Configurations
LEAD_SCORING_FLAG = getenv_boolean("LEAD_SCORING_FLAG")
LEAD_SCORING_HOST = os.getenv("LEAD_SCORING_HOST")
