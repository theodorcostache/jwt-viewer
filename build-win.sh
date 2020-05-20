#!/bin/bash

rm -rf build/
rm -rf dist/

if [ ! -d env ]; then
    python -m virtualenv env
    source env/Scripts/activate
    pip install -r requirements.txt
    pip install pyinstaller
else
    source env/Scripts/activate
fi

pyinstaller --noconsole --onefile --name jwtviewer.exe main.py