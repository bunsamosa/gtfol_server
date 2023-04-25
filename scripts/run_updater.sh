#!/bin/bash
cd /home/deploy/tweet_loader
. .venv/bin/activate
doppler run -- python3 daily_refresh.py
