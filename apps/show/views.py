#coding:utf-8
from django.shortcuts import render
from django.http.response import JsonResponse
import socket

#引用例子：points[0]['city']，seq=1为第一跳
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

#request是必须的
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
	point = points[need_seq - 1]
	print ("\npoint:%s" %point)
	return JsonResponse(point)