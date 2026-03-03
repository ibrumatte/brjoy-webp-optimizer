#!/bin/bash
export GDK_BACKEND=x11
cd /home/brjoy2/.local/share/brjoy-image-converter
exec python3 conversor_gui.py
