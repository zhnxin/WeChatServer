#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import requests
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.options
from tornado.options import define, options
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from msgCrypt.settings import logger, IP, PORT

from msgCrypt.utils import MSGCRYPTMAP
from msgCrypt.models import CallBackMsg,PositiveImageMsg,PositiveTextMsg
from msgCrypt import ierror
from handler.handlerFactory import getHandler

define("port", default=PORT, help="run on the given port", type=int)
define("host", default=IP, help="run port on given host", type=str)


class DemoHandler(tornado.web.RequestHandler):

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
                to_xml = handler(xml_content,MSGCRYPTMAP['demo'])
                logger.debug(to_xml)
                ret, encrypt_xml = MSGCRYPTMAP['demo'].EncryptMsg(sNonce=nonce, sReplyMsg=str(to_xml))
                if ret != ierror.WXBizMsgCrypt_OK:
                    logger.error("decode post error:{}".format(ret))
                    self.set_status(403, "fail to encryp post")
                else:
                    self.write(encrypt_xml)
            self.finish()

class ActiceMsgHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)

    @run_on_executor
    def send_text_msg(self,msg,toUser, toParty, toTag):
        txtmsg = PositiveTextMsg(
            access_token=MSGCRYPTMAP['demo'].access_token,
            agentid=MSGCRYPTMAP['demo'].agentID,
            toUser=toUser,
            toParty=toParty,
            toTag=toTag
            )
        txtmsg.setContent(msg)
        txtmsg.send()
        
    @run_on_executor
    def send_img_msg(self,toUser, toParty, toTag):
        imgmsg = PositiveImageMsg(
            access_token=MSGCRYPTMAP['demo'].access_token,
            agentid=MSGCRYPTMAP['demo'].agentID,
            toUser=toUser,
            toParty=toParty,
            toTag=toTag
        )
        with open('msgCrypt/test.jpg', 'r') as test_img:
            imgmsg.setImage(test_img, MSGCRYPTMAP['demo'])
            imgmsg.send()
    
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
    
        toUser=data.get('toUser','')
        toParty=data.get('toParty','')
        toTag=data.get('toTag','')
        msg_type = data.get('type',None)
        if not (toParty or toUser or toTag):
            toUser = '@all'
        if msg_type:
            if  msg_type == 'text':
                self.send_text_msg(data.get('content',''),toUser, toParty, toTag)
            elif msg_type == 'img':
                self.send_img_msg(toUser,toParty,toTag)
        self.write('finished')
        self.finish()

class DemoUserHandler(tornado.web.RequestHandler):
    
    def get(self):
        userid = self.get_argument("userid", "")
        res = requests.get(
            'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={}&userid={}'.format(MSGCRYPTMAP['demo'].access_token,userid),
             verify=False,timeout=1
            )
        res.raise_for_status()
        self.write(res.content)

def updateAccessToken():
    for name, app in MSGCRYPTMAP.items():
        logger.debug('access_token update:%s' % name)
        app.UpdateAccessToken()


def main():
    application = tornado.web.Application([
        (r"^/public/api/{0,1}", DemoHandler),
        (r"^/api/demo/v1/msg{0,1}",ActiceMsgHandler),
        (r"^/api/demo/v1/user{0,1}",ActiceMsgHandler)
    ])
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port, address=IP)
    # update per 1:59
    tornado.ioloop.PeriodicCallback(updateAccessToken, 7140000).start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    print("Run server on {}:{}".format(options.host, options.port))
    updateAccessToken()
    main()
