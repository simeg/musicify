import logging
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Union

logger = logging.getLogger(__name__)
IS_PRODUCTION = bool(os.environ.get('IS_PRODUCTION', default=False))

config_path = "./src/config.yaml"

Config = Union[Dict[str, Any], None]


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
        return None


def _get_config() -> Config:
    if IS_PRODUCTION:
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
            else:
                return None
        except FileNotFoundError:
            logger.exception(
                "Could not find configuration file at path=[%s]", config_path)
            return None
