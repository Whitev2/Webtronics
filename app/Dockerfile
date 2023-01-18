FROM python:3.11-buster

ENV PYTHONUNBUFFERED=1

LABEL version = '1'
LABEL master = 'Webtronics task'

RUN mkdir /webtron
WORKDIR /webtron



COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# for migrations
COPY migrations .
COPY alembic.ini .

COPY src .

