#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from msgCrypt.models import PassiveTextMsg, PassiveImageMsg
from .models import PoolTextMsgHandlerFactory, EventClickHandlerFactory

textHandlerFactory = PoolTextMsgHandlerFactory()
clickHandlerFactory = EventClickHandlerFactory(textHandlerFactory)


# handler factory 入口
def getHandler(xml_content):
    if xml_content['xml']['MsgType'] == 'event' and xml_content['xml']['Event'] == 'click':
        handle = clickHandlerFactory.get(xml_content['xml']['EventKey'])
        return handle
    else:
        return None


import random

defaultMsg = ['富强', '民主', '文明', '和谐', '自由', '平等', '公正', '法治', '爱国', '敬业',
              '诚信', '友善', '( •̀ .̫ •́ )✧', '(つд⊂)', ' (•౪• )',
              ' (๑•̀ㅂ•́) ✧', 'ლ(╹◡╹ლ)', '_(:з」∠)_', '( •̥́ ˍ •̀ू )', 'Ծ‸Ծ', '～﹃～)~zZ',
              '(⺣◡⺣)', '(๑•́ ∀ •̀๑)', '(ง •̀_•́)ง', 'ฅ^ω^ฅ', '( ´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥`)',
              '(⇀‸↼‶)', '(⃘  ̂͘₎o̮₍ ̂͘ )⃘', 'ฅʕ•̫͡•ʔฅ', '(๑॔ᵒ̴̶̷◡  ˂̶๑॓)ゞ❣', 'ᕙ(⇀‸↼‵‵)ᕗ',
              '(ᵒ̤̑ ₀̑ ᵒ̤̑)', 'ヽ(ｏ`皿′ｏ)ﾉ', 'ー( ´ ▽ ` )ﾉ', '↺  ♫   ☼',
              '(*´・ω・`)⊃', '⊂(˃̶͈̀ε ˂̶͈́ ⊂ )))Σ≡=─', '_(´ཀ`」 ∠)_', '( ⸝⸝⸝°_°⸝⸝⸝ )', '∠( ᐛ 」∠)＿']


def defaultHandler(xml_contend, sMsgCrypt):
    textSend = PassiveTextMsg(xml_contend)
    msg = defaultMsg[random.randint(0, len(defaultMsg) - 1)]
    to_xml = textSend.generate(msg=msg)
    return to_xml


def eventHandlerDemo(xml_content, sMsgCrypt):
    textSend = PassiveTextMsg(xml_content)
    msg = defaultMsg[random.randint(0, len(defaultMsg) - 1)]
    to_xml = textSend.generate(msg=msg)
    return to_xml


def enentHandlerDemo_image(xml_content, sMsgCrypt):
    image_send = PassiveImageMsg(xml_content)
    with open('image/temp.jpg', 'rb') as imgFile:
        to_xml = image_send.generateFromImage(imgFile, sMsgCrypt)
    return to_xml


clickHandlerFactory.put('10001', eventHandlerDemo)
clickHandlerFactory.put('10002', enentHandlerDemo_image)
textHandlerFactory.put(u"颜文字", defaultHandler)
textHandlerFactory.put(u'溜了溜了', enentHandlerDemo_image)
