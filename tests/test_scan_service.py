import tempfile
import unittest
from pathlib import Path

from app.services.scan_service import ScanService


class TestScanService(unittest.TestCase):
    def test_scan_folder_applies_extension_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.png').write_bytes(b'a')
            (root / 'b.jpg').write_bytes(b'b')
            (root / 'c.webp').write_bytes(b'c')

            svc = ScanService()
            files = svc.scan_folder(str(root), extensions=['.png', 'webp'])
            names = sorted(Path(item['path']).name for item in files)
            self.assertEqual(names, ['a.png', 'c.webp'])

    def test_collect_paths_applies_extension_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'assets'
            folder.mkdir(parents=True, exist_ok=True)
            (folder / 'hero.png').write_bytes(b'a')
            (folder / 'thumb.jpg').write_bytes(b'b')

            svc = ScanService()
            files = svc.collect_paths([str(folder)], extensions=['png'])
            names = sorted(Path(item['path']).name for item in files)
            self.assertEqual(names, ['hero.png'])


if __name__ == '__main__':
    unittest.main()
