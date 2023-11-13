import av
import time
import os
import logging
from dataclasses import dataclass
from threading import Event
from concurrent.futures import ThreadPoolExecutor

logging.getLogger('libav').setLevel(logging.ERROR)

@dataclass
class RtspSource:
    """
    Represents an RTSP source with a file name prefix and URL.
    """
    file_name_prefix: str
    url: str

class RtspSnapshotGenerator:
    """
    A class for generating snapshots from RTSP sources and saving them to disk.
    """
    def __init__(self, rtsp_sources: list[RtspSource], seconds_to_sleep: int = 60, recording_dir: str = "./snapshots", console_logging: bool = True, file_logging: bool = False):
        """
        Initializes the RtspSnapshotGenerator.

        Args:
            rtsp_sources (list[RtspSource]): List of RTSP sources to capture snapshots from.
            seconds_to_sleep (int, optional): Seconds to sleep between snapshots. Default is 60 seconds.
            recording_dir (str, optional): Directory to save captured snapshots. Default is "./snapshots".
            console_logging (bool, optional): Whether to enable console logging. Default is True.
            file_logging (bool, optional): Whether to enable file logging. Default is False.
        """
        self.rtsp_sources = rtsp_sources
        self.seconds_to_sleep = seconds_to_sleep
        self.recording_dir = recording_dir
        self.stop_event = Event()
        self.current_source = None
        self.console_logging = console_logging
        self.file_logging = file_logging
        self.log_file = "rtsp_snap.log"
        self.transport = "tcp"

        if self.console_logging or self.file_logging:
            log_format = '%(asctime)s [RTSP SNAP] [%(levelname)s]: %(message)s'

            if self.console_logging:
                logging.basicConfig(level=logging.INFO, format=log_format)

            if self.file_logging:
                logging.basicConfig(filename=self.log_file, level=logging.INFO, format=log_format)

        if not os.path.exists(self.recording_dir):
            self.log(f"Create Recording Directory: {self.recording_dir}")
            os.makedirs(self.recording_dir)

    def log(self, msg: str = "", level: str = "info"):
        """
        Logs a message with the specified logging level.

        Args:
            msg (str, optional): The message to log.
            level (str, optional): The logging level (e.g., "info", "error"). Default is "info".
        """
        logger = getattr(logging, level)
        if self.console_logging or self.file_logging:
            logger(msg)

    def _decode_on_frame_and_save_to_disk(self, rs: RtspSource):
        """
        Connects to an RTSP source, decodes frames, and saves them to disk.

        Args:
            rs (RtspSource): The RTSP source to capture frames from.
        """
        try:
            self.log(f'Connect: {rs.url}')
            container = av.open(rs.url, 'r', options = {'rtsp_transport': self.transport})
            for packet in container.demux():
                for frame in packet.decode():
                    ts = time.strftime("%Y%m%d_%H%M%S")
                    self.log(f'Save Frame for {rs.url} frame-{ts}.jpg')
                    frame.to_image().save(os.path.join(self.recording_dir, f'{rs.file_name_prefix}_frame_{ts}.jpg'))
                    container.close()
                    self.log(f'Disconnect: {rs.url}')
                    return
        except Exception as error:
            self.log(error, "error")

    def start(self):
        """
        Starts the snapshot generation process in a separate thread.
        """
        self.thread_pool = ThreadPoolExecutor(max_workers=len(self.rtsp_sources))
        for rs in self.rtsp_sources:
            self.thread_pool.submit(self._decode_on_frame_and_save_to_disk, rs)

    def stop(self):
        """
        Stops the snapshot generation process and closes the current RTSP source.
        """
        self.thread_pool.shutdown()