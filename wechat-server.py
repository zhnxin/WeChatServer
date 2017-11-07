#!/usr/bin/env python  
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

from msgCrypt.WXBizMsgCrypt import WXBizMsgCrypt
from msgCrypt.settings import msg_crypt,logger,IP,PORT
define("port", default=PORT, help="run on the given port", type=int)
define("host", default=IP, help="run port on given host", type=str)

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

def main():

    application = tornado.web.Application([
        (r"^/api/public/{0,1}",MainHandler),
    ])    
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port, address=IP)
    tornado.ioloop.IOLoop.instance().start()

def test():
    print msg_crypt.UpdateAccessToken()


if __name__=="__main__":
    print "Run server on %s:%s" % (options.host, options.port)
    main()