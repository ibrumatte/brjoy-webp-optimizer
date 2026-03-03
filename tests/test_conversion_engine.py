import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import time

from app.core.conversion_engine import ConversionEngine
from app.services.history_service import HistoryService


class TestConversionEngine(unittest.TestCase):
    def test_build_converted_report_path_preserves_directories(self):
        engine = ConversionEngine(history_service=HistoryService())
        before, after = engine._build_converted_report_path('assets/teste/daisi.png', 'webp')
        self.assertEqual(before, 'assets/teste/daisi.png')
        self.assertEqual(after, 'assets/teste/daisi.webp')

    def test_generate_reports_tracks_multiple_source_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True)

            details = [
                {
                    'file': 'assets/a.png',
                    'source_path': str(tmp_path / 'a' / 'assets' / 'a.png'),
                    'output_paths': [str(tmp_path / 'a' / 'assets' / 'a.webp')],
                    'before': 2000,
                    'after': 1000,
                    'saved': 1000,
                    'percent': 50.0,
                },
                {
                    'file': 'assets/b.png',
                    'source_path': str(tmp_path / 'b' / 'assets' / 'b.png'),
                    'output_paths': [str(tmp_path / 'b' / 'assets' / 'b.webp')],
                    'before': 2000,
                    'after': 900,
                    'saved': 1100,
                    'percent': 55.0,
                },
            ]

            meta = engine._generate_reports(
                output_folder=str(tmp_path / 'output'),
                details=details,
                duration=3.2,
                success=2,
                errors=0,
                total=2,
                formato='webp',
                source_folders=[str(tmp_path / 'a' / 'assets'), str(tmp_path / 'b' / 'assets')],
            )

            self.assertEqual(len(meta['source_folders']), 2)
            self.assertTrue(Path(meta['html_report']).exists())
            self.assertTrue(Path(meta['ai_report']).exists())
            self.assertTrue(Path(meta['csv_report']).exists())

    def test_derive_source_root_from_rel_path(self):
        engine = ConversionEngine(history_service=HistoryService())
        root = engine._derive_source_root('/tmp/project/assets/teste/daisi.png', 'assets/teste/daisi.png')
        self.assertEqual(root, '/tmp/project')

    def test_cancel_marks_pending_as_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True, exist_ok=True)

            files = []
            for idx in range(8):
                source = tmp_path / f'image_{idx}.png'
                source.write_bytes(b'a' * 1200)
                files.append({
                    'id': str(idx),
                    'path': str(source),
                    'relPath': source.name,
                    'size': source.stat().st_size,
                })

            def fake_convert(cmd, check, capture_output, text):
                output = Path(cmd[-1])
                output.parent.mkdir(parents=True, exist_ok=True)
                time.sleep(0.12)
                output.write_bytes(b'b' * 600)
                class Result:
                    stderr = ''
                return Result()

            payload = {
                'files': files,
                'config': {
                    'formato': 'webp',
                    'manter_estrutura': True,
                    'substituir_no_lugar': False,
                    'qualidade': 85,
                    'brightness': 100,
                    'batch_sizes_enabled': False,
                    'redimensionar': False,
                },
            }

            with patch('app.core.conversion_engine.subprocess.run', side_effect=fake_convert):
                job_id = engine.start_conversion(payload)
                time.sleep(0.03)
                self.assertTrue(engine.cancel(job_id))

                deadline = time.time() + 5
                phase = ''
                while time.time() < deadline:
                    status = engine.get_status(job_id)
                    phase = status['phase']
                    if phase in {'canceled', 'done', 'error'}:
                        break
                    time.sleep(0.05)

            final_status = engine.get_status(job_id)
            self.assertEqual(final_status['phase'], 'canceled')
            self.assertGreaterEqual(final_status['skipped'], 1)
            self.assertEqual(final_status['success'] + final_status['errors'] + final_status['skipped'], final_status['total'])

    def test_output_collision_creates_suffixed_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True, exist_ok=True)

            source = tmp_path / 'hero.png'
            source.write_bytes(b'a' * 2000)
            existing_output = tmp_path / 'hero.webp'
            existing_output.write_bytes(b'old')

            def fake_convert(cmd, check, capture_output, text):
                output = Path(cmd[-1])
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(b'new' * 300)
                class Result:
                    stderr = ''
                return Result()

            payload = {
                'files': [{
                    'id': '1',
                    'path': str(source),
                    'relPath': source.name,
                    'size': source.stat().st_size,
                }],
                'config': {
                    'formato': 'webp',
                    'manter_estrutura': True,
                    'substituir_no_lugar': False,
                    'qualidade': 85,
                    'brightness': 100,
                    'batch_sizes_enabled': False,
                    'redimensionar': False,
                },
            }

            with patch('app.core.conversion_engine.subprocess.run', side_effect=fake_convert):
                job_id = engine.start_conversion(payload)
                deadline = time.time() + 5
                while time.time() < deadline:
                    status = engine.get_status(job_id)
                    if status['phase'] in {'done', 'error', 'canceled'}:
                        break
                    time.sleep(0.03)

            self.assertTrue((tmp_path / 'hero_1.webp').exists())
            self.assertTrue((tmp_path / 'hero.webp').exists())

    def test_start_conversion_tracks_multiple_source_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True, exist_ok=True)

            img_a = tmp_path / 'site-a' / 'assets' / 'a.png'
            img_b = tmp_path / 'site-b' / 'assets' / 'b.png'
            img_a.parent.mkdir(parents=True, exist_ok=True)
            img_b.parent.mkdir(parents=True, exist_ok=True)
            img_a.write_bytes(b'a' * 1200)
            img_b.write_bytes(b'b' * 1000)

            files = [
                {'id': 'a', 'path': str(img_a), 'relPath': 'assets/a.png', 'size': img_a.stat().st_size},
                {'id': 'b', 'path': str(img_b), 'relPath': 'assets/b.png', 'size': img_b.stat().st_size},
            ]

            def fake_convert(cmd, check, capture_output, text):
                output = Path(cmd[-1])
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(b'c' * 500)
                class Result:
                    stderr = ''
                return Result()

            payload = {
                'files': files,
                'config': {
                    'formato': 'webp',
                    'manter_estrutura': True,
                    'substituir_no_lugar': False,
                    'qualidade': 85,
                    'brightness': 100,
                    'batch_sizes_enabled': False,
                    'redimensionar': False,
                },
            }

            with patch('app.core.conversion_engine.subprocess.run', side_effect=fake_convert):
                job_id = engine.start_conversion(payload)
                deadline = time.time() + 5
                while time.time() < deadline:
                    status = engine.get_status(job_id)
                    if status['phase'] in {'done', 'error', 'canceled'}:
                        break
                    time.sleep(0.03)

            final_status = engine.get_status(job_id)
            self.assertEqual(final_status['phase'], 'done')
            self.assertIn(str(tmp_path / 'site-a'), final_status['sourceFolders'])
            self.assertIn(str(tmp_path / 'site-b'), final_status['sourceFolders'])

    def test_start_conversion_rejects_invalid_file_item(self):
        engine = ConversionEngine(history_service=HistoryService())
        payload = {
            'files': [{'id': 'x', 'path': '', 'relPath': '', 'size': 0}],
            'config': {'formato': 'webp', 'brightness': 100, 'qualidade': 85},
        }
        with self.assertRaises(ValueError):
            engine.start_conversion(payload)

    def test_start_conversion_rejects_files_not_list(self):
        engine = ConversionEngine(history_service=HistoryService())
        payload = {
            'files': 'invalid',
            'config': {'formato': 'webp', 'brightness': 100, 'qualidade': 85},
        }
        with self.assertRaises(ValueError):
            engine.start_conversion(payload)

    def test_start_conversion_rejects_config_not_object(self):
        engine = ConversionEngine(history_service=HistoryService())
        payload = {
            'files': [{'id': '1', 'path': '/tmp/a.png', 'relPath': 'a.png', 'size': 10}],
            'config': 'invalid',
        }
        with self.assertRaises(ValueError):
            engine.start_conversion(payload)

    def test_invalid_quality_string_falls_back_to_default(self):
        engine = ConversionEngine(history_service=HistoryService())
        normalized = engine._normalize_config({'formato': 'webp', 'qualidade': 'abc', 'brightness': 100})
        self.assertEqual(normalized['qualidade'], 85)

    def test_conflict_policy_skip_marks_item_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True, exist_ok=True)

            source = tmp_path / 'hero.png'
            source.write_bytes(b'a' * 2000)
            (tmp_path / 'hero.webp').write_bytes(b'existing')

            payload = {
                'files': [{
                    'id': '1',
                    'path': str(source),
                    'relPath': source.name,
                    'size': source.stat().st_size,
                }],
                'config': {
                    'formato': 'webp',
                    'manter_estrutura': True,
                    'substituir_no_lugar': False,
                    'conflict_policy': 'skip',
                    'qualidade': 85,
                    'brightness': 100,
                },
            }

            with patch('app.core.conversion_engine.subprocess.run') as mocked_run:
                job_id = engine.start_conversion(payload)
                deadline = time.time() + 5
                while time.time() < deadline:
                    status = engine.get_status(job_id)
                    if status['phase'] in {'done', 'error', 'canceled'}:
                        break
                    time.sleep(0.03)

            final_status = engine.get_status(job_id)
            self.assertEqual(final_status['phase'], 'done')
            self.assertEqual(final_status['success'], 0)
            self.assertEqual(final_status['skipped'], 1)
            mocked_run.assert_not_called()

    def test_conflict_policy_overwrite_with_bak_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True, exist_ok=True)

            source = tmp_path / 'hero.png'
            source.write_bytes(b'a' * 2000)
            output = tmp_path / 'hero.webp'
            output.write_bytes(b'old-data')

            def fake_convert(cmd, check, capture_output, text):
                out_path = Path(cmd[-1])
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(b'new-data')
                class Result:
                    stderr = ''
                return Result()

            payload = {
                'files': [{
                    'id': '1',
                    'path': str(source),
                    'relPath': source.name,
                    'size': source.stat().st_size,
                }],
                'config': {
                    'formato': 'webp',
                    'manter_estrutura': False,
                    'substituir_no_lugar': True,
                    'conflict_policy': 'overwrite',
                    'backup_enabled': True,
                    'backup_strategy': 'bak',
                    'qualidade': 85,
                    'brightness': 100,
                },
            }

            with patch('app.core.conversion_engine.subprocess.run', side_effect=fake_convert):
                job_id = engine.start_conversion(payload)
                deadline = time.time() + 5
                while time.time() < deadline:
                    status = engine.get_status(job_id)
                    if status['phase'] in {'done', 'error', 'canceled'}:
                        break
                    time.sleep(0.03)

            self.assertEqual((tmp_path / 'hero.webp').read_bytes(), b'new-data')
            self.assertEqual((tmp_path / 'hero.webp.bak').read_bytes(), b'old-data')

    def test_conflict_policy_overwrite_with_backup_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history = HistoryService(history_file=tmp_path / 'history.txt')
            engine = ConversionEngine(history_service=history)
            engine.reports_dir = tmp_path / 'reports'
            engine.reports_dir.mkdir(parents=True, exist_ok=True)

            source = tmp_path / 'hero.png'
            source.write_bytes(b'a' * 2000)
            output = tmp_path / 'hero.webp'
            output.write_bytes(b'old-data')

            def fake_convert(cmd, check, capture_output, text):
                out_path = Path(cmd[-1])
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(b'new-data')
                class Result:
                    stderr = ''
                return Result()

            payload = {
                'files': [{
                    'id': '1',
                    'path': str(source),
                    'relPath': source.name,
                    'size': source.stat().st_size,
                }],
                'config': {
                    'formato': 'webp',
                    'manter_estrutura': False,
                    'substituir_no_lugar': True,
                    'conflict_policy': 'overwrite',
                    'backup_enabled': True,
                    'backup_strategy': 'folder',
                    'qualidade': 85,
                    'brightness': 100,
                },
            }

            with patch('app.core.conversion_engine.subprocess.run', side_effect=fake_convert):
                job_id = engine.start_conversion(payload)
                deadline = time.time() + 5
                while time.time() < deadline:
                    status = engine.get_status(job_id)
                    if status['phase'] in {'done', 'error', 'canceled'}:
                        break
                    time.sleep(0.03)

            self.assertEqual((tmp_path / 'hero.webp').read_bytes(), b'new-data')
            self.assertEqual((tmp_path / '_backup' / 'hero.webp').read_bytes(), b'old-data')


if __name__ == '__main__':
    unittest.main()
