#!/usr/local/bin/python

# Imports
import os
import signal
import sys
import time
from typing import Union

import yaa.config as yaa_config
import yaa.exit_codes as exit_codes
from yaa.logger import get_logger
from yaa.data.youtube import YouTubeChannel
from yaa.workers.youtube.live import create_live_worker
from yaa.workers.youtube.uploads import create_upload_worker

# Globals
is_end_signal_raised = False
channels: list[YouTubeChannel] = list()

# Application's code
# > Preparing the config and logger
logger = get_logger("main", yaa_config.DEFAULT_LOGGER_LEVEL_APPLICATION)

# > Processing the config file.
logger.info("Processing the YouTube channels...")
for channel_config in config.youtube.channels:
    channel_config.name = (channel_config.name if channel_config is not None else channel_config.internal_id)
    logger.debug("Registering '{}'".format(channel_config.name))
    channels.append(YouTubeChannel(config, channel_config))

# > Preparing the YouTube Workers.
logger.info("Preparing the YouTube Workers for {} channel{}...".format(
    len(channels), ("s" if len(channels) > 1 else "")))
for channel in channels:
    if channel.channel_config.check_live and channel.channel_config.interval_ms_live != -1:
        logger.debug("Adding live worker for '{}'".format(channel.channel_config.name))
        channel.worker_live = create_live_worker(channel)
        pass
    if channel.channel_config.check_upload and channel.channel_config.interval_ms_upload != -1:
        logger.debug("Adding upload worker for '{}'".format(channel.channel_config.name))
        channel.worker_upload = create_upload_worker(channel)
        pass

# > Preparing the output folders if needed.
logger.info("Preparing the output folder structure...")
try:
    os.makedirs(config.get_root_data_dir(), exist_ok=True)
    os.makedirs(config.get_youtube_basedir(), exist_ok=True)
    for channel in channels:
        os.makedirs(channel.get_output_path(), exist_ok=True)
        os.makedirs(channel.get_livestream_output_path(), exist_ok=True)
        os.makedirs(channel.get_uploads_output_path(), exist_ok=True)
except OSError as err:
    logger.error("Failed to create some of the required folders !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_MKDIR_FAILURE)


# > Preparing and registering the signal handler
def sigint_term_handler(sig, frame):
    logger.info('SIGINT or SIGTERM received !')
    logger.debug('Setting the global kill-switch and waiting for main loop !')
    global is_end_signal_raised
    is_end_signal_raised = True
    global end_signal_to_use
    end_signal_to_use = sig


logger.info("Registering SIG handlers...")
signal.signal(signal.SIGINT, sigint_term_handler)
signal.signal(signal.SIGTERM, sigint_term_handler)

# > Calculating the expected self shutdown time
logger.info("Finalizing some things...")
logger.debug("Calculating the expected self shutdown time")
expected_self_shutdown_time = config.application.auto_shutdown_after_ms

# FIXME: Finish this !

if type(expected_self_shutdown_time) is not int:
    logger.error("The config field 'application.auto_shutdown_after_ms' isn't an integer !")
    sys.exit(exit_codes.ERROR_INVALID_CONFIG_FIELD_TYPE)
if expected_self_shutdown_time == -1:
    expected_self_shutdown_time = float('inf')
else:
    expected_self_shutdown_time = float(expected_self_shutdown_time)

# > Preparing the self-shutdown signal number.
logger.debug("Preparing the self-shutdown signal number")
end_signal_to_use: Union[int, str] = config.application.auto_shutdown_number_to_send
if type(end_signal_to_use) is str:
    end_signal_to_use = str(end_signal_to_use)
if end_signal_to_use not in [-1, signal.SIGINT, signal.SIGTERM]:
    logger.debug("Setting the auto-shutdown signal to -1. (Invalid value -> {}:{})".format(
        type(end_signal_to_use),
        end_signal_to_use
    ))
    end_signal_to_use = -1
if end_signal_to_use == -1:
    logger.debug("Setting the auto-shutdown signal to SIGTERM. (Was set to -1)")
    end_signal_to_use = signal.SIGTERM

# > Main loop
logger.info("Entering main loop...")
logger.info("\033[36m-\033[94m===========================\033[36m-\033[39m")
while True:
    for channel in channels:
        # Checking if a "live" worker can and should run.
        if channel.channel_config.check_live and channel.channel_config.interval_ms_live != -1:
            if channel.should_run_worker_live() and channel.worker_live is not None:
                logger.debug("Running worker => {}".format(channel.worker_live.name))
                channel.worker_live.run()
        
        # Checking if an "upload" worker can and should run.
        if channel.channel_config.check_upload and channel.channel_config.interval_ms_upload != -1:
            if channel.should_run_worker_upload():
                # Checking if a live worker is running before running the upload worker.
                if channel.worker_live is not None:
                    if channel.channel_config.allow_upload_while_live:
                        logger.debug("Running worker [c1] => {}".format(channel.worker_upload.name))
                        channel.worker_upload.run()
                    elif not channel.worker_live.is_running():
                        logger.debug("Running worker [c2] => {}".format(channel.worker_upload.name))
                        channel.worker_upload.run()
                    else:
                        logger.info("Not running '{}' due to an ongoing live !".format(channel.worker_upload.name))
                else:
                    logger.info("Running worker [c3] => '{}'".format(channel.worker_upload.name))
                    channel.worker_upload.run()
    
    # Waiting a bit to avoid wasting CPU cycles.
    time.sleep(1)
    
    # Checking if the application should exit.
    if is_end_signal_raised or time.time() > expected_self_shutdown_time:
        logger.debug("Exit requested via signals or reached self-shutdown timestamp !")
        
        # Checking if the threads should be gracefully killed.
        if ((time.time() > expected_self_shutdown_time) and
            (not config.application.auto_shutdown_do_wait_for_workers)) or \
                (is_end_signal_raised and
                 (not config.application.signal_shutdown_do_wait_for_workers)):
            # Gracefully killing threads.
            for channel in channels:
                logger.debug("Sending signals to channel '{}'...".format(channel.channel_config.name))
                
                if channel.worker_upload is not None:
                    if channel.worker_upload.is_running():
                        channel.worker_upload.end_signal_to_process = end_signal_to_use
                
                if channel.worker_live is not None:
                    if channel.worker_live.is_running():
                        channel.worker_live.end_signal_to_process = end_signal_to_use
        
        # Waiting for the threads do die.
        has_found_running_threads: bool = True
        
        while has_found_running_threads:
            has_found_running_threads = False
            
            for channel in channels:
                logger.debug("Checking threads for '{}'...".format(channel.channel_config.name))
                
                if channel.worker_upload is not None:
                    if channel.worker_upload.is_running():
                        has_found_running_threads = True
                
                if channel.worker_live is not None:
                    if channel.worker_live.is_running():
                        has_found_running_threads = True
                
                if has_found_running_threads:
                    time.sleep(0.1)
                    break
        
        # Exiting the main loop
        break

# > Printing the logs footer
logger.info("Goodbye !")
logger.info("\033[36m-\033[94m===========================\033[36m-\033[39m")
logger.info(" \033[96m\\_\\ \033[36m\\_\\             \033[36m/_/ \033[96m/_/\033[39m")

# > Exiting properly
sys.exit(exit_codes.NO_ERROR)
