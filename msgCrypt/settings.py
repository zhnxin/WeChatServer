#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
import ConfigParser
import logging
from .WXBizMsgCrypt import WXBizMsgCrypt
from .models import EventClickHandlerFactory

config = ConfigParser.ConfigParser()
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
config.read(os.path.join(BASE_DIR, 'wechatserver.conf'))

CorpID = config.get('work','CorpID')
Token = config.get('app','Token')
EncodingAESKey = config.get('app','EncodingAESKey')
Corpsecret = config.get('app','Corpsecret')

IP = config.get('base', 'IP')
PORT = config.get('base', 'Port')
LOG_LEVEL = config.get('base', 'LogLevel')

msg_crypt = WXBizMsgCrypt(sToken=Token,sEncodingAESKey=EncodingAESKey,sCorpID=CorpID,sCorpsecret=Corpsecret)

def set_log(level, filename='wechatserver.log'):
    """
    return a log file object
    根据提示设置log打印
    """
    log_file = os.path.join(BASE_DIR, filename)
    # if not os.path.isfile(log_file):
    #     os.mknod(log_file)
    #     os.chmod(log_file, 0777)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    logger_f = logging.getLogger('wechat')
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f

logger = set_log(LOG_LEVEL)

