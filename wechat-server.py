#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.options
from tornado.options import define, options
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from msgCrypt.settings import logger, IP, PORT, MSGCRYPTMAP
from msgCrypt.models import CallBackMsg,PositiveImageMsg,PositiveTextMsg
from msgCrypt import ierror
from msgCrypt.handlerFactory import getHandler

define("port", default=PORT, help="run on the given port", type=int)
define("host", default=IP, help="run port on given host", type=str)


class DemoHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)
    @run_on_executor
    def sendMsg(self):
        # txtmsg = PositiveTextMsg(access_token=MSGCRYPTMAP['demo'].UpdateAccessToken(),agentid=MSGCRYPTMAP['demo'].agentID)
        # txtmsg.setContent("（づ￣3￣）づ╭❤～")
        # txtmsg.send()
        imgmsg = PositiveImageMsg(access_token=MSGCRYPTMAP['demo'].UpdateAccessToken(),agentid=MSGCRYPTMAP['demo'].agentID)
        with open('msgCrypt/test.jpg', 'wr') as test_img:
            imgmsg.setImage(test_img, MSGCRYPTMAP['demo'])
            imgmsg.send()

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
        ret, replyEchoStr = msg.verifyURL(sEchoStr=echostr, sMsgCrypt=MSGCRYPTMAP['demo'])
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
                ret, encrypt_xml = MSGCRYPTMAP['demo'].EncryptMsg(sNonce=nonce, sReplyMsg=str(to_xml))
                if ret != ierror.WXBizMsgCrypt_OK:
                    logger.error("decode post error:{}".format(ret))
                    self.set_status(403, "fail to encryp post")
                else:
                    self.write(encrypt_xml)
            #self.sendMsg()
            self.finish()


def updateAccessToken():
    for name, app in MSGCRYPTMAP.items():
        logger.debug('access_token update:%s' % name)
        app.UpdateAccessToken()


def main():
    application = tornado.web.Application([
        (r"^/api/public/{0,1}", DemoHandler),
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
