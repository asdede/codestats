#!/bin/bash
# Cache refresh script

echo "Refreshing cache at $(date)" >> /app/cache.log

/usr/local/bin/python3 /app/src/back/save_to_cache.py

echo "Cache refreshed!"