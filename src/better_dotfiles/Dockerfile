FROM python:3.11.1

WORKDIR /app
ARG requirements=requirements/production.txt

COPY . /app

RUN /usr/local/bin/python -m pip install --upgrade pip && pip install --no-cache-dir -e . --no-cache-dir -r $requirements
