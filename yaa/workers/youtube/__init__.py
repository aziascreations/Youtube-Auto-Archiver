# Imports
from yaa.data.youtube import YouTubeChannel
from yaa.workers.worker import Worker


# Classes
class YouTubeWorker(Worker):
    """
    Extension of the Worker class that handles YouTube channels.
    """
    channel: YouTubeChannel
    
    def __init__(self, name, entry_point, channel: YouTubeChannel):
        super().__init__(name, entry_point)
        self.channel = channel
        self.logger_worker.setLevel(self.channel.config.youtube.logging_level_worker)
