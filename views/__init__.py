#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from .demo import *
from msgCrypt import MSGCRYPTMAP,logger

def updateAccessToken():
    for name, app in MSGCRYPTMAP.items():
        logger.debug('access_token update:%s' % name)
        app.UpdateAccessToken()