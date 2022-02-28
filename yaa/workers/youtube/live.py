# Imports
import os
import subprocess
import time
from typing import Union

from yaa.data.youtube import YouTubeChannel
from yaa.logger import get_logger
from yaa.workers.youtube import YouTubeWorker


# Classes
class __WorkerLive(YouTubeWorker):
    """
    Private class that is used for livestream related tasks.
    It should only be used outside this module if no other way of determining its goal is available.
    """
    
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point, channel)


# Methods
def create_live_worker(channel: YouTubeChannel) -> YouTubeWorker:
    """
    Creates a YouTubeWorker that handles and process livestreams from and for a given channel.
    
    :param channel: A YouTubeChannel object for which the live worker should be created
    :return: A YouTubeWorker object for the corresponding channel
    """
    return __WorkerLive("worker-yt-live-" + channel.channel_config.internal_id, __thread_yt_live, channel)


def __thread_yt_live(worker: YouTubeWorker, **args):
    """
    Thread method for the live worker that checks if a channel is currently livestreaming.
    Once finished, the thread sets the worker's 'last_return_code' variable with the one returned by streamlink.

    :param worker: Worker from which this thread was spawned.
    :param args: Raw arguments passed by workers. (Not used)
    :return: Nothing. (See the description for more info)
    """
    
    # Preparing the logger for the 1st time if needed.
    if worker.logger_thread is None:
        worker.logger_thread = get_logger(
            "yt-live-" + worker.channel.channel_config.internal_id,
            worker.channel.config.youtube.logging_level_thread
        )
    
    # Makes non-debug logs possible to debug from a bird's eye view.
    worker.logger_thread.info("Running 'YouTube Live' thread for '{}' !".format(worker.channel.channel_config.name))
    
    # Preparing the base filename with no extension
    file_base_name: str = "{}-live-{}".format(
        worker.channel.channel_config.internal_id,
        str(int(time.time()))
    )
    
    # Preparing the command
    command: str = "streamlink --hls-live-restart -o \"{}\" https://www.youtube.com/c/{}/live {}".format(
        os.path.normpath(os.path.join(worker.channel.get_livestream_output_path(), file_base_name + ".mp4")),
        worker.channel.channel_config.channel_id,
        worker.channel.channel_config.quality_live
    )
    worker.logger_thread.debug("Command: " + command)
    
    # Used to check when the metadata should be grabbed
    process_start_time: Union[float, None] = time.time()
    metadata_delay: float = worker.channel.config.youtube.delay_ms_metadata_download / 1000
    
    # Running the processes
    process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process_yt_dlp: Union[subprocess.Popen, None] = None
    has_sent_signal: bool = False
    
    while process.poll() is None:
        if metadata_delay != -1 and process_start_time is not None:
            if time.time() > process_start_time + metadata_delay:
                # Attempting to download the metadata
                worker.logger_thread.debug("Attempting to download metadata...")
                
                # TODO: Fix for the new folder structure !
                command_yt_dlp = "yt-dlp --write-thumbnail --write-description --write-info-json --skip-download " \
                                 "-o \"{}\" https://www.youtube.com/c/{}/live"
                command_yt_dlp = command_yt_dlp.format(
                    os.path.normpath(os.path.join(worker.channel.get_livestream_output_path(), file_base_name)),
                    worker.channel.channel_config.channel_id
                )
                worker.logger_thread.debug("Command: " + command_yt_dlp)
                
                process_yt_dlp = subprocess.Popen(command_yt_dlp, shell=True, stdout=subprocess.PIPE)
                
                # Disabling subsequent checks
                process_start_time = None
                metadata_delay = -1
        
        if (not has_sent_signal) and (worker.end_signal_to_process != -1):
            worker.logger_thread.info("Detected a shutdown signal ! ({})".format(worker.end_signal_to_process))
            process.send_signal(worker.end_signal_to_process)
            if process_yt_dlp is not None:
                if process_yt_dlp.poll() is None:
                    process_yt_dlp.send_signal(worker.end_signal_to_process)
            has_sent_signal = True
        
        # Prevents CPU hogging
        time.sleep(0.01)
    
    # Just in case...
    process.wait()
    
    # Should be fine, for now...
    if process_yt_dlp is not None:
        worker.logger_thread.debug("Waiting to yt-dlp to finish...")
        process_yt_dlp.wait()
    
    worker.last_return_code = process.returncode
    
    worker.logger_thread.debug("Closing thread ! => {}".format(worker.last_return_code))
