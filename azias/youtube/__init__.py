import logging
import os
import time

import azias
import azias.config as config
from azias.worker import Worker


class Channel:
    internal_id: str
    channel_id: str
    name: str
    output_subdir: str
    check_live: bool
    check_upload: bool
    interval_ms_live: int
    interval_ms_upload: int
    
    worker_live: Worker
    worker_upload: Worker
    # Not implemented yet
    # worker_ids: Worker

    check_live_last_timestamp: float
    check_live_ongoing: bool
    check_upload_last_timestamp: float
    check_upload_ongoing: bool
    
    quality_live: str
    
    logger: logging.Logger
    
    def __init__(self, internal_id, channel_id, name, output_subdir, check_live, check_upload, interval_ms_live,
                 interval_ms_upload, quality_live):
        self.internal_id = internal_id
        self.channel_id = channel_id
        self.name = name
        self.output_subdir = output_subdir
        self.check_live = check_live
        self.check_upload = check_upload
        self.interval_ms_live = interval_ms_live
        self.interval_ms_upload = interval_ms_upload
        self.check_live_last_timestamp = time.time()
        self.check_live_ongoing = False
        self.check_upload_last_timestamp = time.time()
        self.check_upload_ongoing = False
        self.quality_live = quality_live
        self.logger = azias.get_logger("yt-"+internal_id, config.current_logger_level_youtube)
        
    def get_output_path(self) -> str:
        return os.path.join(config.get_youtube_basedir(), self.output_subdir)
    
    def should_run_worker_live(self) -> bool:
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


channels: list[Channel] = list()
