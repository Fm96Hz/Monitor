import psutil
import sys
scale = 1.024E9

def getCPU():
    logicNum = psutil.cpu_count  #CPU逻辑个数
    physicalNum = psutil.cpu_count(logical=False)  #CPU物理核心
    Cpudict = {'logicNum': logicNum,
               'physicalNum': physicalNum}
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
    return Diskdict

"""
if __name__ == '__main__' :
    CoreLogicNum = getCPUCoreLogicNum()
    CPUCoreTrueNum = getCPUCoreTrueNum()
    diskPath = '/home'
    #while(1):
        #print(CoreLogicNum)
        #print(CPUCoreTrueNum)
    print(getMem())
        #print(getDisk(diskPath))
"""