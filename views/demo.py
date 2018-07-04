#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import requests
import os

import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from msgCrypt import MSGCRYPTMAP,logger,BASE_DIR
from msgCrypt import ierror
from msgCrypt import CallBackMsg, PositiveImageMsg, PositiveTextMsg
from handler import getHandler

__all__ = ['DemoMsgHandler','DemoUserHandler','DemoVerifyHandler']


class DemoVerifyHandler(tornado.web.RequestHandler):

    def get_msg(self):
        msg_signature = self.get_argument("msg_signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        return msg_signature, timestamp, nonce

    # verify URL
    def get(self):
        msg_signature, timestamp, nonce = self.get_msg()
        echostr = self.get_argument("echostr", "")
        msg = CallBackMsg(msg_signature, timestamp, nonce)
        try:
            ret, replyEchoStr = msg.verifyURL(sEchoStr=echostr, sMsgCrypt=MSGCRYPTMAP['demo'])
        except Exception as e:
            logger.exception(e)
            self.write(e)
        else:
            logger.debug("verify url ret:{}====replyEchoStr:{}".format(ret, replyEchoStr))
            self.write(replyEchoStr)

    # handle received message
    def post(self):
        msg_signature, timestamp, nonce = self.get_msg()
        msg = CallBackMsg(msg_signature, timestamp, nonce)
        ret, xml_content = msg.decodePOST(sPostData=self.request.body, sMsgCrypt=MSGCRYPTMAP['demo'])
        if ret != ierror.WXBizMsgCrypt_OK:
            logger.error("decode post error:{}".format(ret))
            self.set_status(403, "fail to parse post")
        else:
            handler = getHandler(xml_content)
            if handler:
                to_xml = handler(xml_content, MSGCRYPTMAP['demo'])
                logger.debug(to_xml)
                ret, encrypt_xml = MSGCRYPTMAP['demo'].EncryptMsg(sNonce=nonce, sReplyMsg=str(to_xml))
                if ret != ierror.WXBizMsgCrypt_OK:
                    logger.error("decode post error:{}".format(ret))
                    self.set_status(403, "fail to encryp post")
                else:
                    self.write(encrypt_xml)
            self.finish()


class DemoMsgHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)

    @run_on_executor
    def send_text_msg(self, msg, toUser, toParty, toTag):
        txtmsg = PositiveTextMsg(
            access_token=MSGCRYPTMAP['demo'].access_token,
            agentid=MSGCRYPTMAP['demo'].agentID,
            toUser=toUser,
            toParty=toParty,
            toTag=toTag
        )
        txtmsg.setContent(msg)
        res = txtmsg.send()
        logger.debug(res.content)

    @run_on_executor
    def send_img_msg(self, toUser, toParty, toTag):
        imgmsg = PositiveImageMsg(
            access_token=MSGCRYPTMAP['demo'].access_token,
            agentid=MSGCRYPTMAP['demo'].agentID,
            toUser=toUser,
            toParty=toParty,
            toTag=toTag
        )
        try:
            with open('assets/image/temp.jpg', 'rb') as test_img:
                imgmsg.setImage(test_img, MSGCRYPTMAP['demo'])
                res = imgmsg.send()
                logger.debug(res)
        except Exception as e:
            logger.exception(e)

    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        toUser = self._read_to_target(data.get('toUser', ''))
        toParty = self._read_to_target(data.get('toParty', ''))
        toTag = self._read_to_target(data.get('toTag', ''))
        msg_type = data.get('type', None)
        if toUser and not isinstance(toUser,list):
            toUser=[toUser]
        if not (toParty or toUser or toTag):
            toUser = '@all'

        logger.info('positive send msg > target > toUser:{},toParty:{},toTag:{}'.format(toUser,toParty,toTag))
        if msg_type:
            if msg_type == 'text':
                self.send_text_msg(data.get('content', ''), toUser=toUser, toParty=toParty,toTag=toTag)
            elif msg_type == 'img':
                self.send_img_msg(toUser, toParty, toTag)
        self.write('finished')
        self.finish()

    @staticmethod
    def _read_to_target(target):
        if target.find(',') > 0:
            return target.split(',')
        else:
            return target


class DemoUserHandler(tornado.web.RequestHandler):

    def get(self):
        userid = self.get_argument("userid", "")
        res = requests.get(
            'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={}&userid={}'.format(
                MSGCRYPTMAP['demo'].access_token, userid),
            verify=False, timeout=1
        )
        res.raise_for_status()
        self.write(res.content)

