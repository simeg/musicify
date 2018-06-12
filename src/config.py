import logging
import os
from pathlib import Path
from typing import Dict, Any

import yaml

logger = logging.getLogger(__name__)
is_production = bool(os.environ.get('IS_PRODUCTION', default=False))

config_path = "./src/config.yaml"

Config = Dict[str, Any]


def spotify_api() -> Config:
    return _get_config_key('spotify_api')


def face_api() -> Config:
    return _get_config_key('face_api')


def _get_config_key(key) -> Config:
    config = _get_config()
    if key in config:
        return config[key]
    else:
        logger.error("Key [%s] does not exist in config dict", key)


def _get_config() -> Config:
    if is_production:
        env = os.environ
        return {
            "spotify_api": {
                "client_id": env.get('spotify_client_id'),
                "client_secret": env.get('spotify_client_secret'),
            },
            "face_api": {
                "subscription_key": env.get('face_api_subscription_key'),
            }
        }
    else:
        try:
            if Path(config_path).exists():
                with open(config_path) as file:
                    return yaml.load(file)
        except FileNotFoundError:
            logger.exception(
                "Could not find configuration file at path=[%s]", config_path)
