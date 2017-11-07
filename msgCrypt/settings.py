#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
import ConfigParser
from .WXBizMsgCrypt import WXBizMsgCrypt

config = ConfigParser.ConfigParser()
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
config.read(os.path.join(BASE_DIR, 'wechatserver.conf'))

CorpID = config.get('work','CorpID')
Token = config.get('app','Token')
EncodingAESKey = config.get('app','EncodingAESKey')
Corpsecret = config.get('app','Corpsecret')

msg_crypt = WXBizMsgCrypt(sToken=Token,sEncodingAESKey=EncodingAESKey,sCorpID=CorpID,sCorpsecret=Corpsecret)
