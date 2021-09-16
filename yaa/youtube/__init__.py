import logging
import os
import time
from typing import Union

import yaa
import yaa.config as config
from yaa.worker import Worker


class Channel:
    internal_id: str
    channel_id: str
    name: str
    
    output_subdir: str
    
    check_live: bool
    check_upload: bool
    
    interval_ms_live: int
    interval_ms_upload: int
    
    worker_live: Union[Worker, None]
    worker_upload: Union[Worker, None]
    
    quality_live: str
    quality_upload: str
    
    backlog_days_upload: int
    
    break_on_existing: bool
    break_on_reject: bool
    
    yt_dlp_extra_args: str
    
    allow_upload_while_live: bool
    
    logger: logging.Logger
    
    check_live_last_timestamp: float
    check_live_ongoing: bool
    check_upload_last_timestamp: float
    check_upload_ongoing: bool
    
    def __init__(self, internal_id, channel_id, name=None, output_subdir=None, check_live=False, check_upload=False,
                 interval_ms_live=-1, interval_ms_upload=-1, quality_live="best", quality_upload="best",
                 backlog_days_upload=7, break_on_existing=True, break_on_reject=True, yt_dlp_extra_args="",
                 allow_upload_while_live=True, **kwargs):
        self.internal_id = internal_id
        self.channel_id = channel_id
        
        self.name = (name if name is not None else internal_id)
        self.output_subdir = (output_subdir if output_subdir is not None else internal_id)
        
        self.check_live = check_live
        self.check_upload = check_upload
        self.interval_ms_live = interval_ms_live
        self.interval_ms_upload = interval_ms_upload
        self.check_live_last_timestamp = time.time()
        self.check_live_ongoing = False
        self.check_upload_last_timestamp = time.time()
        self.check_upload_ongoing = False
        self.quality_live = quality_live
        self.quality_upload = quality_upload
        self.backlog_days_upload = backlog_days_upload
        self.break_on_existing = break_on_existing
        self.break_on_reject = break_on_reject
        self.yt_dlp_extra_args = yt_dlp_extra_args
        self.allow_upload_while_live = allow_upload_while_live
        
        # Preparing the worker's logger.
        self.logger = yaa.get_logger(
            "yt-" + internal_id,
            config.get_config_value(
                config.DEFAULT_LOGGER_LEVEL_APPLICATION,
                ["application", "logging_level_main"]
            )
        )
        
        # Checking if any unhandled keyword was given as an argument.
        for key, value in kwargs.items():
            self.logger.warning("Unhandled keyword parameter used when creating a channel: {} => {}".format(
                key, value))
    
    def get_output_path(self) -> str:
        """
        Get the output path for the current channel for any file storage task.
        
        :return: Output path for the current channel for any file storage task.
        """
        return os.path.join(config.get_youtube_basedir(), self.output_subdir)
    
    def should_run_worker_live(self) -> bool:
        """
        Returns a boolean indicating whether or not the live thread should run.
        
        :return: True if the live thread should run, False otherwise.
        """
        if (not self.check_live) or self.interval_ms_live == -1:
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
        
        if time.time() > self.check_live_last_timestamp + (self.interval_ms_live / 1000):
            self.check_live_last_timestamp = time.time()
            self.logger.debug("Worker run")
            return True

        self.logger.debug("No worker run: not enough time passed ({:.1f}s vs {:.1f}s)".format(
            time.time() - self.check_live_last_timestamp,
            self.interval_ms_live / 1000
        ))
        return False
    
    def should_run_worker_upload(self) -> bool:
        """
        Returns a boolean indicating whether or not the upload thread should run.
        
        :return: True if the upload thread should run, False otherwise.
        """
        if (not self.check_upload) or self.interval_ms_upload == -1:
            self.logger.debug("No worker run: disabled")
            return False
        
        if self.worker_upload is not None:
            if self.worker_upload.is_running():
                self.logger.debug("No worker run: ongoing")
                self.check_upload_ongoing = True
                return False
        
        if self.check_upload_ongoing:
            # The thread is no longer running but was during the last check.
            self.check_upload_ongoing = False
            self.check_upload_last_timestamp = time.time()
            self.logger.debug("No worker run: was ongoing")
            return False
        
        if time.time() > self.check_upload_last_timestamp + (self.interval_ms_upload / 1000):
            self.check_upload_last_timestamp = time.time()
            self.logger.debug("Worker run")
            return True
        
        self.logger.debug("No worker run: not enough time passed ({:.1f}s vs {:.1f}s)".format(
            time.time() - self.check_upload_last_timestamp,
            self.interval_ms_upload / 1000
        ))
        return False


channels: list[Channel] = list()
""" List of instantiated and registered Channel objects. """
