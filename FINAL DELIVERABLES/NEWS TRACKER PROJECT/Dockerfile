FROM python:3.10-slim-buster

WORKDIR /news-tracker

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install libxml2
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]