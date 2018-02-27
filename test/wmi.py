import wmi
from win32com.client import GetObject
import win32gui, time

mywmi = GetObject("winmgmts:")
# allProcess = mywmi.ExecQuery("select * from Win32_Process")
# for i in allProcess:
#     pid = i.Properties_("ProcessID")
#     print pid

# network = mywmi.ExecQuery("select Processor, _Total, Processor Time from PerformanceCounter")
# print network
# for i in network:
#     print i.Properties_("Processor")

mywql = mywmi.ExecQuery("SELECT * FROM Win32_PerfFormattedData_PerfProc_Process where PercentPrivilegedTime>10")


def getPrcessInfo(wql):
    while 1:

        for j in wql:
            # print j.Properties_("PercentPrivilegedTime").__int__()
            ##print j.Properties_("name").__str__()+" "+j.Properties_("IDProcess").__str__()+"  "+j.Properties_("PercentPrivilegedTime").__str__()
            if j.Properties_("name").__str__() != "_Total" and j.Properties_("name").__str__() != "Idle":
                print
                j.Properties_("name")
                print
                j.Properties_("PercentPrivilegedTime").__int__()
                print
                j.Properties_("WorkingSet").__int__()
                time.sleep(1)
                # return 1
                # break

                ##print ":)"


getProcessInfo(mysql)