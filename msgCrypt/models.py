#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import xmltodict
import time

from settings import msg_crypt
from WXBizMsgCrypt import XMLParse, throw_exception, FormatException
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


class MsgModel(object):
    def __init__(self, xml_contend):
        self.content = xml_contend
        self.toUser = xml_contend['xml']['FromUserName']
        self.fromUser = xml_contend['xml']['ToUserName']


class TextMsg(MsgModel):
    TEXT_MSG_TEMP = """<xml>
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
        resp_xml = self.TEXT_MSG_TEMP % resp_dict
        return resp_xml
