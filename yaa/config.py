import json
import logging
import os
import sys
from typing import Union

import yaa
from yaa import exit_codes as exit_codes

# Setting up the private logger, only used for warnings and errors, should not be muted, ever.
__logger_config = yaa.get_logger("config", logging.WARNING)
# __logger_config.setLevel(logging.DEBUG) # (Only used when debugging specific errors)

# Reading and validating the 'YAA_CONFIG_PATH' environment variable
__CONFIG_PATH_DEFAULT = "./config.json"
CONFIG_PATH = os.getenv("YAA_CONFIG_PATH", __CONFIG_PATH_DEFAULT)

# Reading and validating the 'YAA_ALLOW_ROOT' environment variable
ALLOW_ROOT = os.getenv("YAA_ALLOW_ROOT", "1")
if ALLOW_ROOT in ["0", "1"]:
    ALLOW_ROOT = bool(int(ALLOW_ROOT))
else:
    ALLOW_ROOT = True
    __logger_config.error("The 'YAA_ALLOW_ROOT' environment variable is not set to '1' or '0' !")

# Reading and validating the 'YAA_ALLOW_RAW_PARAMETERS' environment variable
# Not used for the moment since the quality argument is still vulnerable to command injection attacks.
# ALLOW_RAW_PARAMETERS = os.getenv("YAA_ALLOW_RAW_PARAMETERS", "1")
# if ALLOW_RAW_PARAMETERS in ["0", "1"]:
#     ALLOW_RAW_PARAMETERS = bool(int(ALLOW_RAW_PARAMETERS))
# else:
#     ALLOW_RAW_PARAMETERS = True
#     __logger_config.error("The 'YAA_ALLOW_RAW_PARAMETERS' environment variable is not set to '1' or '0' !")

DEFAULT_DELAY_MS_METADATA_DOWNLOAD = 30000
DEFAULT_APPLICATION_ROOT_OUTPUT_DIRECTORY = "./data"
DEFAULT_YOUTUBE_MAIN_OUTPUT_DIRECTORY = "./youtube"

DEFAULT_LOGGER_LEVEL_APPLICATION = logging.DEBUG
DEFAULT_LOGGER_LEVEL_WORKER = logging.DEBUG
DEFAULT_LOGGER_LEVEL_THREAD = logging.DEBUG

config: dict = dict()


def load(config_path: str = CONFIG_PATH) -> None:
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
    
    # Quickly checking if the config file is outdated. (v0.4.0 or older)
    if "application" in config:
        if "base_output_dir" in config["application"]:
            __logger_config.error("Please update you config file !")
            __logger_config.error("It is still using the format for the 0.4.0 version of the application !")
            __logger_config.error("Once you remove the 'application.base_output_dir' field, this error will go away !")
            sys.exit(exit_codes.ERROR_OUTDATED_CONFIG)


def get_config_value(default_value: Union[str, int, float, None, list, dict, bool],
                     *args: Union[str, list[str], tuple]) -> Union[str, int, float, None, list, dict, bool]:
    """
    Returns the value, or the default value, of one of the fields in the config file.
    
    :param default_value: Value to return in case the filed could not be found.
    :param args: Location of the field in the config file as a list of strings.
    :return: The desired or default value.
    """
    current_config_section = config
    
    if args is None:
        raise ValueError("The config requested is None !")
    
    if len(args) <= 0:
        raise ValueError("No config path given !")
    
    if config is None:
        __logger_config.warning("You requested a value while the config is not loaded !")
        return default_value
    
    if type(args[0]) is list:
        args = tuple(args[0])
    
    if type(args[0]) is tuple:
        args = args[0]
    
    for config_key in args:
        if type(config_key) is not str:
            raise ValueError("One of the config keys is not a string !")
        if config_key in current_config_section:
            __logger_config.debug("Found config key: {}".format(config_key))
            current_config_section = current_config_section[config_key]
        else:
            __logger_config.debug("Returning default value early !")
            return default_value
    
    return current_config_section


def get_root_data_dir() -> str:
    """
    Get the absolute path for any file storage task.
    
    :return: Absolute path to the root folder used for any file storage task.
    """
    return os.path.abspath(
        get_config_value(DEFAULT_APPLICATION_ROOT_OUTPUT_DIRECTORY, ["application", "root_output_dir"]))


def get_youtube_basedir() -> str:
    """
    Get the absolute path for any YouTube-related file storage task.
    
    :return: Absolute path to the root directory for YouTube-related file storage task.
    """
    return os.path.abspath(os.path.join(
        get_root_data_dir(),
        get_config_value(DEFAULT_YOUTUBE_MAIN_OUTPUT_DIRECTORY, ["youtube", "output_subdir"])
    ))


def get_youtube_live_metadata_delay_ms() -> int:
    """
    Retrieves the delay in milliseconds between the start of a live downloader thread and the moment it attempts to
    download its thumbnail and description.
    
    :return: The amount of time to wait in milliseconds.
    """
    if "youtube" in config:
        if "delay_ms_metadata_download" in config["youtube"]:
            return config["youtube"]["delay_ms_metadata_download"]
    return DEFAULT_DELAY_MS_METADATA_DOWNLOAD
