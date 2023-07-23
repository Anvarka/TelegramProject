FROM python:3.8-slim AS bot


RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN pip3 install -r ./requirements.txt
RUN chmod +x main.py

CMD python3 main.py;