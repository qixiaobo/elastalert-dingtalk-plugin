#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xuyaoqiang
@contact: xuyaoqiang@gmail.com
@date: 2017-09-14 17:35
@version: 0.0.0
@license:
@copyright:

"""
import json

import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException
from requests.exceptions import RequestException


class DingTalkAlerter(Alerter):
    required_options = frozenset(['dingtalk_webhook', 'dingtalk_msgtype'])

    def __init__(self, rule):
        super(DingTalkAlerter, self).__init__(rule)
        self.dingtalk_webhook_url = self.rule['dingtalk_webhook']
        self.dingtalk_msgtype = self.rule.get('dingtalk_msgtype', 'text')
        self.dingtalk_isAtAll = self.rule.get('dingtalk_isAtAll', False)
        self.dingtalk_title = self.rule.get('dingtalk_title', '')
        self.dingtalk_messageUrl = self.rule.get('dingtalk_messageUrl', 'http://log.f6car.com')

    def format_body(self, body):
        return body.encode('utf8')

    def get_payload(self):

        if self.dingtalk_msgtype == 'text':
            return {
                "msgtype": self.dingtalk_msgtype,
                "text": {
                    "content": body + self.dingtalk_messageUrl
                },
                "at": {
                    "isAtAll": self.dingtalk_isAtAll
                }
            }
        elif self.dingtalk_msgtype == 'link':
            return {
                "msgtype": self.dingtalk_msgtype,
                "link": {
                    "text": body,
                    "picUrl": "",
                    "messageUrl": self.dingtalk_messageUrl
                }
            }

    def alert(self, matches):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=utf-8"
        }
        body = self.create_alert_body(matches)
        payload = {
            "msgtype": self.dingtalk_msgtype,
            "text": {
                "content": body
            },
            "at": {
                "isAtAll": self.dingtalk_isAtAll
            }
        }
        try:
            response = requests.post(self.dingtalk_webhook_url,
                                     data=json.dumps(payload, cls=DateTimeEncoder),
                                     headers=headers)
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error request to Dingtalk: {0}".format(str(e)))

    def get_info(self):
        return {
            "type": "dingtalk",
            "dingtalk_webhook": self.dingtalk_webhook_url
        }
        pass
