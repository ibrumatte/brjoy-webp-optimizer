import tempfile
import unittest
from pathlib import Path

from app.bridge.desktop_api import DesktopAPI
from app.services.settings_service import SettingsService


class TestDesktopAPI(unittest.TestCase):
    def test_bootstrap_and_preferences_roundtrip(self):
        api = DesktopAPI()

        with tempfile.TemporaryDirectory() as tmp:
            settings_file = Path(tmp) / 'settings.json'
            api.settings_service = SettingsService(settings_file=settings_file)

            bootstrap = api.get_app_bootstrap()
            self.assertIn('presets', bootstrap)
            self.assertIn('locale', bootstrap)

            response = api.set_preferences({'locale': 'en-US', 'theme': 'dark'})
            self.assertTrue(response['ok'])
            prefs = api.get_preferences()
            self.assertEqual(prefs['locale'], 'en-US')
            self.assertEqual(prefs['theme'], 'dark')

    def test_cancel_unknown_job_returns_false(self):
        api = DesktopAPI()
        response = api.cancel_conversion('missing-job')
        self.assertFalse(response['canceled'])

    def test_invalid_conversion_payload_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.start_conversion({'files': [], 'config': {}})

    def test_get_missing_job_status_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.get_conversion_status('missing-job')

    def test_open_report_with_invalid_kind_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.open_report('report-id', 'pdf')

    def test_collect_paths_with_invalid_payload_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.collect_paths('not-a-list')  # type: ignore[arg-type]

    def test_set_preferences_with_invalid_payload_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.set_preferences('bad')  # type: ignore[arg-type]

    def test_scan_folder_with_empty_path_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.scan_folder('')

    def test_scan_folder_with_invalid_extension_filter_raises(self):
        api = DesktopAPI()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                api.scan_folder(tmp, ['png', '.exe'])

    def test_collect_paths_with_invalid_extension_filter_raises(self):
        api = DesktopAPI()
        with self.assertRaises(ValueError):
            api.collect_paths(['/tmp/non-existing-file.png'], None, ['webp', '.exe'])


if __name__ == '__main__':
    unittest.main()
