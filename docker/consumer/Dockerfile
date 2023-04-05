FROM python:3.11.1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY data_loader/requirements.txt .
RUN pip install -r requirements.txt

COPY data_loader/src .