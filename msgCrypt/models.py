#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import time
import types

import xmltodict
from .ierror import *
import json
import requests
from .WXBizMsgCrypt import throw_exception, FormatException

"""
# @param source_type: 公众平台上传素材类型：图片（image）、语音（voice）、视频（video），普通文件（file）
"""


class CallBackMsg(object):
    def __init__(self, msg_signature, timestamp, nonce, msg_encrypt=None):
        self.msg_encrypt = msg_encrypt
        self.msg_signature = msg_signature
        self.timestamp = timestamp
        self.nonce = nonce

    def verifyURL(self, sEchoStr, sMsgCrypt):
        ret, replyEchoStr = sMsgCrypt.VerifyURL(sMsgSignature=self.msg_signature, sTimeStamp=self.timestamp,
                                                sNonce=self.nonce, sEchoStr=sEchoStr)
        return ret, replyEchoStr

    def decodePOST(self, sPostData, sMsgCrypt):
        ret, xml_content = sMsgCrypt.DecryptMsg(sMsgSignature=self.msg_signature, sTimeStamp=self.timestamp,
                                                sNonce=self.nonce,
                                                sPostData=sPostData)
        if ret != WXBizMsgCrypt_OK:
            return ret, None
        else:
            dataDict = xmltodict.parse(xml_content)
            return ret, dataDict


class PassiveMsg(object):
    def __init__(self, xml_contend):
        self.content = xml_contend
        self.toUser = xml_contend['xml']['FromUserName']
        self.fromUser = xml_contend['xml']['ToUserName']


class PassiveTextMsg(PassiveMsg):
    MSG_TEMP = """<xml>
   <ToUserName><![CDATA[{resp_dict[toUser]}]]></ToUserName>
   <FromUserName><![CDATA[{resp_dict[fromUser]}]]></FromUserName> 
   <CreateTime>{resp_dict[timestamp]}</CreateTime>
   <MsgType><![CDATA[text]]></MsgType>
   <Content><![CDATA[{resp_dict[msg]}]]></Content>
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
        resp_xml = self.MSG_TEMP.format(resp_dict=resp_dict)
        return resp_xml


class PassiveImageMsg(PassiveMsg):
    MSG_TEMP = """<xml>
   <ToUserName><![CDATA[{resp_dict[toUser]}]]></ToUserName>
   <FromUserName><![CDATA[{resp_dict[fromUser]}]]></FromUserName>
   <CreateTime>{resp_dict[timestamp]}</CreateTime>
   <MsgType><![CDATA[image]]></MsgType>
   <Image>
       <MediaId><![CDATA[{resp_dict[media_id]}]]></MediaId>
   </Image>
</xml>"""

    def generate(self, media_id, timestamp=None):
        if timestamp is None:
            timestamp = str(int(time.time()))
        resp_dict = {
            "toUser": self.toUser,
            "fromUser": self.fromUser,
            "media_id": media_id,
            "timestamp": timestamp
        }
        resp_xml = self.MSG_TEMP.format(resp_dict=resp_dict)
        return resp_xml

    def generateFromImage(self,imageFile,sMsgCrypt,timestamp=None):
        image_id = sMsgCrypt.UploadImage(imageFile)
        if image_id:
            print("upload image:{}".format(image_id))
            return self.generate(image_id,timestamp)
        else:
            throw_exception("[error]: failed in uploading images !", FormatException)
            return None


class PositiveMsg(object):
    """
    # 构造函数
    # @param access_token: 公众平台上，access_token
    # @param agentid: 公众平台上，企业应用ID
    # @param toUser: 发送目标，接受UserID 和 [UserID1,UserID2,...],默认@all
    # @param toParty: 发送目标，接受PartyID 和 [PartyID1,PartyID2,...]
    #@param toTag: 发送目标，接受PTagID 和 [TagID1,TagID2,...]
    """

    def __init__(self, access_token, agentid, toUser='', toParty='', toTag=''):
        self.sendURL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token)
        self.access_token = access_token
        if toUser == '@all':
            touser = toUser
            toparty = toParty
            totag = toTag
        elif isinstance(toUser, list):
            touser = '|'.join(toUser)
            toparty = toParty
            totag = toTag
        else:
            touser = ''
            if isinstance(toParty, list):
                toparty = '|'.join(toParty)
            else:
                toparty = toParty
            if isinstance(toTag, list):
                totag = '|'.join(toTag)
            else:
                totag = toTag
        self.messageBody = {
            "touser": touser,
            "toparty": toparty,
            "totag": totag,
            "agentid": agentid
        }

    def send(self):
        header = {
            'content-type':'application/json',
            'cache-control':'no-cache'
        }
        message_body = json.dumps(self.messageBody,ensure_ascii=False).encode('utf-8')
        res = requests.post(self.sendURL, data=message_body,headers=header)
        return res


class PositiveTextMsg(PositiveMsg):
    def __init__(self, content='',**kwargs):
        super(PositiveTextMsg, self).__init__(**kwargs)
        self.messageBody['msgtype'] = 'text'
        self.messageBody['text'] = {'content': content}

    def setContent(self, content):
        self.messageBody['text']['content'] = content


class PositiveImageMsg(PositiveMsg):
    def __init__(self, **kwargs):
        super(PositiveImageMsg, self).__init__(**kwargs)
        self.messageBody['msgtype'] = 'image'

    def setImage(self, imageFile, sMsgCrypt):
        image_id = sMsgCrypt.UploadImage(imageFile)
        print("upload image:{}".format(image_id))
        if image_id:
            self.messageBody['image'] = {"media_id": image_id}
        else:
            throw_exception("upload image failed!", FormatException)

    def setImageID(self,image_id):
        self.messageBody['image'] = {"media_id": image_id}

