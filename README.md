
## Usage

#### RtspSnapshotGenerator Arguments

- `rtsp_sources` (list[RtspSource]): A list of RTSP sources to capture snapshots from.

- `seconds_to_sleep` (int, optional): Seconds to sleep between snapshots. Default is 60 seconds.

- `recording_dir` (str, optional): Directory to save captured snapshots. Default is "./snapshots".

- `console_logging` (bool, optional): Whether to enable console logging. Default is True.

- `file_logging` (bool, optional): Whether to enable file logging. Default is False.

### RtspSource

#### Dataclass Fields

- `file_name_prefix` (str): Represents a file name prefix for the snapshots captured from this RTSP source.

- `url` (str): The RTSP URL of the camera stream.


### Creating an RTSP Snapshot Generator

To create an RTSP Snapshot Generator, you can use the `RtspSnapshotGenerator` class provided by the `rtsp_snap` module. Here's how to set up the generator:

```python
from rtsp_snap import RtspSource, RtspSnapshotGenerator

rtsp_sources = [
    RtspSource(file_name_prefix="cam_1", url="rtsp://username:password@camera1_ip/rtsp_stream"),
    # Add more RTSP sources as needed
]

generator = RtspSnapshotGenerator(rtsp_sources, seconds_to_sleep=10, recording_dir="./snapshots", console_logging=True)
```

### Start/Stop an RTSP Snapshot Generator

```python
generator.start()  # Start capturing snapshots
# You can run the generator for a specified duration or manually stop it with Ctrl+C
generator.stop()   # Stop capturing snapshots and close the RTSP sources
```

### Demo Implementation

Here's a demo implementation that captures snapshots from multiple RTSP sources for 50 seconds and gracefully stops when Ctrl+C is pressed:

```python
from rtsp_snap import RtspSource, RtspSnapshotGenerator
import time
import signal
import sys

def signal_handler(sig, frame):
    print("\nStopping snapshot generation...")
    generator.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Set up a signal handler for Ctrl+C (KeyboardInterrupt)
    signal.signal(signal.SIGINT, signal_handler)

    rtsp_sources = [
        RtspSource(file_name_prefix="cam_1", url="rtsp://username:password@camera1_ip/rtsp_stream"),
        RtspSource(file_name_prefix="cam_2", url="rtsp://username:password@camera2_ip/rtsp_stream"),
        # Add more RTSP sources as needed
    ]

    generator = RtspSnapshotGenerator(rtsp_sources, seconds_to_sleep=10, recording_dir="./snapshots", console_logging=True)
    generator.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        pass  # Allow Ctrl+C to gracefully stop the script

    generator.stop()
```