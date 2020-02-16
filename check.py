#!/usr/bin/env python3

import os
import requests
import json
import time

nvr_addr = os.getenv('NVR_ADDR', 'reolink.local')
nvr_user = os.getenv('NVR_USER', 'admin')
nvr_pass = os.getenv('NVR_PASS', 'admin')
nvr_meth = os.getenv('NVR_METH', 'http')
nvr_port = os.getenv('NVR_PORT', '80')

slack_wh = os.getenv('SLACK_WH', 'http://fakehook.local')

poll_int = os.getenv('POLL_INTERVAL', 60)

cgi_uri = 'cgi-bin/api.cgi?cmd='

import logging
fmt="%(asctime)s - %(levelname)-s - %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)
log = logging.getLogger(__name__)

while True:
  # get token
  payload = [{ "cmd": "Login", "action": 0,
              "param": {
              "User": { "userName": nvr_user, "password": nvr_pass } }
            }]
  cmd = 'Login'
  url = '{}://{}:{}/{}{}'.format(nvr_meth, nvr_addr, nvr_port, cgi_uri, cmd)
  ret = requests.post(url, data=json.dumps(payload)).json()
  token = ret[0]['value']['Token']['name']

  # get hdd status
  cmd = 'GetHddInfo'
  url = '{}://{}:{}/{}{}&token={}'.format(nvr_meth, nvr_addr, nvr_port, cgi_uri, cmd, token)
  ret = requests.get(url).json()
  capy = ret[0]['value']['HddInfo'][0]['capacity']
  size = ret[0]['value']['HddInfo'][0]['size']

  log.info("cap: {} size: {}".format(capy, size))

  # reboot if necessary
  if capy == 0 and size == 0:
    # send slack post
    log.info("post to slack")
    post = {"text": "rebooting reolink DVR - lost HDD"}
    try:
      json_data = json.dumps(post)
      req = requests.post(slack_wh,
                          data=json_data.encode('ascii'),
                          headers={'Content-Type': 'application/json'})
    except Exception as em:
      log.error("EXCEPTION: " + str(em))

    # exec reboot
    cmd = 'Reboot'
    url = '{}://{}:{}/{}{}&token={}'.format(nvr_meth, nvr_addr, nvr_port, cgi_uri, cmd, token)
    ret = requests.get(url).json()
    log.info(ret)


  # logout
  cmd = 'Logout'
  url = '{}://{}:{}/{}{}&token={}'.format(nvr_meth, nvr_addr, nvr_port, cgi_uri, cmd, token)
  ret = requests.get(url).json()
  log.info(ret)


  log.info("sleeping {} seconds...".format(poll_int))
  time.sleep(int(poll_int))
