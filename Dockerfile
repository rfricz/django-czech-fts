FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONMALLOC=mimalloc

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends curl

WORKDIR /app
COPY ./Pipfile* ./
RUN pip install --upgrade pip && \
    pip install --upgrade pipenv

RUN pipenv sync --system

COPY ./fts/ ./fts
COPY ./static/ ./static
COPY --chmod=755 ./manage.py ./gunicorn.conf.py ./docker/wsgi-entrypoint.sh ./

ENTRYPOINT [ "./wsgi-entrypoint.sh" ]
