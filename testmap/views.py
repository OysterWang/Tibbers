#coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse


def home(request):
	str1 = "hehe"
	return render(request, 'index.html', {'string':str1})

def ajax_returnPoint(request):
	point = {'city': 'Beijing', 'coord': [108.54,34.16], 'seq': 1}
	return JsonResponse(point)
