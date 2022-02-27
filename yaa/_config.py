import logging

DEFAULT_DELAY_MS_METADATA_DOWNLOAD = 30000
DEFAULT_APPLICATION_ROOT_OUTPUT_DIRECTORY = "./data"
DEFAULT_YOUTUBE_MAIN_OUTPUT_DIRECTORY = "./youtube"

DEFAULT_LOGGER_LEVEL_APPLICATION = logging.DEBUG
DEFAULT_LOGGER_LEVEL_WORKER = logging.DEBUG
DEFAULT_LOGGER_LEVEL_THREAD = logging.DEBUG

# def get_youtube_live_metadata_delay_ms() -> int:
#     """
#     Retrieves the delay in milliseconds between the start of a live downloader thread and the moment it attempts to
#     download its thumbnail and description.
#
#     :return: The amount of time to wait in milliseconds.
#     """
#     if "youtube" in config:
#         if "delay_ms_metadata_download" in config["youtube"]:
#             return config["youtube"]["delay_ms_metadata_download"]
#     return DEFAULT_DELAY_MS_METADATA_DOWNLOAD
