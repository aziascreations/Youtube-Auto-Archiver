# Imports
import os
import signal
import subprocess
import time

from yaa.data.youtube import YouTubeChannel
from yaa.logger import get_logger
from yaa.workers.youtube import YouTubeWorker


# Classes
class __WorkerUpload(YouTubeWorker):
    """
    Private class that is used for regular upload related tasks.
    It should only be used outside this module if no other way of determining its goal is available.
    """
    
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point, channel)


# Methods
def create_upload_worker(channel: YouTubeChannel) -> YouTubeWorker:
    """
    Creates a YouTubeWorker that handles and process uploads from and for a given channel.
    :param channel: A YouTubeChannel object for which the upload worker should be created
    :return: A YouTubeWorker object for the corresponding channel
    """
    return __WorkerUpload("worker-yt-upload-" + channel.channel_config.internal_id, __thread_yt_upload, channel)


def __thread_yt_upload_sig_handler(sig, frame):
    print("#" * 50)


def __thread_yt_upload(worker: YouTubeWorker, **args):
    """
    Thread method for the upload worker that checks if a channel has uploads that match a filter.
    Once finished, the thread sets the worker's 'last_return_code' variable with the one returned by yt-dlp.

    :param worker: Worker from which this thread was spawned.
    :param args: Raw arguments passed by workers. (Not used)
    :return: Nothing. (See the description for more info)
    """
    # Preparing the logger for the 1st time if needed.
    if worker.logger_thread is None:
        worker.logger_thread = get_logger(
            "yt-upload-" + worker.channel.channel_config.internal_id,
            worker.channel.config.youtube.logging_level_thread
        )
    
    # Registering SIG handlers...
    signal.signal(signal.SIGINT, __thread_yt_upload_sig_handler)
    signal.signal(signal.SIGTERM, __thread_yt_upload_sig_handler)
    
    # Preparing the command
    command: str = "yt-dlp --no-warnings --newline --no-progress --dateafter now-{}days {}{}-f {} {}" \
                   "https://www.youtube.com/c/{}"
    command = command.format(
        ("1" if worker.channel.channel_config.backlog_days_upload < 1
         else str(worker.channel.channel_config.backlog_days_upload)),
        ("" if not worker.channel.channel_config.break_on_existing else "--break-on-existing "),
        ("" if not worker.channel.channel_config.break_on_reject else "--break-on-reject "),
        worker.channel.channel_config.quality_upload,
        worker.channel.channel_config.yt_dlp_extra_args +
        ("" if worker.channel.channel_config.yt_dlp_extra_args.endswith(" ") else " "),
        worker.channel.channel_config.channel_id
    )
    worker.logger_thread.debug("Command: " + command)
    
    # Running the process
    process: subprocess.Popen = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        cwd=os.path.normpath(worker.channel.get_output_path())
    )
    
    # Waiting for it to finish...
    has_sent_signal: bool = False
    while process.poll() is None:
        if (not has_sent_signal) and (worker.end_signal_to_process != -1):
            worker.logger_thread.debug("Detected a shutdown signal ! ({})".format(worker.end_signal_to_process))
            process.send_signal(worker.end_signal_to_process)
            has_sent_signal = True
        # Prevents CPU hogging
        time.sleep(0.2)
    
    # Just in case...
    process.wait()
    
    worker.last_return_code = process.returncode
    
    lines = process.stdout.readlines()
    process.stdout.flush()
    for line in lines:
        worker.logger_thread.debug(line)
    
    worker.logger_thread.debug("Closing thread ! => {}".format(worker.last_return_code))
