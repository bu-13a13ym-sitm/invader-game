#!/bin/bash

VENV_DIR = "venv"
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

pip install --upgrade pip
pip install -r requirements.txt