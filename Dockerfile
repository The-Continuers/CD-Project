FROM python:3.9

RUN apt-get update -y && apt-get install -y spim

WORKDIR /app

COPY requirements.txt ./
RUN date
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x rtests.sh assert_run.sh run.sh

ENV PYTHONUNBUFFERED 1
