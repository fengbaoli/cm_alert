# -*- coding: utf-8 -*-
__author__ = 'blfeng'
__mail__ = 'wenyefbl@163.com'
__date__ = '2016-10-26'
__version = 1.0
from cm_cluster.get_clusters import GetCluster
from alert.alert_send import AlertSend
from printlog.debug import logdebug
import os,re,time
import ConfigParser
#读取配置文件
cf = ConfigParser.ConfigParser()
cf.read(os.getcwd()+"/conf/cm_get.conf")
host = cf.get("cm","host")
port = int(cf.get("cm","port"))
username = cf.get("cm","username")
password = cf.get("cm","password")
backup_path = cf.get("backup","backup_path")
log_path = cf.get("log","log_path")
#实例化
getcm = GetCluster(host=host,port = port ,username = username,password = password)
sendm=AlertSend()
log = logdebug()
#sendmessage = AlertSend.sendmessage(mc_object="",message="",host_ip="",hostname="")
#主机列表
hostdic = getcm.get_hosts()
#cm service列表
cm_list =  getcm.services()
#cm 集群名
c_name = getcm.cluster()

#get rolse
roles=getcm.get_roles(cluster_name=c_name,services=cm_list)
#获取配置
conf = getcm.get_config(cluster_name=c_name,roles=roles)
if not os.path.exists(backup_path):
    os.mkdir(backup_path)

backup_filename ="%s/%s-%s" % (backup_path,time.strftime('%Y-%m-%d-%H-%M-%S'),"cm_all_config.txt")
file = open (backup_filename,"a+")
for s in conf:
    host_ipaddress = s['host_ipaddress']
    service_name = s['service_name']
    roles_name = s['roles_name']
    config_key = s['config_key']
    values = s['values']
    message = "ip:"+host_ipaddress+"|service_name:"+service_name+"|roles_name:"+roles_name+"|config_key:"+config_key+"|values:"+values+"\n"
    file.write(message)
file.close()    
message="backup succeeded!"
log.loginfo(log_path,message)
