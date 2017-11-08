#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import time
import types

import xmltodict

from settings import msg_crypt
import ierror


class CallBackMsg(object):
    def __init__(self, msg_signature, timestamp, nonce, msg_encrypt=None):
        self.msg_encrypt = msg_encrypt
        self.msg_signature = msg_signature
        self.timestamp = timestamp
        self.nonce = nonce

    def verifyURL(self, sEchoStr):
        ret, replyEchoStr = msg_crypt.VerifyURL(sMsgSignature=self.msg_signature, sTimeStamp=self.timestamp,
                                                sNonce=self.nonce, sEchoStr=sEchoStr)
        return ret, replyEchoStr

    def decodePOST(self, sPostData):
        ret, xml_content = msg_crypt.DecryptMsg(sMsgSignature=self.msg_signature, sTimeStamp=self.timestamp,
                                                sNonce=self.nonce,
                                                sPostData=sPostData)
        if ret != ierror.WXBizMsgCrypt_OK:
            return ret, None
        else:
            dataDict = xmltodict.parse(xml_content)
            return ret, dataDict


class PassiveMsgModel(object):
    def __init__(self, xml_contend):
        self.content = xml_contend
        self.toUser = xml_contend['xml']['FromUserName']
        self.fromUser = xml_contend['xml']['ToUserName']


class PassiveTextMsg(PassiveMsgModel):
    MSG_TEMP = """<xml>
   <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
   <FromUserName><![CDATA[%(fromUser)s]]></FromUserName> 
   <CreateTime>%(timestamp)s</CreateTime>
   <MsgType><![CDATA[text]]></MsgType>
   <Content><![CDATA[%(msg)s]]></Content>
</xml>"""

    def generate(self, msg, timestamp=None):
        if timestamp is None:
            timestamp = str(int(time.time()))
        resp_dict = {
            "toUser": self.toUser,
            "fromUser": self.fromUser,
            "msg": msg,
            "timestamp": timestamp
        }
        resp_xml = self.MSG_TEMP % resp_dict
        return resp_xml

class PassiveImageMsg(PassiveMsgModel):
    MSG_TEMP = """<xml>
   <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
   <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
   <CreateTime>%(timestamp)</CreateTime>
   <MsgType><![CDATA[image]]></MsgType>
   <Image>
       <MediaId><![CDATA[%(media_id)s]]></MediaId>
   </Image>
</xml>"""

    def generate(self,media_id,timestamp=None):
        if timestamp is None:
            timestamp = str(int(time.time()))
        resp_dict = {
            "toUser": self.toUser,
            "fromUser": self.fromUser,
            "media_id": media_id,
            "timestamp": timestamp
        }
        resp_xml = self.MSG_TEMP % resp_dict
        return resp_xml

class EventClickHandlerFactory(object):
    def __init__(self):
        self.factory = {}

    def put(self,buttonKey,func):
        assert isinstance(func,types.FunctionType)
        self.factory[buttonKey] = func

    def get(self,buttonKey):
        self.factory.get(buttonKey,None)

