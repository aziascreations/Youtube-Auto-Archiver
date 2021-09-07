import os
import subprocess
import time

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
            "yt-live-"+worker.channel.internal_id,
            config.current_logger_level_thread)

    command: str = "streamlink --hls-live-restart -o {}/{}.mp4 https://www.youtube.com/c/{}/live best".format(
        os.path.normpath(worker.channel.get_output_path()),
        worker.channel.internal_id+"-live-"+str(int(time.time())),
        worker.channel.channel_id
    )
    worker.logger_thread.debug("Command: "+command)
    
    process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    worker.last_return_code = process.returncode
    
    # Debugging time sink
    # time.sleep((worker.channel.interval_ms_live / 1000) * 1.5)
    
    worker.logger_thread.debug("Closing thread ! => {}".format(worker.last_return_code))


def create_live_worker(channel: Channel) -> YouTubeWorker:
    return __WorkerLive("worker-yt-live-"+channel.internal_id, __thread_yt_live, channel)
