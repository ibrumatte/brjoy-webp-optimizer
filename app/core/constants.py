from __future__ import annotations

import multiprocessing

APP_NAME = "BrJoy Image Converter"
APP_ID = "brjoy-image-converter"
APP_DATA_DIRNAME = ".local/share/brjoy-image-converter"

IGNORED_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    ".cache",
    "__pycache__",
    ".next",
    ".nuxt",
    ".vite",
}

SUPPORTED_EXTENSIONS = {
    ".heic",
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
    ".gif",
    ".webp",
    ".avif",
}

MAX_DROP_SCAN_FILES = 2000
MAX_SCAN_DEPTH = 10
MAX_SCAN_FILES = 10000
MAX_WORKERS = min(4, multiprocessing.cpu_count())

PRESETS = {
    "Hero Image": {"resize": True, "width": 1920, "height": 1080, "crop": True, "quality": 85},
    "Blog Post": {"resize": True, "width": 1200, "height": 630, "crop": True, "quality": 85},
    "Thumbnail": {"resize": True, "width": 400, "height": 300, "crop": True, "quality": 80},
    "Mobile Optimized": {"resize": True, "width": 800, "height": None, "crop": False, "quality": 80},
    "Avatar/Icon": {"resize": True, "width": 256, "height": 256, "crop": True, "quality": 90},
    "Original Quality": {"resize": False, "width": None, "height": None, "crop": False, "quality": 95},
}

DEFAULT_PREFERENCES = {
    "locale": "pt-BR",
    "theme": "system",
    "lastPreset": "",
    "uiDensity": "compact",
}
