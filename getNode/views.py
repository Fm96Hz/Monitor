from django.shortcuts import render
from django.http import HttpResponse
from . import NodeInfo
# Create your views here.

def getNodeInfo(request):
    cpuContext = NodeInfo.getCPU()
    memContext = NodeInfo.getMem()
    diskContext = NodeInfo.getDisk("/")
    context = dict(cpuContext,**memContext)
    context = dict(context,**diskContext)
    return render(request,'getNode/NodeInfo.html',context)
