import subprocess
import os
import time
import json
import sys
import logging
from pathlib import Path
from google.cloud import secretmanager
import shlex


TEAM_GCP_PROJECT = os.environ["TEAM_GCP_PROJECT"]
SECRET_NAME = <INSERT-HERE>

DBT_BASE_COMMAND = ["dbt", "--no-use-colors", "--log-format", "json"]


def get_dbt_log(log_path) -> str:
    with open(log_path) as log:
        return log.read()


def dbt_log_to_xcom():
    dbt_log_path = "logs/dbt.log"
    xcom_json_path = "/airflow/xcom/return.json"
    dbt_koder = ["Z023"]
    xcom_log = []
    with open(dbt_log_path) as f:
        for log_line in f:
            log_obj = json.loads(log_line)
            if "info" in log_obj and log_obj["info"]["code"] in dbt_koder:
                xcom_log.append(log_obj)
    with open(xcom_json_path, "w") as f:
        f.write(json.dumps(xcom_log))


def set_secrets_as_envs():
    secrets = secretmanager.SecretManagerServiceClient()
    resource_name = f"projects/{TEAM_GCP_PROJECT}/secrets/{SECRET_NAME}/versions/latest"
    secret = secrets.access_secret_version(name=resource_name)
    secret_str = secret.payload.data.decode("UTF-8")
    secrets = json.loads(secret_str)
    os.environ.update(secrets)


if __name__ == "__main__":
    set_secrets_as_envs()  # get secrets from gcp
    logger = logging.getLogger(__name__)
    log_path = Path(__file__).parent / "logs/dbt.log"

    stream_handler = logging.StreamHandler(sys.stdout)
    os.environ["TZ"] = "Europe/Oslo"
    time.tzset()

    schema = os.environ["DB_SCHEMA"]
    os.environ["DBT_ENV_SECRET_USER"] = f"{os.environ['DB_USER']}[{schema}]"
    os.environ["DBT_DB_SCHEMA"] = schema
    os.environ["DBT_ENV_SECRET_PASS"] = os.environ["DB_PASSWORD"]
    logger.info("DBT miljøvariabler er lastet inn")

    # default dbt kommando er build
    command = shlex.split(os.getenv("DBT_COMMAND", "build"))

    log_level = os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(log_level)
    logger.addHandler(stream_handler)

    try:
        subprocess.run(
            DBT_BASE_COMMAND + ["deps"],
            check=True,
            capture_output=True,
        )
        output = subprocess.run(
            (DBT_BASE_COMMAND + command),
            check=True,
            capture_output=True,
        )
        logger.info(output.stdout.decode("utf-8"))
        logger.debug(get_dbt_log(log_path))
        # dbt_log_to_xcom()
    except subprocess.CalledProcessError as err:
        raise Exception(logger.error(get_dbt_log(log_path)), err.stdout.decode("utf-8"))
