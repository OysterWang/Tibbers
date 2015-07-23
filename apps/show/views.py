#coding:utf-8
from django.shortcuts import render
from django.http.response import JsonResponse
import socket

#引入trace
#from utils import getpoints
import os, sys, time, re
from subprocess import Popen, PIPE
from multiprocessing import Process
#引入trace
ip_list = []
points = []

#引用例子：points[0]['city']，seq=1为第一跳
points_example = [{
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
"flag" : 1,
"seq"  : 3,
"city" : "guangzhou",
"ip"   : "3.3.3.3",
"coord": [113.23333,23.16667]
},{
"flag" : 1,
"seq"  : 4,
"city" : "hongkong",
"ip"   : "4.4.4.4",
"coord": [114.10000,22.20000]
},{
"flag" : 1,
"seq"  : 5,
"city" : "taiwan",
"ip"   : "5.5.5.5",
"coord": [121.491121,25.127053]
},{
"flag" : 0
}]


#引入trace
def trace_path(domain_str, need_seq, points):
	cmd_str = "tracert -d " + domain_str
	print("domain_str : %s, need_seq : %d"%(domain_str, need_seq))
	print("cmd_str : %s"%cmd_str)
	p = Popen(cmd_str, stdout=PIPE)
	regex_ip = re.compile(b'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3}')
	seq = 0
	target_ip = ""
	while True:
		one_line = p.stdout.readline()

		if not one_line:
		   break
		#print("one_line:\n%s"%one_line)
		ip_extract = regex_ip.findall(one_line) #抽出每一hop中的ip list
		#print("ip_extract:%s"%ip_extract)
		if len(ip_extract) >= 1:
			if seq == 0:	#第一个ip为目的ip，非hop中的
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
				#print ("points%s"%points)
				print("IP: %s %s"%(ip_extract[0], one_line))
				seq += 1
	point = {}
	point['flag'] = 0
	points.append(point)	#trace结束
	print ("points%s"%points)
	print("I know you need points[%d]:%s"%((need_seq-1), points[need_seq-1]))
	print("ip_list:%s"%ip_list)
	print ("tracert %s end!"%domain_str)

#request是必须的。
def trace(request):
	host_name = socket.getfqdn(socket.gethostname())	#获取服务器名称
	host_local_ip = socket.gethostbyname(host_name)	#获取服务器ip
	host_internet_ip = "202.106.57.170"	#获取服务器Internet ip
	host_coordinate_lng = 116.432045
	host_coordinate_lat = 39.910683
	host_city = "Beijing"

	point_start={"seq":0, 
	"city":host_city, 
	"host_local_ip":host_local_ip,
	"host_internet_ip":host_internet_ip, 
	"host_coordinate_lng":host_coordinate_lng,
	"host_coordinate_lat":host_coordinate_lat,
	"host_name":host_name
	}

	return render(request, "trace.html", {"point_start":point_start})

def ajax_returnPoint(request):
	ip_des = request.GET["ip_des"]
	need_seq = int(request.GET["need_seq"])
	print("*******************************************************")
	print ("ip_des: %s, need_seq: %s" %(ip_des,need_seq))
	
	#开始trace进程

	if need_seq == 1:
		p1 = Process(target=trace_path, args=(ip_des, need_seq, points))
		p1.start()
		#p1.join()

	#trace_path(ip_des, need_seq)	#61.135.169.121

	while True:
		try:
			print("############## loop for searching points[%d]" %(need_seq - 1))
			if points[need_seq - 1]:
				print("################   searching points[%d]" %(need_seq - 1))
				print("####################### found!!! %d:%s"%(need_seq, points[need_seq - 1]))
				break
		except Exception as ex:
			print("exception:%s"%ex)
			print("need_seq %d not got yet!"%need_seq)
			time.sleep(0.5)
	
	point = points[need_seq - 1]
	print ("\nreturn point:%s" %point)
	return JsonResponse(point)



