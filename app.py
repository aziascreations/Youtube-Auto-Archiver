#!/usr/local/bin/python

# Imports
import os
import signal
import sys
import time

import azias
import azias.config as config
import azias.youtube as yt
import azias.youtube.workers as yt_workers
import azias.exit_codes as exit_codes


# Constants
CONFIG_PATH = "./config.json"


# Globals
is_end_signal_raised = False


# Code
logger = azias.get_logger("main", config.current_logger_level_generic)
logger.info("##################################")
logger.info("# Youtube-Auto-Archiver - v0.2.0 #")
logger.info("##################################")

# Changing CWD to app.py's location (Mainly done for Docker)
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
    config.load(CONFIG_PATH)
except OSError as err:
    logger.error("Failed to load the config file !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CONFIG_OS_ERROR)
except Exception as err:
    logger.error("Failed to parse the config file !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CONFIG_JSON_ERROR)
logger.setLevel(config.current_logger_level_generic)
logger.debug("Config loaded: {}".format(config.json.dumps(config.config)))

# Parsing the config file
logger.info("Parsing the YouTube channels...")
for channel in config.config["youtube"]["channels"]:
    logger.debug("Registering '{}'".format(channel["name"]))
    yt.channels.append(yt.Channel(**channel))

logger.info("Preparing the YouTube Workers...")
for channel in yt.channels:
    if channel.check_live and channel.interval_ms_live != -1:
        logger.debug("Adding live worker for '{}'".format(channel.name))
        channel.worker_live = yt_workers.create_live_worker(channel)
        pass
    if channel.check_upload and channel.interval_ms_upload != -1:
        logger.debug("Adding upload worker for '{}'".format(channel.name))
        # channel.worker_upload =
        pass

logger.info("Preparing the output folder structure...")
try:
    os.makedirs(config.get_basedir(), exist_ok=True)
    os.makedirs(config.get_youtube_basedir(), exist_ok=True)
    for yt_channel in yt.channels:
        os.makedirs(yt_channel.get_output_path(), exist_ok=True)
except OSError as err:
    logger.error("Failed to create some of the required folders !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_MKDIR_FAILURE)


def sigint_term_handler(sig, frame):
    logger.info('SIGINT or SIGTREM received !')
    logger.debug('Setting the global kill-switch and waiting for main loop !')
    global is_end_signal_raised
    is_end_signal_raised = True


logger.info("Registering SIG handlers...")
signal.signal(signal.SIGINT, sigint_term_handler)
signal.signal(signal.SIGTERM, sigint_term_handler)

logger.info("Entering main loop...")
while True:
    for channel in yt.channels:
        if channel.check_live and channel.interval_ms_live != -1:
            if channel.should_run_worker_live() and channel.worker_live is not None:
                logger.debug("Running worker => {}".format(channel.worker_live.name))
                channel.worker_live.run()
    
    time.sleep(1)
    
    if is_end_signal_raised:
        logger.debug("Exit requested via signals, breaking the loop !")
        break

logger.info("Goodbye !")
sys.exit(exit_codes.NO_ERROR)
