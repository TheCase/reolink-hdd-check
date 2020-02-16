FROM python:3

ADD . /

RUN pip install -r requirements.txt

ENV NVR_ADDR=http://reolink-nvr.local
ENV NVR_USER=admin
ENV NVR_PASS=admin
ENV NVR_METH=http
ENV NVR_PORT=80
ENV SLACK_WH=http://placeholer.local
ENV POLL_INTERVAL=60

CMD ["python", "check.py"]
