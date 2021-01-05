FROM python:3.7

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r pip-requirements.txt
LABEL org.opencontainers.image.source https://github.com/SENERGY-Platform/import-dwd-alerts
CMD [ "python", "./main.py" ]
