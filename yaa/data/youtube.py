# Imports
import logging
import os
import time
from typing import Union

from yaa.config import ConfigRoot, ConfigYoutubeChannel
from yaa.logger import get_logger
from yaa.workers.worker import Worker


# Classes
class YouTubeChannel:
    """
    This class represents a YouTube channel on a higher level than the config file's 'ConfigYoutubeChannel' object.

    It is used by workers to access the config and any channel-related info.
    """
    
    channel_config: ConfigYoutubeChannel
    """Channel config this object is attached to"""
    
    worker_live: Union[Worker, None]
    """
    Worker that handles any livestream-related task.
    Left to None if no checks and downloads should be done.
    """
    
    worker_upload: Union[Worker, None]
    """
    Worker that handles any upload-related task.
    Left to None if no checks and downloads should be done.
    """
    
    logger: logging.Logger
    """Logger used by the Channel class."""
    
    check_live_last_timestamp: float
    """Unix timestamp of the last time the channel was checked for an ongoing livestream."""
    
    check_live_ongoing: bool
    """
    Boolean indicating whether the livestream worker was found to be running when checking
    if the livestream worker should run.
    """
    
    check_upload_last_timestamp: float
    """Unix timestamp of the last time the channel was checked for a regular uploads."""
    
    check_upload_ongoing: bool
    """
    Boolean indicating whether the upload worker was found to be running when checking
    if the upload worker should run.
    """
    
    def __init__(self, config: ConfigRoot, channel_config: ConfigYoutubeChannel):
        self.config = config
        self.channel_config = channel_config
        self.worker_live = None
        self.worker_upload = None
        self.check_live_last_timestamp = time.time()
        self.check_live_ongoing = False
        self.check_upload_last_timestamp = time.time()
        self.check_upload_ongoing = False
        
        # Preparing the worker's logger.
        self.logger = get_logger(
            name="yt-" + self.channel_config.internal_id,
            level=self.config.application.logging_level_main
        )
    
    def get_output_path(self) -> str:
        """
        Get the output path for the current channel for any file storage task.

        :return: Output path for the current channel for any file storage task.
        """
        return os.path.join(self.config.get_youtube_basedir(), self.channel_config.output_subdir)
    
    # FIXME: Move this method elsewhere
    def should_run_worker_live(self) -> bool:
        """
        Returns a boolean indicating whether the live thread should run.

        :return: True if the live thread should run, False otherwise.
        """
        if (not self.channel_config.check_live) or self.channel_config.interval_ms_live == -1:
            self.logger.debug("No worker run: disabled")
            return False
        
        if self.worker_live is not None:
            if self.worker_live.is_running():
                self.logger.debug("No worker run: ongoing")
                self.check_live_ongoing = True
                return False
        
        if self.check_live_ongoing:
            # The thread is no longer running but was during the last check.
            self.check_live_ongoing = False
            self.check_live_last_timestamp = time.time()
            self.logger.debug("No worker run: was ongoing")
            return False
        
        if time.time() > self.check_live_last_timestamp + (self.channel_config.interval_ms_live / 1000):
            self.check_live_last_timestamp = time.time()
            self.logger.debug("Worker run")
            return True
        
        self.logger.debug("No worker run: not enough time passed ({:.1f}s vs {:.1f}s)".format(
            time.time() - self.check_live_last_timestamp,
            self.channel_config.interval_ms_live / 1000
        ))
        return False

    # FIXME: Move this method elsewhere
    def should_run_worker_upload(self) -> bool:
        """
        Returns a boolean indicating whether the upload thread should run.

        :return: True if the upload thread should run, False otherwise.
        """
        if (not self.channel_config.check_upload) or self.channel_config.interval_ms_upload == -1:
            self.logger.debug("Worker not ran: disabled")
            return False
        
        if self.worker_upload is not None:
            if self.worker_upload.is_running():
                self.logger.debug("Worker not ran: ongoing")
                self.check_upload_ongoing = True
                return False
        
        if self.check_upload_ongoing:
            # The thread is no longer running but was during the last check.
            self.check_upload_ongoing = False
            self.check_upload_last_timestamp = time.time()
            self.logger.debug("Worker not ran: was ongoing")
            return False
        
        if time.time() > self.check_upload_last_timestamp + (self.channel_config.interval_ms_upload / 1000):
            self.check_upload_last_timestamp = time.time()
            self.logger.debug("Worker run")
            return True
        
        self.logger.debug("Worker not ran: not enough time passed ({:.1f}s vs {:.1f}s)".format(
            time.time() - self.check_upload_last_timestamp,
            self.channel_config.interval_ms_upload / 1000
        ))
        return False
