#coding:utf-8
from django.shortcuts import render

import utils.detect

def index(request):
    results = utils.detect.getResults()	#detect模块得到ping的结果
    return render(request, "alive.html", {"results_content":results})

    