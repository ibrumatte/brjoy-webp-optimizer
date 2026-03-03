import json
import tempfile
import unittest
from pathlib import Path

from app.services.settings_service import SettingsService


class TestSettingsService(unittest.TestCase):
    def test_get_preferences_returns_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            svc = SettingsService(settings_file=Path(tmp) / 'settings.json')
            prefs = svc.get_preferences()
            self.assertEqual(prefs['locale'], 'pt-BR')
            self.assertEqual(prefs['theme'], 'system')

    def test_set_preferences_merges_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'settings.json'
            svc = SettingsService(settings_file=path)
            merged = svc.set_preferences({'locale': 'en-US', 'theme': 'dark'})
            self.assertEqual(merged['locale'], 'en-US')
            self.assertEqual(merged['theme'], 'dark')

            disk = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(disk['locale'], 'en-US')
            self.assertEqual(disk['theme'], 'dark')

    def test_set_preferences_accepts_ui_density(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'settings.json'
            svc = SettingsService(settings_file=path)
            merged = svc.set_preferences({'uiDensity': 'compact'})
            self.assertEqual(merged['uiDensity'], 'compact')

    def test_invalid_preference_values_fallback_to_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'settings.json'
            svc = SettingsService(settings_file=path)
            merged = svc.set_preferences({
                'locale': 'fr-FR',
                'theme': 'neon',
                'uiDensity': 'dense',
                'lastPreset': 123,
            })
            self.assertEqual(merged['locale'], 'pt-BR')
            self.assertEqual(merged['theme'], 'system')
            self.assertEqual(merged['uiDensity'], 'compact')
            self.assertEqual(merged['lastPreset'], '')


if __name__ == '__main__':
    unittest.main()
