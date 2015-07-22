#coding:utf-8
import urllib,re
import os,sys
import time

'''
E:\CloudSync\LITB_NETWORK_SYNC\Python_Projects\Tibbers\utils>tracert -d www.baidu.com

通过最多 30 个跃点跟踪
到 www.a.shifen.com [61.135.169.121] 的路由:

  1    <1 毫秒    2 ms     1 ms  192.168.4.129
  2    <1 毫秒   <1 毫秒   <1 毫秒 192.168.11.30
  3     2 ms     2 ms     2 ms  202.106.57.169
  4     1 ms     3 ms     2 ms  61.148.155.77
  5     5 ms     3 ms     3 ms  61.148.146.29
  6     3 ms     2 ms     2 ms  124.65.58.174
  7     2 ms     3 ms     4 ms  123.125.248.90
  8     *        *        *     请求超时。
  9     2 ms     1 ms     1 ms  61.135.169.121

跟踪完成。

E:\CloudSync\LITB_NETWORK_SYNC\Python_Projects\Tibbers\utils>

points = [{
"flag" : 1,
"seq"  : 1,
"city" : "tianjin",
"ip"   : "1.1.1.1",
"coord": [117.20000,39.13333]
},{
"flag" : 1,
"seq"  : 2,
"city" : "shanghai",
"ip"   : "2.2.2.2",
"coord": [121.48,31.22]
},{
"flag" : 0
}]
'''
def get_tracert(domain):
    ip_list = []
    data = os.popen('tracert -d %s ' % domain).readlines()
    b = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')
    data = [  b.findall(x) for x in data ]
    for x in data:
        if x != []:
            ip_list.append(''.join(x))
    return ip_list

from subprocess import Popen, PIPE
def tracert_2(domain_str):
    ip_list = []
    point = {}
    #point['flag'] = 1
    points = []
    cmd_str = "tracert -d " + domain_str
    p = Popen(cmd_str, stdout=PIPE)
    regex_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')
    seq = 1
    while True:
        line = p.stdout.readline()
        ip_extract = regex_ip.findall(line)
        if len(ip_extract) >= 1:
            ip_list.append(ip_extract[0])
            print("IP: %s %s"%(ip_extract[0], line))
            seq += 1
        if not line:
            break
    print("ip_list:%s"%ip_list)
    print ("tracert end!")

import sys
from subprocess import Popen
def tracert_3():
    if len(sys.argv) < 2:
        print ' '
        sys.exit(1)
    cmd_line = sys.argv[1:]
    p1 = Popen("tracert -d 192.168.12.8")
    p2 = Popen("tracert -d www.baidu.com")
    time.sleep(1)
    #p.terminate()
    print("p1.pid:%s,p2.pid:%s" %(p1.pid,p2.pid))
    for i in range(100):
        print(i)
    p1.communicate()[0]

if __name__ == '__main__':
    tracert_2("61.135.169.121")

