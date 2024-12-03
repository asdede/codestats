#!/bin/bash
# Cache refresh script

echo "Refreshing cache at $(date)" >> /app/cache.log
python ./src/back/save_to_cache.py
echo "Cache refreshed!"