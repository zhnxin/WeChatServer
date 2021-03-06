#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import yaml
import logging

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def load_conf(conf_file_name):
    path = os.path.join(BASE_DIR, conf_file_name)
    if os.path.exists(path):
        return yaml.load(open(path,'r'))
    return None


def get_conf():
    configuration = load_conf('application.yml')
    if not configuration:
        configuration = load_conf('application.yaml')
    return configuration


CONFIG = get_conf()
IP = CONFIG['server'].get('ip', '0.0.0.0')
PORT = CONFIG['server'].get("port", '8000')
LOG_LEVEL = CONFIG['server'].get("loglever", 'debug')


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
    logger_f = logging.getLogger('')
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f


logger = set_log(LOG_LEVEL)
