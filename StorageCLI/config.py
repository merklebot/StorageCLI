from platformdirs import user_config_path
from pathlib import Path
import json

APP_NAME = "StorageCLI"
AUTHOR_NAME = "Merklebot"
config_file = Path(f'{user_config_path(APP_NAME, AUTHOR_NAME)}/config.json')


def write_config(organization_name, bucket_token):
    config_file.parent.mkdir(exist_ok=True, parents=True)
    config_file.write_text(json.dumps({
        "organization_name": organization_name,
        "bucket_token": bucket_token
    }))


def read_organization_name():
    config = json.loads(config_file.read_text())
    return config.get("organization_name")


def read_token():
    config = json.loads(config_file.read_text())
    return config.get("bucket_token")


def clear_config():
    config_file.parent.mkdir(exist_ok=True, parents=True)
    config_file.write_text("{}")
