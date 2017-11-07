#!/usr/bin/env python  
import tornado.ioloop
import tornado.web

from msgCrypt.WXBizMsgCrypt import WXBizMsgCrypt
from msgCrypt.settings import msg_crypt,logger

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        msg_signature = self.get_argument("msg_signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        echostr = self.get_argument("echostr", "")
        ret,replyEchoStr = msg_crypt.VerifyURL(sMsgSignature=msg_signature,sTimeStamp=timestamp,sNonce=nonce,sEchoStr=echostr)
        logger.debug("verify url ret:{}====replyEchoStr:{}".format(ret,replyEchoStr))
        self.write(replyEchoStr)
    def post(self):
        pass


application = tornado.web.Application([
    (r"^/api/public/{0,1}",MainHandler),
])

def test():
    print msg_crypt.UpdateAccessToken()


if __name__=="__main__":
    application.listen(8002)
    tornado.ioloop.IOLoop.instance().start()
    # test()