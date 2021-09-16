import os
import signal
import subprocess
import time
from typing import Union

import yaa
import yaa.config as config
from yaa.youtube import Channel
from yaa.worker import Worker


class YouTubeWorker(Worker):
    """
    Extension of the Worker class that handles YouTube channels.
    """
    channel: Channel
    
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point)
        self.channel = channel
        self.logger_worker.setLevel(config.get_config_value(
            config.DEFAULT_LOGGER_LEVEL_WORKER,
            ["youtube", "logging_level_worker"]
        ))


class __WorkerLive(YouTubeWorker):
    """
    Private class that is used for livestream related tasks.
    It should only be used outside of this module if no other way of determining its goal is available.
    """
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point, channel)


class __WorkerUpload(YouTubeWorker):
    """
    Private class that is used for regular upload related tasks.
    It should only be used outside of this module if no other way of determining its goal is available.
    """
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point, channel)


def __thread_yt_upload_sig_handler(sig, frame):
    print("#"*50)


def __thread_yt_upload(worker: YouTubeWorker, **args):
    """
    Thread method for the upload worker that checks if a channel has uploads that match a filter.
    Once finished, the thread sets the worker's 'last_return_code' variable with the one returned by yt-dlp.
    
    :param worker: Worker from which this thread was spawned.
    :param args: Raw arguments passed by workers. (Not used)
    :return: Nothing. (See the description for more info)
    """
    # Preparing the logger if needed
    if worker.logger_thread is None:
        worker.logger_thread = yaa.get_logger(
            "yt-upload-" + worker.channel.internal_id,
            config.get_config_value(
                config.DEFAULT_LOGGER_LEVEL_THREAD,
                ["youtube", "logging_level_thread"]
            )
        )
    
    # Registering SIG handlers...
    signal.signal(signal.SIGINT, __thread_yt_upload_sig_handler)
    signal.signal(signal.SIGTERM, __thread_yt_upload_sig_handler)
    
    # Preparing the command
    command: str = "yt-dlp --no-warnings --newline --no-progress --dateafter now-{}days {}{}-f {} {}https://www.youtube.com/c/{}".format(
        ("1" if worker.channel.backlog_days_upload < 1 else str(worker.channel.backlog_days_upload)),
        ("" if not worker.channel.break_on_existing else "--break-on-existing "),
        ("" if not worker.channel.break_on_reject else "--break-on-reject "),
        worker.channel.quality_upload,
        worker.channel.yt_dlp_extra_args + ("" if worker.channel.yt_dlp_extra_args.endswith(" ") else " "),
        worker.channel.channel_id
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


def __thread_yt_live(worker: YouTubeWorker, **args):
    """
    Thread method for the live worker that checks if a channel is currently livestreaming.
    Once finished, the thread sets the worker's 'last_return_code' variable with the one returned by streamlink.
    
    :param worker: Worker from which this thread was spawned.
    :param args: Raw arguments passed by workers. (Not used)
    :return: Nothing. (See the description for more info)
    """
    # Preparing the logger if needed
    if worker.logger_thread is None:
        worker.logger_thread = yaa.get_logger(
            "yt-live-" + worker.channel.internal_id,
            config.get_config_value(
                config.DEFAULT_LOGGER_LEVEL_THREAD,
                ["youtube", "logging_level_thread"]
            )
        )
    
    # Preparing the base filename with no extension
    file_base_name: str = "{}{}-live-{}".format(
        config.config["youtube"]["general_prefix"],
        worker.channel.internal_id,
        str(int(time.time()))
    )
    
    # Preparing the command
    command: str = "streamlink --hls-live-restart -o \"{}\" https://www.youtube.com/c/{}/live {}".format(
        os.path.normpath(os.path.join(worker.channel.get_output_path(), file_base_name + ".mp4")),
        worker.channel.channel_id,
        worker.channel.quality_live
    )
    worker.logger_thread.debug("Command: " + command)
    
    # Used to check when the metadata should be grabbed
    process_start_time: Union[float, None] = time.time()
    metadata_delay: float = config.get_youtube_live_metadata_delay_ms() / 1000
    
    # Running the processes
    process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process_yt_dlp: Union[subprocess.Popen, None] = None
    has_sent_signal: bool = False
    
    while process.poll() is None:
        if metadata_delay != -1 and process_start_time is not None:
            if time.time() > process_start_time + metadata_delay:
                worker.logger_thread.debug("Attempting to download metadata...")
                
                command_yt_dlp = "yt-dlp --write-thumbnail --write-description --write-info-json --skip-download " \
                                 "-o \"{}\" https://www.youtube.com/c/{}/live".format(
                    os.path.normpath(os.path.join(worker.channel.get_output_path(), file_base_name)),
                    worker.channel.channel_id)
                worker.logger_thread.debug("Command: "+command_yt_dlp)

                process_yt_dlp = subprocess.Popen(command_yt_dlp, shell=True, stdout=subprocess.PIPE)
                
                # Disabling subsequent checks
                process_start_time = None
                metadata_delay = -1
        
        if (not has_sent_signal) and (worker.end_signal_to_process != -1):
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


def create_live_worker(channel: Channel) -> YouTubeWorker:
    """
    Creates a YouTubeWorker that handles and process livestreams from and for a given channel.
    :param channel: A Channel object for which the live worker should be created
    :return: A YouTubeWorker object for the corresponding channel
    """
    return __WorkerLive("worker-yt-live-" + channel.internal_id, __thread_yt_live, channel)


def create_upload_worker(channel: Channel) -> YouTubeWorker:
    """
    Creates a YouTubeWorker that handles and process uploads from and for a given channel.
    :param channel: A Channel object for which the upload worker should be created
    :return: A YouTubeWorker object for the corresponding channel
    """
    return __WorkerLive("worker-yt-upload-" + channel.internal_id, __thread_yt_upload, channel)
