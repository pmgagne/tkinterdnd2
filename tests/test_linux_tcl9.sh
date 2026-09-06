#!/usr/bin/env bash
# Test Linux x64 + Tcl 9 binary loading using a Fedora container.
# Run from the tkinterdndeliav directory.
set -e
docker run --rm \
  -v "$(pwd):/workspace" \
  -w /workspace \
  fedora:latest \
  bash -c "
    set -e
    dnf install -y python3 python3-tkinter python3-pip xorg-x11-server-Xvfb libXcursor 2>&1 | tail -3
    pip3 install -e . --break-system-packages --quiet
    Xvfb :99 -screen 0 1024x768x24 &
    sleep 1
    DISPLAY=:99 python3 -m unittest discover -s tests -v
  "
