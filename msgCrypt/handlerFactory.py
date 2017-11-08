#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from .models import PassiveTextMsg, EventClickHandlerFactory
import random

clickHandlerFactory = EventClickHandlerFactory()

defaultMsg = ['(*゜ー゜*)', '(￣△￣；)', '(。_。)', '(°ー°〃)', '￣△￣', '富强', '民主', '文明', '和谐', '自由', '平等', '公正', '法治', '爱国', '敬业',
              '诚信', '友善']


def defaultHandler(xml_contend):
    textSend = PassiveTextMsg(xml_contend)
    msg = defaultMsg[random.randint(0, len(defaultMsg) - 1)]
    to_xml = textSend.generate(msg=msg)
    return to_xml


def getHandler(xml_contend):
    if (xml_contend['xml']['MsgType'] == 'event' and xml_contend['xml']['MsgType']['Event']):
        return clickHandlerFactory.get(xml_contend['xml']['EventKey'])
    else:
        return defaultHandler


def eventHandlerDemo(xml_content):
    textSend = PassiveTextMsg(xml_content)
    to_xml = textSend.generate(msg="点击的是：获取当前告警信息")
    return to_xml


clickHandlerFactory.put('10001', eventHandlerDemo)
