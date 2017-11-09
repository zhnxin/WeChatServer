#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from .models import PassiveTextMsg, EventClickHandlerFactory,PassiveImageMsg
import random

clickHandlerFactory = EventClickHandlerFactory()

defaultMsg = ['(*゜ー゜*)', '(￣△￣；)', '(。_。)', '(°ー°〃)', '￣△￣', '富强', '民主', '文明', '和谐', '自由', '平等', '公正', '法治', '爱国', '敬业',
              '诚信', '友善']


def defaultHandler(xml_contend,sMsgCrypt):
    textSend = PassiveTextMsg(xml_contend)
    msg = defaultMsg[random.randint(0, len(defaultMsg) - 1)]
    to_xml = textSend.generate(msg=msg)
    return to_xml

def getHandler(xml_content):
    if xml_content['xml']['MsgType'] == 'event' and xml_content['xml']['Event'] == 'click':
        handle = clickHandlerFactory.get(xml_content['xml']['EventKey'])
        return handle
    else:
        return None


def eventHandlerDemo(xml_content,sMsgCrypt):
    textSend = PassiveTextMsg(xml_contend)
    msg = defaultMsg[random.randint(0, len(defaultMsg) - 1)]
    to_xml = textSend.generate(msg=msg)
    return to_xml

def enentHandlerDemo_image(xml_content,sMsgCrypt):
    imageSend = PassiveImageMsg(xml_contend)
    with open('image/temp.jpg','rb') as imgFile:
        to_xml = imageSend.generateFromImage(imgFile,sMsgCrypt)
    return to_xml


clickHandlerFactory.put('10001', eventHandlerDemo)
clickHandlerFactory.put('10002', enentHandlerDemo_image)