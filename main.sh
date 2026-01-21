#!/usr/bin/env bash

python3 main.py
cd public && python3 -m http.server 8888
