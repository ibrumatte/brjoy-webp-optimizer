from __future__ import annotations

import os
from pathlib import Path

from app.bridge.desktop_api import DesktopAPI


def run_desktop_app() -> None:
    try:
        import webview  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "pywebview is not installed. Install with: pip3 install pywebview"
        ) from exc

    os.environ.setdefault("GDK_BACKEND", "x11")

    api = DesktopAPI()
    project_root = Path(__file__).resolve().parents[2]
    index_html = project_root / "frontend" / "dist" / "index.html"

    if index_html.exists():
        window = webview.create_window(
            title="BrJoy Image Converter",
            url=index_html.as_uri(),
            js_api=api,
            min_size=(980, 700),
            width=1280,
            height=840,
            text_select=False,
            background_color="#F2F7F7",
        )
    else:
        fallback_html = """
        <html><body style='font-family:Segoe UI,Arial;padding:24px;background:#f2f7f7;color:#142033'>
        <h2>Frontend bundle not found</h2>
        <p>Build the frontend first:</p>
        <pre>cd frontend\nnpm install\nnpm run build</pre>
        </body></html>
        """
        window = webview.create_window(
            title="BrJoy Image Converter",
            html=fallback_html,
            js_api=api,
            min_size=(980, 700),
            width=980,
            height=700,
            background_color="#F2F7F7",
        )

    api.attach_window(window)
    window.events.closed += lambda: None
    webview.start(debug=False, http_server=False)
