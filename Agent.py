"""部署在Node节点上"""

import time

import psutil
import sys
import socket
import json
import threading
scale = 1.024E9

"---------获取节点信息---------"
def getCPU():
    logicNum = psutil.cpu_count()  #CPU逻辑个数
    physicalNum = psutil.cpu_count(logical=False)  #CPU物理核心
    Cpudict = {'logicNum': logicNum,
               'physicalNum': physicalNum}
    #Cpudict = json.dumps(Cpudict, ensure_ascii=False).encode("utf-8")
    return Cpudict

def getMem():
    Memtotal = psutil.virtual_memory().total / scale
    Memavailable = psutil.virtual_memory().available / scale
    Memused = psutil.virtual_memory().used / scale
    Mempercent = psutil.virtual_memory().percent
    Memdict = {'Memtotal': format(Memtotal,'.2f')+'G',
               'Memavailable': format(Memavailable,'.2f')+'G',
               'Memused': format(Memused,'.2f')+'G',
               'Mempercent': str(Mempercent)+'%'}
    #Memdict = json.dumps(Memdict, ensure_ascii=False).encode("utf-8")
    return Memdict

def getMemSwap():
    return psutil.swap_memory().available / scale

def getDisk(Path):
    Disktotal = psutil.disk_usage(Path).total / scale
    Diskused = psutil.disk_usage(Path).used / scale
    Diskfree = psutil.disk_usage(Path).free / scale
    Diskpercent = psutil.disk_usage(Path).percent
    Diskdict = {'Disktotal': format(Disktotal,'.2f')+'G',
               'Diskfree': format(Diskfree,'.2f')+'G',
               'Diskused': format(Diskused,'.2f')+'G',
               'Diskpercent': str(Diskpercent)+'%'}
    #Diskdict = json.dumps(Diskdict, ensure_ascii=False).encode("utf-8")
    return Diskdict

"---------socket通信-----------"
def handle_client_request(service_client_socket,ip_port):  #建立连接后的新套接字，负责收发数据
    #循环接收客户端发送的数据
    while True:
        #接收客户端发送的数据
        recv_data = service_client_socket.recv(1024)
        #容器类型数据：列表、字典、元组、字符串、range、二进制数据等等
        #判断客户端是否在发送数据
        if recv_data.decode("utf-8") == "Request NodeInfo":
            #如果收到数据，打印收到的数据内容，以及来源
            print(recv_data.decode("utf-8"),ip_port)
            #回复客户端
            service_client_socket.send(json.dumps(NodeInfo, ensure_ascii=False).encode("utf-8"))
        else:
            #客户端发送数据长度为0，客户端不再发送数据，判断客户端下线
            print("Shutdown!：", ip_port)
            break
    #关闭收发数据套接字
    service_client_socket.close()

if __name__ == '__main__' :
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定地址，并开始监听，开始监听后，tcp_server_socket变为被动套接字，只接受客户端连接请求
    tcp_server_socket.bind(("", 9000))
    tcp_server_socket.listen(10)

    while True:
        service_client_socket,ip_port = tcp_server_socket.accept()
        Cpudict = getCPU()
        Memdict = getMem()
        Diskdict = getDisk("/")
        NodeInfo = dict(Cpudict, **Memdict)
        NodeInfo = dict(NodeInfo,**Diskdict)
        sub_thread = threading.Thread(target=handle_client_request, args=(service_client_socket, ip_port))
        sub_thread.setDaemon(True)
        sub_thread.start()