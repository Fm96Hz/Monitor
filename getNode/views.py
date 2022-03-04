from django.shortcuts import render
from django.http import HttpResponse
from . import NodeInfo
import asyncio
import websockets
# Create your views here.


def getNodeInfo(request):
    context = NodeInfo.message()
    return render(request,'getNode/NodeInfo.html',context)


