#!/bin/bash
set -ex
pytest
python3 trading_platform/manage.py migrate
python3 trading_platform/manage.py runserver 0.0.0.0:8000