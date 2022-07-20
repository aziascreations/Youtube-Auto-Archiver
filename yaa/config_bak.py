# Imports
import json
import logging
import os
import sys

from . import logger, exit_codes

from dataclasses import dataclass, field

# Globals
__logger_config = logger.get_logger("config")

# Constants
CONFIG_PATH_DEFAULT = os.getenv("YAA_CONFIG_PATH", "./config.json")
# TODO: Add an env var for this constant for 0.8.0
DEFAULT_LOGGER_LEVEL_APPLICATION = logging.DEBUG
DEFAULT_LOGGER_LEVEL_WORKER = logging.DEBUG
DEFAULT_LOGGER_LEVEL_THREAD = logging.DEBUG


# Classes
@dataclass
class ConfigApplication:
    """Config fields related to the application itself."""
    
    root_output_dir: str = "./data"
    """Root directory where the downloaded data should be stored in."""
    
    logging_level_main: int = 10
    """
    Logging level for the main app.
    See Python's documentation for more information
    """
    
    auto_shutdown_after_ms: int = -1
    """
    Delay in milliseconds after which the application should automatically exit with a return code of 0.
    This can be used to restart containers and clean potential memory leaks.
    """
    
    auto_shutdown_do_wait_for_workers: bool = True
    """
    Indicates whether or not the application should wait for all worker's thread to finish without sending a SIGINT or SIGTERM signal back to them after the countdown was reached.
    If set to False, the application will forcefully kill these threads which could lead to a loss or corruption of data.
    No new threads will be launched while the main loop waits for all threads to be finished with there work.
    """
    
    auto_shutdown_number_to_send: int = -1
    """
    Indicates which signal should be send to threads if auto_shutdown_do_wait_for_workers is set to False.
    Allowed values are -1, SIGINT (2) and SIGTERM (15).
    If it is set to an incorrect value, or to -1, it will automatically be set to SIGTERM (15) and will be said in the debug-level logs.
    """
    
    signal_shutdown_do_wait_for_workers: bool = False
    """
    Indicates whether or not the application should wait for all worker's thread to finish without sending a SIGINT or SIGTERM signal back to them after receiving a shutdown signal.
    If set to False, the application will forcefully kill these threads which could lead to a loss or corruption of data.
    No new threads will be launched while the main loop waits for all threads to be finished with there work.
    """


@dataclass
class ConfigYoutubeChannel:
    internal_id: str
    """Arbitrary string used in downloaded files and loggers' names."""
    
    channel_id: str
    """Id of the relevant YouTube channel."""
    
    # FIXME: Find a way to make it equal to 'internal_id'
    name: str
    """Friendly name used in logging only."""
    
    # FIXME: Find a way to make it equal to './{internal_id}'
    output_subdir: str
    """
    Directory in which all the files for this channel are downloaded into.
    Appended to application.root_output_dir and youtube.output_subdir.
    """
    
    live_subdir: str = "./livestreams"
    """
    Directory in which all the livestream files for this channel are downloaded into.
    Appended to application.root_output_dir, youtube.output_subdir and youtube.{channel}.output_subdir.
    """
    
    upload_subdir: str = "./uploads"
    """
    Directory in which all the upload files for this channel are downloaded into.
    Appended to application.root_output_dir, youtube.output_subdir and youtube.{channel}.output_subdir.
    """
    
    check_live: bool = False
    """Toggles the live downloading worker and threads."""
    
    check_upload: bool = False
    """Toggles the video downloading worker and threads."""
    
    interval_ms_live: int = -1
    """
    Delay in ms between each verification of the channel to see if it is livestreaming.
    Will disable the functionality if set to -1.
    """
    
    interval_ms_upload: int = -1
    """
    Delay in ms between each verification of the channel to see if it is livestreaming.
    Will disable the functionality if set to -1.
    """
    
    quality_live: str = "best"
    """Quality setting used in streamlink when downloading a live."""
    
    quality_upload: str = "best"
    """Quality setting used in yt-dlp with the -f option."""
    
    backlog_days_upload: int = 7
    """
    Number of days to look back to for uploads
    Added as-is in the --dateafter now-Xdays option where X is the number of days given here.
    """
    
    break_on_existing: bool = True
    """Indicates if yt-dlp should stop downloading uploads when encountering an existing completed download."""
    
    break_on_reject: bool = True
    """Indicates if yt-dlp should stop downloading uploads when encountering a filtered video."""
    
    yt_dlp_extra_args: str = ""
    """Extra args added as-is to the yt-dlp command right before the channel URL."""
    
    allow_upload_while_live: bool = True
    """Indicates whether yt-dlp can download videos while a live worker is running for the given channel."""


@dataclass
class ConfigYoutube:
    """Config fields related to all YouTube-centric tasks."""
    
    output_subdir: str = "./youtube"
    """
    Directory in which all YouTube related downloads are stored.
    Appended to application.root_output_dir.
    """
    
    delay_ms_metadata_download: int = 30000
    """
    Delay in ms between the start of a live downloader thread and the moment it attempts to download its thumbnail and description.
    Can be disabled if set to -1.
    """
    
    logging_level_worker: int = 10
    """
    Logging level for all YouTube-related workers.
    See Python's documentation for more information
    """
    
    logging_level_thread: int = 10
    """
    Logging level for all YouTube-related threads.
    See Python's documentation for more information
    """
    
    channels: list[ConfigYoutubeChannel] = field(default_factory=lambda: [])
    """List of channels' info for the workers"""


@dataclass
class ConfigRoot:
    """Main class that contains all the application's config"""
    
    application: ConfigApplication = ConfigApplication()
    """Contains the configs that are use globally by the application."""
    
    youtube: ConfigYoutube = ConfigYoutube()
    """Contains the configs for the YouTube related part of the application."""
    
    def get_root_data_dir(self) -> str:
        """
        Get the absolute path for any file storage task.
        
        :return: Absolute path to the root folder used for any file storage task.
        """
        return os.path.abspath(self.application.root_output_dir)
    
    def get_youtube_basedir(self) -> str:
        """
        Get the absolute path for any YouTube-related file storage task.
        
        :return: Absolute path to the root directory for YouTube-related file storage task.
        """
        return os.path.abspath(os.path.join(self.get_root_data_dir(), self.youtube.output_subdir))


# Methods
def load_config(config_path: str = CONFIG_PATH_DEFAULT) -> ConfigRoot:
    """
    Reads the given config file and returns a proper config object.
    
    :param config_path: Path to the config file.
    :return: The parsed config file.
    :raises IOError: If the config file couldn't be found.
    :raises IOError: If the config file couldn't be found.
    """
    
    if not os.path.exists(config_path):
        raise IOError("The config file '{}' could not be found !".format(config_path))
    
    with open(config_path, "r") as f:
        _raw_config = json.load(f)
    
    # Quickly checking if the config file is outdated. (v0.4.0 or older)
    if "application" in _raw_config:
        if "base_output_dir" in _raw_config["application"]:
            __logger_config.error("Please update you config file !")
            __logger_config.error("It is still using the format for the 0.4.0 version of the application !")
            __logger_config.error("Once you remove the 'application.base_output_dir' field, this error will go away !")
            sys.exit(exit_codes.ERROR_OUTDATED_CONFIG)
    
    config = ConfigRoot(**_raw_config)
    config.application = ConfigApplication(**config.application)
    config.youtube = ConfigYoutube(**config.youtube)
    config.youtube.channels = [ConfigYoutubeChannel(**x) for x in config.youtube.channels]
    
    return config
