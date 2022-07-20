# Imports
from dataclasses import dataclass, asdict, field
import logging
import json
import os
import pathlib
from typing import Optional

import toml
import yaml


# Constants
CURRENT_VERSION_NUMBER = 1


# Classes
@dataclass
class ConfigLoggerShared:
    """Any log-related configs."""
    
    log_format: str = "[%(asctime)s] [%(name)s/%(levelname).3s]: %(message)s"
    """Logging format used for every logger."""
    
    log_date_format: str = "%H:%M:%S"
    """Time format used for every logger."""
    
    level_main_script: int = logging.INFO
    """Used by the main script that sets up everything else."""
    
    level_web_setup: int = logging.INFO
    """Used during the setup and exiting steps of Flask."""
    
    print_header: bool = True
    """???"""
    
    print_footer: bool = True
    """???"""


@dataclass
class ConfigWebInterface:
    """Web interface's configs."""
    
    enable: bool = False
    """Whether or not the web interface should be enabled, loaded and started."""
    
    host: str = "127.0.0.1"
    """Which host the web server should bind itself to."""
    
    port: int = 8080
    """Which port the web server should use."""


@dataclass
class ConfigYoutubeChannelUploads:
    """???"""
    
    enable: bool = False
    """Toggles the video downloading worker and threads."""


@dataclass
class ConfigYoutubeChannelLivestreams:
    """???"""
    
    enable: bool = False
    """Toggles the livestream downloading worker and threads."""


@dataclass
class ConfigYoutubeChannel:
    """Config fields related to a single channel."""
    
    internal_id: str
    """Arbitrary string used in downloaded files and loggers' names."""
    
    channel_id: str
    """Id of the relevant YouTube channel."""
    
    friendly_name: Optional[str] = None
    """Friendly name used in logging to identify the channel more easily."""
    
    uploads: Optional[ConfigYoutubeChannelUploads] = ConfigYoutubeChannelUploads()
    """???"""
    
    livestreams: Optional[ConfigYoutubeChannelLivestreams] = ConfigYoutubeChannelLivestreams()
    """???"""
    
    # Fixing the optional fields
    def __post_init__(self):
        if self.friendly_name is None:
            self.friendly_name = self.internal_id
            
        if self.uploads is None:
            self.uploads = ConfigYoutubeChannelUploads()
            
        if self.livestreams is None:
            self.livestreams = ConfigYoutubeChannelLivestreams()
            
        if type(self.uploads) is dict:
            self.uploads: dict
            self.uploads = ConfigYoutubeChannelUploads(**self.uploads)
            
        if type(self.livestreams) is dict:
            self.livestreams: dict
            self.livestreams = ConfigYoutubeChannelLivestreams(**self.livestreams)


@dataclass
class ConfigYoutube:
    """Config fields related to all YouTube-centric tasks."""
    
    common_output_subdir: str = "youtube"
    """
    Sub-directory in which all YouTube related downloads are stored.
    Appended to 'base_output_dir'.
    """
    
    uploads_output_directory: str = "uploads"
    """???"""
    
    livestreams_output_directory: str = "livestreams"
    """???"""
    
    channels: Optional[list[ConfigYoutubeChannel]] = field(default_factory=lambda: [])
    """???"""
    
    # Fixing the optional fields & dataclasses
    def __post_init__(self):
        if self.channels is None:
            self.channels = list()
        
        # FIXME: Parse the channels !


@dataclass
class ConfigRoot:
    """Main class that contains all the application's config"""
    
    version: int = CURRENT_VERSION_NUMBER
    """
    Number representing the current version of the config file.
    Will be incremented everytime breaking changes occur.
    """
    
    base_output_dir: str = "./data"
    """Directory where all other sub-dirs will be contained."""
    
    allow_running_as_root: bool = False
    """Whether the application should be able to run as root."""
    
    skip_if_no_get_uid: bool = True
    """
    Skips the root user process check if 'os.getuid' is not available.
    A warning will be shown if True, an error will be show instead if False.
    """
    
    web: ConfigWebInterface = ConfigWebInterface()
    """Web interface's configs."""
    
    logs: ConfigLoggerShared = ConfigLoggerShared()
    """Any log-related configs."""
    
    youtube: ConfigYoutube = ConfigYoutube()
    """Config fields related to all YouTube-centric tasks."""
    
    # Fixing the optional fields & dataclasses
    def __post_init__(self):
        if type(self.web) is dict:
            self.web: dict
            self.web = ConfigWebInterface(**self.web)
            
        if type(self.logs) is dict:
            self.logs: dict
            self.logs = ConfigLoggerShared(**self.logs)
            
        if type(self.youtube) is dict:
            self.youtube: dict
            self.youtube = ConfigYoutube(**self.youtube)


# Methods
def load_config_from_dict(raw_data: dict) -> ConfigRoot:
    return ConfigRoot(**raw_data)


def load_config_from_file(file_path: str) -> ConfigRoot:
    if not os.path.exists(file_path):
        raise IOError("The path '{}' given as '{}' doesn't exist !".format(os.path.abspath(file_path), file_path))
    
    if not os.path.isfile(file_path):
        raise IOError("The path '{}' given as '{}' isn't a file !".format(os.path.abspath(file_path), file_path))
    
    with open(file_path, "rb") as f:
        config_raw_data = f.read().decode("utf-8")
    
    try:
        match pathlib.Path(file_path).suffix:
            case ".json":
                return load_config_from_dict(json.loads(config_raw_data))
            case ".toml":
                return load_config_from_dict(toml.loads(config_raw_data))
            case ".yaml" | ".yml":
                return load_config_from_dict(yaml.safe_load(config_raw_data))
    except Exception as err:
        raise ValueError(err)
    
    raise IOError("The file '{}' isn't using a supported extension, got '{}' !".format(
        file_path, pathlib.Path('yourPath.example').suffix
    ))


def export_config_to_json(config: ConfigRoot) -> str:
    return json.dumps(asdict(config), indent=4)


def export_config_to_toml(config: ConfigRoot) -> str:
    return toml.dumps(asdict(config))


def export_config_to_yaml(config: ConfigRoot) -> str:
    return yaml.dump(asdict(config))


# Tests
if __name__ == "__main__":
    """
    _config = ConfigRoot()
    _config.youtube.channels.append(
        ConfigYoutubeChannel(internal_id="test", channel_id="123456")
    )
    _config.youtube.channels.append(
        ConfigYoutubeChannel(internal_id="joe_mama", channel_id="abc789")
    )
    
    print("#"*25)
    print(export_config_to_json(_config))
    print("#"*25)
    print(export_config_to_toml(_config))
    print("#"*25)
    print(export_config_to_yaml(_config))
    print("#"*25)
    """

    print("#"*25)
    config_json = load_config_from_file("../data/test.json")
    print(type(config_json))
    print(type(config_json.youtube))
    print(config_json.youtube)
    
    print("#"*25)
    config_toml = load_config_from_file("../data/test.toml")
    print(type(config_toml))
    print(type(config_toml.youtube))
    print(config_toml)
    
    print("#"*25)
    config_yaml = load_config_from_file("../data/test.yaml")
    print(type(config_yaml))
    print(type(config_yaml.youtube))
    print(config_yaml.youtube)
    
    print("#"*25)
