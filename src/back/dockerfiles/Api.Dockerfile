FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron supervisor

COPY src/back/API.py src/back/API.py
COPY src/back/github_gather.py ./src/back/github_gather.py
COPY src/back/gitlab_gather.py ./src/back/gitlab_gather.py
COPY src/back/waka_gather.py ./src/back/waka_gather.py
COPY src/back/save_to_cache.py ./src/back/save_to_cache.py
COPY src/back/refresh_cache.sh ./refresh_cache.sh

COPY .env ./.env

COPY src/back/dockerfiles/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip install --no-cache-dir fastapi[standard] requests



#RUN sh /app/refresh_cache.sh > /app/refresh_cache_output.log 2>&1


CMD ["supervisord","-c", "/etc/supervisor/conf.d/supervisord.conf"]