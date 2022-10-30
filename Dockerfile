FROM python:3.12-rc-slim

ADD . /

RUN pip install -r requirements.txt

ENV NVR_METH=http
ENV NVR_ADDR=reolink-nvr.local
ENV NVR_USER=admin
ENV NVR_PASS=admin
ENV NVR_PORT=80
ENV SLACK_WH=http://fakehook.local
ENV POLL_INTERVAL=60

CMD ["python", "check.py"]
