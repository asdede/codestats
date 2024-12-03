FROM python:3.12-slim

WORKDIR /app


COPY src/back/API.py src/back/API.py
COPY src/back/github_gather.py ./src/back/github_gather.py
COPY src/back/gitlab_gather.py ./src/back/gitlab_gather.py
COPY src/back/waka_gather.py ./src/back/waka_gather.py
COPY src/back/save_to_cache.py ./src/back/save_to_cache.py
COPY src/back/refresh_cache.sh ./refresh_cache.sh
COPY .env ./.env

RUN pip install --no-cache-dir fastapi[standard] requests

RUN apt-get update && apt-get install -y cron

# Refresh cache every 5 minutes
RUN echo "*/5 * * * * sh /app/refresh_cache.sh >> /app/cron.log 2>&1" > /etc/cron.d/refresh_cache && \
    chmod 0644 /etc/cron.d/refresh_cache && \
    crontab /etc/cron.d/refresh_cache && \
    chmod +x /app/refresh_cache.sh

RUN sh /app/refresh_cache.sh > /app/refresh_cache_output.log 2>&1


CMD cron && fastapi run  ./src/back/API.py && sh refresh_cache.sh