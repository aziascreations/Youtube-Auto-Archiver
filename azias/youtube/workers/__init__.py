import os
import subprocess
import time
from typing import Union

import azias
import azias.config as config
from azias.youtube import Channel
from azias.worker import Worker


class YouTubeWorker(Worker):
    channel: Channel
    
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point)
        self.channel = channel


class __WorkerLive(YouTubeWorker):
    def __init__(self, name, entry_point, channel):
        super().__init__(name, entry_point, channel)


def __thread_yt_live(worker: YouTubeWorker, **args):
    # Preparing the logger if needed
    if worker.logger_thread is None:
        worker.logger_thread = azias.get_logger(
            "yt-live-" + worker.channel.internal_id,
            config.current_logger_level_thread)
    
    file_base_name: str = "{}{}-live-{}".format(
        config.config["youtube"]["general_prefix"],
        worker.channel.internal_id,
        str(int(time.time()))
    )
    
    command: str = "streamlink --hls-live-restart -o \"{}\" https://www.youtube.com/c/{}/live {}".format(
        os.path.normpath(os.path.join(worker.channel.get_output_path(), file_base_name + ".mp4")),
        worker.channel.channel_id,
        worker.channel.quality_live
    )
    worker.logger_thread.debug("Command: " + command)
    
    # Used to check when the metadata should be grabbed
    process_start_time: Union[float, None] = time.time()
    metadata_delay: float = config.get_youtube_metadata_delay() / 1000
    
    process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process_yt_dlp: Union[subprocess.Popen, None] = None
    while process.poll() is None:
        if metadata_delay != -1 and process_start_time is not None:
            if time.time() > process_start_time + metadata_delay:
                worker.logger_thread.debug("Attempting to download metadata...")
                
                command_yt_dlp = "yt-dlp --write-thumbnail --write-description --skip-download -o \"{}\" " \
                                 "https://www.youtube.com/c/{}/live".format(
                    os.path.normpath(os.path.join(worker.channel.get_output_path(), file_base_name)),
                    worker.channel.channel_id)
                worker.logger_thread.debug("Command: "+command_yt_dlp)

                process_yt_dlp = subprocess.Popen(command_yt_dlp, shell=True, stdout=subprocess.PIPE)
                
                # Disabling subsequent checks
                process_start_time = None
                metadata_delay = -1
        
        # Prevents CPU hogging
        time.sleep(0.001)
    
    # Just in case...
    process.wait()
    
    # Should be fine, for now...
    if process_yt_dlp is not None:
        worker.logger_thread.debug("Waiting to yt-dlp to finish...")
        process_yt_dlp.wait()
    
    worker.last_return_code = process.returncode
    
    # Debugging time sink
    # time.sleep((worker.channel.interval_ms_live / 1000) * 1.5)
    
    worker.logger_thread.debug("Closing thread ! => {}".format(worker.last_return_code))


def create_live_worker(channel: Channel) -> YouTubeWorker:
    return __WorkerLive("worker-yt-live-" + channel.internal_id, __thread_yt_live, channel)
