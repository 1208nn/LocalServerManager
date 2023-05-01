import win32serviceutil
import fnmatch
from core.procpass import *
from core.dataop import *


class service:
    def __init__(self, name, filename=None, filepath=None, args=None, webpageport=None, syssvc=False):
        self.name = name
        self.filename = filename
        self.filepath = filepath
        self.args = args
        self.webpageport = webpageport
        self.syssvc = syssvc

    def readdata(self):
        self.args = SvcData[self.name]["args"]
        self.webpageport = SvcData[self.name]["webpageport"]
        self.filename = SvcData[self.name]["filename"]
        self.filepath = SvcData[self.name]["filepath"]
        self.syssvc = SvcData[self.name]["syssvc"]

    def writedata(self):
        SvcData[self.name]["args"] = self.args
        SvcData[self.name]["webpageport"] = self.webpageport
        SvcData[self.name]["filename"] = self.filename
        SvcData[self.name]["filepath"] = self.filepath
        SvcData[self.name]["syssvc"] = self.syssvc
        saveSvcData()

    def runcommands(self, op):  # finished
        if self.filepath:
            os.chdir(self.filepath)
        if op.lower() == "start":  # finished
            if self.syssvc:
                win32serviceutil.StartService(self.name)
                return
            # 启动命令行程序并将其作为后台进程运行
            proc = proccreate([self.filename, self.args['start']])
        elif op.lower() == "stop":  # finished
            if self.syssvc:
                win32serviceutil.StopService(self.name)
                return
            proc = proccreate(
                [self.filename, self.args['stop']]
            )
        elif op.lower() == "server":  # finished
            if self.syssvc:
                return
            proc = proccreate(
                [self.filename, self.args['server']]
            )
        elif op.lower() == "kill":  # finished
            if self.syssvc:
                return
            prockill(self.filename, self.filepath)

        elif op.lower() == "check":  # finished
            return checkrunning()
        elif op.lower() == "restart":  # finished
            if not self.syssvc:
                return
            # restart the win32 service
            win32serviceutil.RestartService(self.name)
            return
        elif op.lower() == "search":
            print(fnmatch.filter(SvcData.keys(), self.name)
                  if '*' in self.name else [name for name in SvcData.keys() if self.name in name])
            exit()
        else:
            return
        return proc

    def checkrunning(self):  # finished
        return proccheck(name=self.name, syssvc=self.syssvc, fname=self.filename, fpath=self.filepath)

    """
    def readoutput(self):
        pass
    """
