#!/usr/bin/env python3
"""
Core logic tests for brjoy-converter without requiring GUI display.
"""
import tempfile
import threading
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path


def load_converter_module():
    script_path = Path(__file__).with_name("brjoy-converter")
    loader = SourceFileLoader("brjoy_converter", str(script_path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


module = load_converter_module()
ConversorHEIC = module.ConversorHEIC


class DummyVar:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class TestCoreLogic(unittest.TestCase):
    def make_obj(self):
        obj = ConversorHEIC.__new__(ConversorHEIC)
        obj.arquivos = []
        obj.pasta_origem = None
        obj.pasta_saida = DummyVar("")
        obj.reports_dir = Path(tempfile.gettempdir()) / "brjoy-reports-tests"
        obj.reports_dir.mkdir(parents=True, exist_ok=True)
        obj.report_items = {}
        obj.atualizar_lista = lambda: None
        return obj

    def test_safe_csv_cell_prefixes_formula(self):
        obj = self.make_obj()
        self.assertEqual(obj._safe_csv_cell("=SUM(A1:A2)"), "'=SUM(A1:A2)")
        self.assertEqual(obj._safe_csv_cell("+cmd"), "'+cmd")
        self.assertEqual(obj._safe_csv_cell("normal"), "normal")

    def test_validate_config_rejects_invalid_batch(self):
        obj = self.make_obj()
        config = {
            "batch_sizes_enabled": True,
            "batch_sizes": [],
            "redimensionar": False,
            "largura_max": None,
            "altura_max": None,
        }
        self.assertIsNotNone(obj._validate_conversion_config(config))

    def test_build_convert_cmd_resizes_when_width_forced_by_batch(self):
        obj = self.make_obj()
        config = {
            "sharpen": False,
            "brightness": 100,
            "redimensionar": False,
            "largura_max": None,
            "altura_max": None,
            "recorte_1x1": False,
            "qualidade": 85,
        }
        cmd = obj._build_convert_cmd("/tmp/x.jpg", config, width=800)
        self.assertIn("-resize", cmd)
        self.assertIn("800x>", cmd)

    def test_resolve_output_folder_uses_original_parent_when_preserving_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source_root = tmp_path / "source"
            nested = source_root / "assets" / "home"
            nested.mkdir(parents=True)
            image = nested / "hero.jpg"
            image.write_bytes(b"data")

            output_root = tmp_path / "output"
            output_root.mkdir()

            obj = self.make_obj()
            info = {"path": str(image), "rel_path": "assets/home/hero.jpg"}
            config = {"substituir_no_lugar": False, "manter_estrutura": True}

            target = obj._resolve_output_folder(info, output_root, config)
            self.assertEqual(target, image.parent)

    def test_reserve_output_path_avoids_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            obj = self.make_obj()
            base = tmp_path / "image.webp"
            base.write_bytes(b"existing")

            reserved = set()
            lock = threading.Lock()

            p1 = obj._reserve_output_path(base, reserved, lock)
            p1.write_bytes(b"x")
            p2 = obj._reserve_output_path(base, reserved, lock)

            self.assertEqual(p1.name, "image_1.webp")
            self.assertEqual(p2.name, "image_2.webp")

    def test_add_files_recursive_and_ignores_known_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            root = tmp_path / "project"
            (root / "imgs" / "nested").mkdir(parents=True)
            (root / "node_modules").mkdir()

            img1 = root / "imgs" / "a.jpg"
            img2 = root / "imgs" / "nested" / "b.png"
            ignored = root / "node_modules" / "x.jpg"
            img1.write_bytes(b"a")
            img2.write_bytes(b"b")
            ignored.write_bytes(b"c")

            obj = self.make_obj()
            obj.pasta_origem = root
            obj._add_files([str(root)])

            paths = {Path(item["path"]).name for item in obj.arquivos}
            self.assertIn("a.jpg", paths)
            self.assertIn("b.png", paths)
            self.assertNotIn("x.jpg", paths)

    def test_get_session_folder_uses_input_parent_for_replace_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            img = tmp_path / "photo.jpg"
            img.write_bytes(b"x")

            obj = self.make_obj()
            config = {"substituir_no_lugar": True}
            out = obj._get_session_folder([{"path": str(img)}], config)

            self.assertEqual(out, img.parent)

    def test_get_session_folder_uses_input_parent_for_preserve_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            img = tmp_path / "photo.jpg"
            img.write_bytes(b"x")

            obj = self.make_obj()
            config = {"substituir_no_lugar": False, "manter_estrutura": True}
            out = obj._get_session_folder([{"path": str(img)}], config)

            self.assertEqual(out, img.parent)

    def test_get_session_folder_uses_custom_output_when_not_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            img = tmp_path / "photo.jpg"
            img.write_bytes(b"x")

            custom = tmp_path / "custom-out"
            obj = self.make_obj()
            obj.pasta_saida = DummyVar(str(custom))
            config = {"substituir_no_lugar": False, "manter_estrutura": False}
            out = obj._get_session_folder([{"path": str(img)}], config)

            self.assertEqual(out, custom)
            self.assertTrue(out.exists())

    def test_create_report_folder_inside_global_reports_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            obj = self.make_obj()
            obj.reports_dir = tmp_path / "reports"
            output_folder = tmp_path / "output-folder"
            output_folder.mkdir()

            folder = obj._create_report_folder(output_folder)

            self.assertTrue(folder.exists())
            self.assertEqual(folder.parent, obj.reports_dir)

    def test_generate_report_saves_files_outside_output_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            obj = self.make_obj()
            obj.reports_dir = tmp_path / "reports"
            obj.reports_dir.mkdir(parents=True, exist_ok=True)
            output_folder = tmp_path / "project-output"
            output_folder.mkdir()

            details = [{
                "file": "assets/hero.png",
                "before": 2000,
                "after": 1000,
                "saved": 1000,
                "percent": 50.0,
            }]

            metadata = obj._generate_report(
                output_folder=output_folder,
                details=details,
                duration=1.5,
                success=1,
                errors=0,
                total=1,
                formato="webp",
                source_folders=[str(output_folder)],
            )

            self.assertIsNotNone(metadata)
            report_folder = Path(metadata["report_folder"])
            self.assertEqual(report_folder.parent, obj.reports_dir)
            self.assertTrue((report_folder / "conversion-report.html").exists())
            self.assertTrue((report_folder / "AI-CODE-UPDATE.txt").exists())
            self.assertTrue((report_folder / "conversions.csv").exists())
            self.assertTrue((report_folder / "report-meta.json").exists())
            self.assertFalse((output_folder / "conversion-report.html").exists())
            self.assertEqual(metadata["source_folders"], [str(output_folder)])

    def test_generate_ai_report_preserves_directory_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            obj = self.make_obj()
            report_folder = tmp_path / "reports" / "session"
            report_folder.mkdir(parents=True, exist_ok=True)

            details = [{
                "file": "assets/teste/daisi.png",
                "before": 2000,
                "after": 1000,
                "saved": 1000,
                "percent": 50.0,
            }]
            paths = obj._generate_ai_report(report_folder, details, "webp")

            self.assertIsNotNone(paths)
            ai_content = (report_folder / "AI-CODE-UPDATE.txt").read_text(encoding="utf-8")
            self.assertIn("assets/teste/daisi.png → assets/teste/daisi.webp", ai_content)
            self.assertIn("images/assets/teste/daisi.webp", ai_content)

    def test_generate_report_tracks_multiple_source_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            obj = self.make_obj()
            obj.reports_dir = tmp_path / "reports"
            obj.reports_dir.mkdir(parents=True, exist_ok=True)
            output_folder = tmp_path / "project-output"
            output_folder.mkdir()

            details = [
                {
                    "file": "assets/a.png",
                    "source_path": str(tmp_path / "site-a" / "assets" / "a.png"),
                    "output_paths": [str(tmp_path / "site-a" / "assets" / "a.webp")],
                    "before": 2000,
                    "after": 1000,
                    "saved": 1000,
                    "percent": 50.0,
                },
                {
                    "file": "assets/b.png",
                    "source_path": str(tmp_path / "site-b" / "assets" / "b.png"),
                    "output_paths": [str(tmp_path / "site-b" / "assets" / "b.webp")],
                    "before": 2000,
                    "after": 1000,
                    "saved": 1000,
                    "percent": 50.0,
                },
            ]

            source_folders = [str(tmp_path / "site-a" / "assets"), str(tmp_path / "site-b" / "assets")]
            metadata = obj._generate_report(
                output_folder=output_folder,
                details=details,
                duration=2.5,
                success=2,
                errors=0,
                total=2,
                formato="webp",
                source_folders=source_folders,
            )

            self.assertEqual(sorted(metadata["source_folders"]), sorted(source_folders))
            report_html = Path(metadata["html_report"]).read_text(encoding="utf-8")
            self.assertIn("Pasta(s) de origem (2)", report_html)

    def test_validate_config_rejects_height_without_width(self):
        obj = self.make_obj()
        config = {
            "batch_sizes_enabled": False,
            "batch_sizes": [],
            "redimensionar": False,
            "largura_max": None,
            "altura_max": 600,
        }
        self.assertIsNotNone(obj._validate_conversion_config(config))


if __name__ == "__main__":
    unittest.main()
