#coding:utf-8
import os, sys, time, re
from subprocess import Popen, PIPE

ip_list = []
points = []

def trace_path(domain_str, need_seq):
   
    cmd_str = "tracert -d " + domain_str
    print("domain_str : %s, need_seq : %d"%(domain_str, need_seq))
    print("cmd_str : %s"%cmd_str)
    p = Popen(cmd_str, stdout=PIPE)
    regex_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')
    seq = 0
    target_ip = ""
    while True:
        one_line = p.stdout.readline()
        if not one_line:
           break
        #print("one_line:%s"%one_line)
        ip_extract = regex_ip.findall(one_line) #抽出每一hop中的ip list
        #print("ip_extract:%s"%ip_extract)
        if len(ip_extract) >= 1:
            if seq == 0:    #第一个ip为目的ip，非hop中的
                target_ip = ip_extract[0]
                seq += 1
                continue
            else: #第二个ip开始存入points列表中
                point = {}
                point['flag'] = 1
                point['seq'] = seq
                point['city'] = ""
                point['ip'] = ip_extract[0]                
                point['coord'] = []
                points.append(point)
                ip_list.append(ip_extract[0])
                print ("points%s"%points)
                print("IP: %s %s"%(ip_extract[0], one_line))
                seq += 1
    point = {}
    point['flag'] = 0
    points.append(point)    #trace结束
    print ("points%s"%points)
    print("ip_list:%s"%ip_list)
    print ("tracert %s end!"%domain_str)

if __name__ == '__main__':
    trace_path("61.135.169.121",1)

