#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from settings import msg_crypt
import ierror
import xmltodict


class CallBackMsg(object):
    def __init__(self,msg_signature, timestamp, nonce,msg_encrypt=None):
        self.msg_encrypt = msg_encrypt
        self.msg_signature = msg_signature
        self.timestamp = timestamp
        self.nonce = nonce

    def verifyURL(self,sEchoStr):
        ret, replyEchoStr = msg_crypt.VerifyURL(sMsgSignature=self.msg_signature,sTimeStamp=self.timestamp,sNonce=self.nonce,sEchoStr=sEchoStr)
        return ret,replyEchoStr

    def __decodePOST(self,sPostData):
        ret,xml_content = msg_crypt.DecryptMsg(sMsgSignature=self.msg_signature, sTimeStamp=self.timestamp, sNonce=self.nonce,
                             sPostData=sPostData)
        if ret != ierror.WXBizMsgCrypt_OK:
            return ret,None
        else:
            dataDict = xmltodict.parse(xml_content)
            return ret,dataDict
