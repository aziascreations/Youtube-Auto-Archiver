#!/usr/local/bin/python

# Imports
import os
import signal
import sys
import time
from typing import Union

import yaa.exit_codes as exit_codes
from yaa.config import load_config_from_file
from yaa.logger import get_logger
from yaa.data.youtube import YouTubeChannel


# Globals
is_end_signal_raised = False
channels: list[YouTubeChannel] = list()


# Application's code
# > Loading the config
try:
    config = load_config_from_file("")
except IOError as err:
    print("Fatal error: Failed to load the config file !")
    print(err)
    sys.exit(exit_codes.ERROR_CONFIG_INVALID_PATH)
except ValueError as err:
    print("Fatal error: Failed to parse the config file !")
    print(err)
    sys.exit(exit_codes.ERROR_CONFIG_PARSING_FAILURE)

# > Preparing the config and logger
logger = get_logger("main", config.logs.level_main_script, config.logs.log_format, config.logs.log_date_format)

# > Printing the logs header
if config.logs.print_header:
    logger.info("          \033[36m_   \033[94m__  \033[36m_\033[39m")
    logger.info("     \033[96m_  \033[36m_// \033[94m/\\\\ \\ \033[36m\\\\_  \033[96m_\033[39m")
    logger.info("   \033[96m_// \033[36m/ / \033[94m/ /_\\ \\ \033[36m\\ \\ \033[96m\\\\_\033[39m")
    logger.info("  \033[96m/ / \033[36m/ / \033[94m/ ___\\\\ \\ \033[36m\\ \\ \033[96m\\ \\\033[39m")
    logger.info(" \033[96m/_/ \033[36m/_/ \033[94m/_/     \033[94m\\_\\ \033[36m\\_\\ \033[96m\\_\\\033[39m")
    logger.info("\033[36m-\033[94m===========================\033[36m-\033[39m")
    logger.info("    \033[36mYoutube-Auto-Archiver\033[39m")
    logger.info("\033[36m-\033[94m===========================\033[36m-\033[39m")

# > Checking if the application is running as 'root'.
if hasattr(os, "getuid"):
    if os.getuid() == 0:
        if config.allow_running_as_root:
            logger.warning("This application is running as 'root',"
                           " you should change the UID and GUID for safety reason !")
        else:
            logger.error("The application is running as 'root' ! (UID==0)")
            sys.exit(exit_codes.ERROR_RUNNING_AS_ROOT)
    else:
        logger.debug("This application isn't running as root, continuing normally...")
elif not config.skip_if_no_get_uid:
    logger.error("The 'os.getuid' method couldn't be found and is required as per the config !")
    sys.exit(exit_codes.ERROR_NO_OS_GETUID)
else:
    logger.warning("This application may be running as root or Administrator, 'os.getuid' wasn't available to check !")

# > Changing the CWD to app.py's location.
# !> This step is mainly done for Docker since I couldn't be bothered to write a bash script for the entrypoint.
logger.info("Correcting CWD...")
try:
    logger.debug("* Original: '{}'".format(os.getcwd()))
    logger.debug("* Final: '{}'".format(os.path.dirname(os.path.realpath(__file__))))
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
except Exception as err:
    logger.error("Failed to change the current working directory !")
    logger.error(err)
    sys.exit(exit_codes.ERROR_CWD_FAILURE)




# > Printing the logs footer
if config.logs.print_footer:
    logger.info("Goodbye !")
    logger.info("\033[36m-\033[94m===========================\033[36m-\033[39m")
    logger.info(" \033[96m\\_\\ \033[36m\\_\\             \033[36m/_/ \033[96m/_/\033[39m")

# > Exiting properly
sys.exit(exit_codes.NO_ERROR)
