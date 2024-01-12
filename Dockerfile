FROM python:3.9

RUN apt-get update && apt-get install -y build-essential python3-dev && apt-get clean

RUN pip install --upgrade pip

COPY requirements.txt /temp/requirements.txt
COPY smartschedule /smartschedule
WORKDIR /smartschedule

EXPOSE 8000

RUN pip install -r /temp/requirements.txt 

RUN adduser --disabled-password service-user

USER service-user