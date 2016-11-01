# -*- coding: utf-8 -*-
__author__ = 'blfeng'
__mail__ = 'wenyefbl@163.com'
__date__ = '2016-10-26'
__version = 1.0
import logging
class logdebug:
    def loginfo(self,log_path,message):
        self.message = message
        self.log_path = log_path
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=self.log_path+"/cluster.log",
                filemode='w')
        logging.info(self.message)
    def logerror(self,log_path,message):
        self.message = message
        self.log_path = log_path
        logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=self.log_path+"/cluster.log",
                filemode='w')
        logging.error(message)
