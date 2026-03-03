import json
import tempfile
import unittest
from pathlib import Path

from app.services.report_service import ReportService


class TestReportService(unittest.TestCase):
    def test_list_reports_and_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = Path(tmp) / 'reports'
            session = reports_dir / '20260303-000001-site'
            session.mkdir(parents=True)
            (session / 'AI-CODE-UPDATE.txt').write_text('line 1\nline 2\n', encoding='utf-8')
            meta = {
                'id': session.name,
                'generated_at': '2026-03-03T10:00:00',
                'report_folder': str(session),
                'html_report': str(session / 'conversion-report.html'),
                'ai_report': str(session / 'AI-CODE-UPDATE.txt'),
                'csv_report': str(session / 'conversions.csv'),
                'success': 1,
                'errors': 0,
                'total': 1,
            }
            (session / 'report-meta.json').write_text(json.dumps(meta), encoding='utf-8')

            svc = ReportService(reports_dir=reports_dir)
            reports = svc.list_reports()
            self.assertEqual(len(reports), 1)
            self.assertEqual(reports[0]['generatedAt'], '2026-03-03T10:00:00')
            self.assertIn('htmlReport', reports[0])
            preview = svc.get_report_preview(session.name)
            self.assertIn('line 1', preview)


if __name__ == '__main__':
    unittest.main()
