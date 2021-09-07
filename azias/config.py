import json
import logging
import os

config: dict = dict()
current_logger_level_generic = logging.DEBUG
current_logger_level_thread = logging.DEBUG
current_logger_level_worker = logging.DEBUG
current_logger_level_youtube = logging.INFO


def load(config_path: str) -> None:
    if not os.path.exists(config_path):
        raise OSError("The config file '{}' could not be found !".format(config_path))
    
    f = open(config_path, "r")
    try:
        global config
        config = json.load(f)
    except Exception as err:
        f.close()
        raise err
    f.close()


def get_basedir() -> str:
    return os.path.abspath(config["application"]["base_output_dir"])


def get_youtube_basedir() -> str:
    return os.path.join(get_basedir(), config["youtube"]["output_subdir"])


def get_youtube_metadata_delay() -> int:
    return config["youtube"]["delay_ms_before_metadata_download"]
