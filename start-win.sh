#!/bin/bash

if [ ! -d env ]; then
    python -m virtualenv env
    source env/Scripts/activate
    pip install -r requirements.txt
else
    source env/Scripts/activate
fi

which python
python main.py