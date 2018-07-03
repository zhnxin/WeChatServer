#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from .WXBizMsgCrypt import WXBizMsgCrypt
from .settings import CONFIG,logger

def loadMsgCryptMap():
    MsgCryptMap={}
    CorpID = CONFIG['wechat']['CorpID']
    for app,args in CONFIG['wechat']['app'].items():
        MsgCryptMap[app] = WXBizMsgCrypt(sToken=args['Token'],
         sEncodingAESKey=args['EncodingAESKey'],
         sCorpId=CorpID,sAgentId=args['AgentId'], sCorpsecret=args['Secret'])
    return MsgCryptMap

MSGCRYPTMAP = loadMsgCryptMap()