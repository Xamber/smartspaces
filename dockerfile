FROM        python:3.5.1

RUN         mkdir -p /usr/src/app
WORKDIR     /usr/src/app

COPY        . /usr/src/app/
RUN         pip install -v -r requirements.txt

CMD         [ "python", "./server.py" ]