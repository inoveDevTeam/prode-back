FROM python:3.10.6

ENV PYTHONUNBUFFERED 1

# Locale (idioma)
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LANG es_AR.UTF-8
ENV LC_ALL es_AR.UTF-8
ENV LANGUAGE es_AR.UTF-8

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /prode/back
