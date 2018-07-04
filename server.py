#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpserver
import tornado.options
from tornado.options import define, options

from msgCrypt import IP, PORT
from views import DemoVerifyHandler,DemoMsgHandler,DemoUserHandler,updateAccessToken

define("port", default=PORT, help="run on the given port", type=int)
define("host", default=IP, help="run port on given host", type=str)



def main():
    application = tornado.web.Application([
        (r"^/public/api/{0,1}", DemoVerifyHandler),
        (r"^/api/demo/v1/msg/{0,1}",DemoMsgHandler),
        (r"^/api/demo/v1/user/{0,1}",DemoUserHandler)
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
