#!/usr/bin/env python  
import tornado.ioloop
import tornado.web

from msgCrypt.WXBizMsgCrypt import WXBizMsgCrypt
from msgCrypt.settings import msg_crypt

class MainHandler(tornado.web.RequestHandler):
    acccess_token=''
    def get(self):
        global msgDecode
        msg_signature = self.get_argument("msg_signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        echostr = self.get_argument("echostr", "")
        ret,replyEchoStr = msgDecode.VerifyURL(sMsgSignature=msg_signature,sTimeStamp=timestamp,sNonce=nonce,sEchoStr=echostr)
        self.write(replyEchoStr)
    def post(self):
        global msgDecode


application = tornado.web.Application([
    (r"^/api/public/{0,1}",MainHandler),
])

def test():
    global msgDecode
    print msgDecode.UpdateAccessToken()


if __name__=="__main__":
    # application.listen(8002)
    # tornado.ioloop.IOLoop.instance().start()
    test()