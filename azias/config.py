import json
import logging
import os
import sys

config: dict = dict()
current_logger_level_generic = logging.DEBUG
current_logger_level_thread = logging.DEBUG
current_logger_level_worker = logging.DEBUG
current_logger_level_youtube = logging.INFO


def load(config_path: str) -> None:
    if not os.path.exists(config_path):
        print("ERROR: The config file '{}' could not be found !".format(config_path))
        sys.exit(1000)
        
    try:
        f = open(config_path, "r")
        global config
        config = json.load(f)
        f.close()
    except Exception as err:
        print("Failed to load or parse the config file !")
        print(err)
        sys.exit(1002)


def get_basedir() -> str:
    return os.path.abspath(config["application"]["base_output_dir"])


def get_youtube_basedir() -> str:
    return os.path.join(get_basedir(), config["youtube"]["output_subdir"])


def get_youtube_metadata_delay() -> int:
    return config["youtube"]["delay_ms_before_metadata_download"]
