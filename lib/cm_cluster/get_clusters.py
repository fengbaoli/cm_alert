# -*- coding: utf-8 -*-
__author__ = 'blfeng'
__mail__ = 'wenyefbl@163.com'
__date__ = '2016-10-26'
__version = 1.0
import requests
import json
from cm_api.api_client import ApiResource
class GetCluster():
    def __init__(self,host,port,username,password):
        self.username = username
        self.host = host
        self.port = port
        self.password = password
    def cluster(self):
        baseurl= "http://%s:%s/api/v12/clusters" %(self.host,self.port)
        r = requests.get(baseurl, auth=(self.username, self.password))
        json_output= json.loads(r.content)
        for s in json_output['items']:
            cluster_name = s['displayName']
        return  cluster_name
    def get_config(self,cluster_name,roles):
        self.cluster_name = cluster_name
        self.roles = roles
        config_list = []
        for roles_dic in roles:
            service_name = roles_dic['service_name']
            roles_name = roles_dic['role_name']
            host_ipaddress = roles_dic['host_ipaddress']
            baseurl ="http://%s:%s/api/v12/clusters/%s/services/%s/roles/%s/config?view=full" %(self.host,self.port,self.cluster_name,service_name,roles_name)
            r = requests.get(baseurl, auth=(self.username, self.password))
            json_output= json.loads(r.content)
            for s in json_output['items']:
                config_dic={}
                if s.has_key('value'):
                    config_key = str(s['name'])
                    values = str(s['value'])
                elif s.has_key('default'):
                    config_key = str(s['name'])
                    values = str(s['default'])
                else:
                    pass
                config_dic['host_ipaddress'] = host_ipaddress
                config_dic['service_name'] = service_name
                config_dic['roles_name'] = roles_name
                config_dic['config_key'] = config_key
                config_dic['values'] = values
                config_list.append(config_dic)
        return  config_list
    def get_hosts(self):
        hosts = {}
        from cm_api.api_client import ApiResource
        api = ApiResource(self.host, self.port, self.username, self.password)
        for h in api.get_all_hosts():
            hosts[h.hostId] = h.ipAddress
        return  hosts
    def get_roles(self,cluster_name,services):
        self.cluster_name = cluster_name
        self.services = services
        roles_list=[]
        for service in self.services:
            baseurl ="http://%s:%s/api/v12/clusters/%s/services/%s/roles" % (self.host,self.port,self.cluster_name,service)
            r = requests.get(baseurl, auth=(self.username, self.password))
            json_output= json.loads(r.content)
            for s in (json_output['items']):
                role_name_dic={}
                get_cm = GetCluster(host=self.host,port = self.port ,username = self.username,password = self.password)
                host_dic = get_cm.get_hosts()
                hostid = str(s['hostRef']['hostId'])
                role_name_dic['host_ipaddress']= str(host_dic[hostid])
                role_name_dic['service_name'] = str(s['serviceRef']['serviceName'])
                role_name_dic['role_name'] = str(s['name'])
                roles_list.append(role_name_dic)
        return   roles_list
    def services(self):
        api = ApiResource(self.host, username=self.username, password=self.password)
        version = None
        service_list = []
        for cluster in api.get_all_clusters():
          if cluster.version == "CDH5":
             version = cluster
        for service in version.get_all_services():
          service_list.append(service.name)
        return  service_list
    def check_status(self,cluster_name,appname):
        message_list = []
        self.cluster_name = cluster_name
        self.appname = appname
        get_cm = GetCluster(host=self.host,port = self.port ,username = self.username,password = self.password)
        hosts = get_cm.get_hosts()
        baseurl =  "http://%s:%s/api/v12/clusters/%s/services/%s/roles" %(self.host,self.port,self.cluster_name,self.appname)
        r1 = requests.get(baseurl, auth=(self.username, self.password))
        json_output1= json.loads(r1.content)
        service_check_list =[]
        for s in json_output1['items']:
            host_ip = hosts[s['hostRef']['hostId']]
            config_staleness_status = s['configStalenessStatus']
            type = s['type']
            health_summary = s['healthSummary']
            role_state = s['roleState']
            entity_status = s['entityStatus']
            health_checks =s['healthChecks']
            for status  in health_checks:
                service_check ={}
                service_name = status['name']
                service_status = status['summary']
                service_check['host_ip'] = host_ip
                service_check['config_staleness_status'] = config_staleness_status
                service_check['type'] = type
                service_check['health_summary'] = health_summary
                service_check['role_state'] = role_state
                service_check['entity_status'] = entity_status
                service_check['service_name'] = service_name
                service_check['service_status'] = service_status
                service_check_list.append(service_check)
        return  service_check_list
