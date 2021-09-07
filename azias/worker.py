import logging
import threading
from typing import Callable, Union

import azias
from azias import config


class Worker:
    name: str
    entry_point: Callable
    thread: Union[threading.Thread, None]
    lock: threading.Lock
    logger_worker: logging.Logger
    logger_thread: Union[logging.Logger, None]
    last_return_code: int
    
    def __init__(self, name, entry_point):
        self.name = name
        self.entry_point = entry_point
        self.thread = None
        self.lock = threading.Lock()
        self.logger_worker = azias.get_logger(name, config.current_logger_level_worker)
        self.logger_thread = None
        self.last_return_code = 0
    
    def run(self, **args) -> bool:
        self.logger_worker.debug("Checking to prepare the Thread launch...")
        
        if self.thread is not None:
            if self.is_running():
                self.logger_worker.warning("A thread is already running on this worker !")
                return False
            else:
                self.logger_worker.debug("A thread has finished running, cleanup needed !")
                self.thread._target = None
                self.thread = None
        
        if not callable(self.entry_point):
            self.logger_worker.error("Unable to call the entrypoint method ! (Not callable)")
            return False
        
        self.logger_worker.debug("Starting thread...")
        self.thread = threading.Thread(target=self.entry_point, args=(self, *args))
        self.thread.start()
        return True
    
    def is_running(self) -> bool:
        if self.thread is not None:
            return self.thread.is_alive()
        
        return False
