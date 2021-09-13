#!/usr/local/bin/python
import os
import signal
import sys
import time
from typing import Union

import yaa
import yaa.config as config
import yaa.exit_codes as exit_codes
from yaa.version import __version__ as version
import yaa.youtube as yt
import yaa.youtube.workers as yt_workers

# Globals
is_end_signal_raised = False
channel: Union[dict, yt.Channel]

# Code
logger = yaa.get_logger("main", config.DEFAULT_LOGGER_LEVEL_APPLICATION)
logger.info("#############################{}".format("#"*len(version)))
logger.info("# Youtube-Auto-Archiver - v{} #".format(version))
logger.info("#############################{}".format("#"*len(version)))

# Check to see if the application is running as 'root'.
if hasattr(os, "getuid"):
    if os.getuid() == 0:
        if config.ALLOW_ROOT:
            logger.warning("This application is running as 'root',"
                           " you should change the UID and GUID for safety reason !")
        else:
            logger.error("The application is running as 'root' ! (UID==0)")
            sys.exit(exit_codes.ERROR_RUNNING_AS_ROOT)

# Changing CWD to app.py's location. (Mainly done for Docker since I couldn't be bothered to write a bash script for it)
logger.info("Correcting CWD...")
try:
    logger.debug("Going from '{}' to '{}'".format(os.getcwd(), os.path.dirname(os.path.realpath(__file__))))
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
except Exception as err:
    logger.error("Failed to change the current working directory !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CWD_FAILURE)

# Loading the config file (Soft link used in Docker)
logger.info("Loading config file...")
try:
    config.load()
except OSError as err:
    logger.error("Failed to load the config file !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CONFIG_OS_ERROR)
except Exception as err:
    logger.error("Failed to parse the config file !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CONFIG_JSON_ERROR)
logger.setLevel(config.get_config_value(10, ["application", "logging_level_main"]))
logger.debug("Config loaded: {}".format(config.json.dumps(config.config)))

# Parsing the config file
logger.info("Parsing the YouTube channels...")
for channel in config.get_config_value([], ["youtube", "channels"]):
    channel["name"] = (channel["name"] if "name" in channel else channel["internal_id"])
    logger.debug("Registering '{}'".format(channel["name"]))
    yt.channels.append(yt.Channel(**channel))

logger.info("Preparing the YouTube Workers for {} channel{}...".format(
    len(yt.channels), ("s" if len(yt.channels) > 1 else "")))
for channel in yt.channels:
    if channel.check_live and channel.interval_ms_live != -1:
        logger.debug("Adding live worker for '{}'".format(channel.name))
        channel.worker_live = yt_workers.create_live_worker(channel)
        pass
    if channel.check_upload and channel.interval_ms_upload != -1:
        logger.debug("Adding upload worker for '{}'".format(channel.name))
        channel.worker_upload = yt_workers.create_upload_worker(channel)
        pass

logger.info("Preparing the output folder structure...")
try:
    os.makedirs(config.get_root_data_dir(), exist_ok=True)
    os.makedirs(config.get_youtube_basedir(), exist_ok=True)
    for yt_channel in yt.channels:
        os.makedirs(yt_channel.get_output_path(), exist_ok=True)
except OSError as err:
    logger.error("Failed to create some of the required folders !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_MKDIR_FAILURE)


def sigint_term_handler(sig, frame):
    logger.info('SIGINT or SIGTERM received !')
    logger.debug('Setting the global kill-switch and waiting for main loop !')
    global is_end_signal_raised
    is_end_signal_raised = True


logger.info("Registering SIG handlers...")
signal.signal(signal.SIGINT, sigint_term_handler)
signal.signal(signal.SIGTERM, sigint_term_handler)

logger.info("Entering main loop...")
while True:
    for channel in yt.channels:
        # Checking if a "live" worker can and should run
        if channel.check_live and channel.interval_ms_live != -1:
            if channel.should_run_worker_live() and channel.worker_live is not None:
                logger.debug("Running worker => {}".format(channel.worker_live.name))
                channel.worker_live.run()
        
        # Checking if a "upload" worker can and should run
        if channel.check_upload and channel.interval_ms_live != -1:
            if channel.should_run_worker_upload() and channel.worker_upload is not None:
                # Checking if a live is running before running the worker
                if channel.allow_upload_while_live:
                    logger.debug("Running worker [c1] => {}".format(channel.worker_upload.name))
                    channel.worker_upload.run()
                elif not channel.worker_live.is_running():
                    logger.debug("Running worker [c2] => {}".format(channel.worker_upload.name))
                    channel.worker_upload.run()
                else:
                    logger.info("Not running '{}' due to an ongoing live !".format(channel.worker_upload.name))
    
    time.sleep(1)
    
    if is_end_signal_raised:
        logger.debug("Exit requested via signals, breaking the loop !")
        break

logger.info("Goodbye !")
sys.exit(exit_codes.NO_ERROR)
