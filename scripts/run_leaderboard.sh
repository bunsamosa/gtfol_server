#!/bin/bash
cd /home/deploy/tweet_loader
. .venv/bin/activate
doppler run -- python3 load_leaderboard.py
