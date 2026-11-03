FROM python:3.14-slim AS app

WORKDIR /app

COPY --chown=1000:1000 requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

USER 1000

COPY --chown=1000:1000 . .
