import unittest
import os
import time
from rtsp_snap import RtspSource, RtspSnapshotGenerator

record_dir = os.path.join(os.getcwd(), "test_snapshots")
url = "rtsp://root:xxx@10.0.0.201/axis-media/media.amp"

class TestRtspSnapshotGenerator(unittest.TestCase):
    def setUp(self):
        # Create the test directory if it doesn't exist
        if not os.path.exists(record_dir):
            os.makedirs(record_dir)

    def tearDown(self):
        # Clean up the test directory after the test
        for file_name in os.listdir(record_dir):
            file_path = os.path.join(record_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(record_dir)

    def test_snapshot_generation(self):
        rtsp_source = RtspSource(file_name_prefix="cam1", url=url)
        generator = RtspSnapshotGenerator([rtsp_source], seconds_to_sleep=1, recording_dir=record_dir, console_logging=False)
        generator.start()
        time.sleep(5)
    
        jpg_files = [filename for filename in os.listdir(record_dir) if filename.endswith(".jpg")]
        self.assertTrue(jpg_files, "No JPG files were created")

        generator.stop()

if __name__ == '__main__':
    unittest.main()