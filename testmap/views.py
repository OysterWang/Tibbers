#coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse
import socket

#引用例子：points[0]['city']，seq=1为第一跳
points = [{
"seq"  : 1,
"city" : "Xian",
"ip"   : "1.1.1.1",
"coord": [108.54,34.16]
},{
"seq"  : 2,
"city" : "Taiwan",
"ip"   : "2.2.2.2",
"coord": [121.491121,25.127053]
}]

def index(request):
	host_name = socket.getfqdn(socket.gethostname())	#获取服务器名称
	host_local_ip = socket.gethostbyname(host_name)	#获取服务器ip
	host_internet_ip = "202.106.57.170"	#获取服务器Internet ip
	host_coordinate_lng = 116.432045
	host_coordinate_lat = 39.910683
	return render(request, "index.html", 
		{"host_name":host_name,
		"host_local_ip":host_local_ip,
		"host_internet_ip":host_internet_ip,
		"host_coordinate_lng":host_coordinate_lng,
		"host_coordinate_lat":host_coordinate_lat})

def ajax_returnPoint(request):
	ip_des = request.GET["ip_des"]
	print ("ip_des: %s" %ip_des)
	point = points[1]	#{'city': 'Beijing', 'coord': [108.54, 34.16], 'seq': 1}
	print ("#######\npoint:%s" %point)
	return JsonResponse(point)

