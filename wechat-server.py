#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.options
from tornado.options import define, options

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from msgCrypt.settings import logger,IP,PORT,msg_crypt
from msgCrypt.models import CallBackMsg,TextMsg
from msgCrypt import ierror
define("port", default=PORT, help="run on the given port", type=int)
define("host", default=IP, help="run port on given host", type=str)

class MainHandler(tornado.web.RequestHandler):

    def get_msg(self):
        msg_signature = self.get_argument("msg_signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        return msg_signature,timestamp,nonce

    def get(self):
        msg_signature, timestamp, nonce = self.get_msg()
        echostr = self.get_argument("echostr", "")
        msg = CallBackMsg(msg_signature, timestamp, nonce)
        ret,replyEchoStr = msg.verifyURL(echostr)
        logger.debug("verify url ret:{}====replyEchoStr:{}".format(ret,replyEchoStr))
        self.write(replyEchoStr)

    def post(self):
        msg_signature, timestamp, nonce = self.get_msg()
        msg = CallBackMsg(msg_signature, timestamp, nonce)
        ret, xml_content = msg.decodePOST(sPostData=self.request.body)
        if ret != ierror.WXBizMsgCrypt_OK:
            self.set_status(403,"fail to parse post")
        else:
            textSend = TextMsg(xml_content)
            ret, encrypt_xml = msg_crypt.EncryptMsg(sNonce=nonce, sReplyMsg=textSend.generate(msg="功能未开发"))
            self.write(encrypt_xml)
            self.finish()

def main():

    application = tornado.web.Application([
        (r"^/api/public/{0,1}",MainHandler),
    ])    
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port, address=IP)
    tornado.ioloop.IOLoop.instance().start()

def test():
    msg_signature='6d0aa184173e0bc0569dfaab7287fcfeeae0ff54'
    timestamp='1509966115'
    nonce='LSUyzTUbgeDrG0J7'
    msg = CallBackMsg(msg_signature, timestamp, nonce)
    msg.generateReply("author：zhengxin")


if __name__=="__main__":
    print "Run server on %s:%s" % (options.host, options.port)
    main()
    # test()