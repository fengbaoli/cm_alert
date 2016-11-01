# -*- coding: utf-8 -*-
__author__ = 'blfeng'
__mail__ = 'wenyefbl@163.com'
__date__ = '2016-10-26'
__version = 1.0
from cm_cluster.get_clusters import GetCluster
from alert.alert_send import AlertSend
from printlog.debug import logdebug 
import os,re
import ConfigParser
#读取配置文件
cf = ConfigParser.ConfigParser()
cf.read(os.getcwd()+"/conf/cm_get.conf")
host = cf.get("cm","host")
port = int(cf.get("cm","port"))
username = cf.get("cm","username")
password = cf.get("cm","password")
no_alert_service =cf.get("alert","no_alert_service") 
alert_object_name =cf.get("alert","alert_object_name")
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
#conf = getcm.get_config(cluster_name=c_name,roles=roles)
#file = open ("conf.text","a+")
#for s in conf:
#    host_ipaddress = s['host_ipaddress']
#    service_name = s['service_name']
#    roles_name = s['roles_name']
#    config_key = s['config_key']
#    values = s['values']
#    message = "ip:"+host_ipaddress+"|service_name:"+service_name+"|roles_name:"+roles_name+"|config_key:"+config_key+"|values:"+values+"\n"
#    file.write(message)
#file.close()    

#各个service 的role状态
for service in cm_list:
    statues = getcm.check_status(cluster_name=c_name,appname=service)
    if len(statues):
        for service in statues:
           host_ip = service['host_ip']
           type = service['type']
           service_name = service['service_name']
           service_status = service['service_status']
           config_staleness_status = service['config_staleness_status']
           role_state =service ['role_state']
           if service_status != "GOOD" :
              if service_name in  no_alert_service:
                 pass
              else:
                 message = type+"'s "+service_name+",service status:"+service_status
                 log.loginfo(log_path,message)
                 #sendm.sendmessage(mc_object=alert_object_name,message=message,host_ip=host_ip,hostname=host_ip)
           if config_staleness_status != "FRESH":
              message = type+"'s "+service_name+",fresh status:"+config_staleness_status
              log.loginfo(log_path,message)
              #sendm.sendmessage(mc_object=alert_object_name,message=message,host_ip=host_ip,hostname=host_ip)
           if role_state != "STARTED":
              message = type+"'s "+service_name+",role state:"+role_state
              log.loginfo(log_path,message)
              #sendm.sendmessage(mc_object=alert_object_name,message=message,host_ip=host_ip,hostname=host_ip)

    else:
        pass
