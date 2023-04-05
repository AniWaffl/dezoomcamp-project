FROM python:3.11.1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY data_producer/requirements.txt .
RUN pip install -r requirements.txt

RUN wget https://git.leroy-wrk.ru/leroy/events-history/raw/branch/master/events.csv -O events.csv -q

COPY data_producer/src .