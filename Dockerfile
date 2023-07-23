FROM python:3.8-slim AS bot


RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN mkdir -p /codebase /storage
ADD . /codebase
WORKDIR /codebase

RUN pip3 install -r requirements.txt
RUN chmod +x /codebase/main.py

CMD python3 /codebase/main.py;