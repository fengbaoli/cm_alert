# -*- coding: utf-8 -*-
__author__ = 'blfeng'
__mail__ = 'wenyefbl@163.com'
__date__ = '2016-10-26'
__version = 1.0
import os
class AlertSend():
    def sendmessage(self,mc_object,message,host_ip,hostname):
        self.mc_object = mc_object
        self.message = message
        self.mc_host_address = host_ip
        self.mc_host = hostname
        cmd = '/sbin/msend -n @10.253.2.178:1828#mc -a ALARM  -r WARNING -b "mc_object=%s;msg=%s;mc_host_address=%s;mc_host=%s"' % (self.mc_object,self.message,self.mc_host_address,self.mc_host)
        os.system(cmd)
