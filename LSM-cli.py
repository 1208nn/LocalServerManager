import argparse
import os
import json
import subprocess
import psutil
import win32serviceutil
from pathlib import Path


# get arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", type=str)
parser.add_argument("-o", "--opreation", type=str)
# start/stop/server/kill/restart/check/list
parser.add_argument("-e", nargs=2, type=str)
# edit/add/del
args = parser.parse_args()


# 获取%appdata%目录路径
appdata_path = os.getenv("APPDATA")
# 拼接JSON文件路径
json_file_path = os.path.join(appdata_path, "LocalSvcMgr", "Svcs.json")
if not os.path.exists(json_file_path):
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, 'w') as f:
        json.dump({}, f)
# 打开JSON文件并读取数据
with open(json_file_path, "r") as f:
    SvcData = json.load(f)


def saveSvcData():
    with open(json_file_path, "w") as f:
        json.dump(SvcData, f)


class service:
    def __init__(self, name, filename, filepath, args, webpageport, syssvc=False):
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
        os.chdir(self.filepath)
        if op.lower() == "start":  # finished
            if self.syssvc:
                win32serviceutil.StartService(self.name)
                return
            # 启动命令行程序并将其作为后台进程运行
            proc = subprocess.Popen(
                [self.filename, self.args['start']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        elif op.lower() == "stop":  # finished
            if self.syssvc:
                win32serviceutil.StopService(self.name)
                return
            proc = subprocess.Popen(
                [self.filename, self.args['stop']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        elif op.lower() == "server":  # finished
            if self.syssvc:
                return
            proc = subprocess.Popen(
                [self.filename, self.args['server']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        elif op.lower() == "kill":  # finished
            if self.syssvc:
                return
            # 获取所有正在运行的进程
            for proc in psutil.process_iter():
                try:
                    # 获取进程的名称和路径
                    process_name = proc.name()
                    process_path = proc.exe()

                    # 如果进程的名称为"filename"，且路径为"filepath"，则终止该进程
                    if process_name == self.filename and process_path == self.filepath:
                        proc.kill()
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    pass
            return
        elif op.lower() == "check":  # finished
            return checkrunning()
        elif op.lower() == "restart":  # finished
            if not self.syssvc:
                return
            # restart the win32 service
            win32serviceutil.RestartService(self.name)
            return
        return proc

    def checkrunning(self):  # finished
        # Check whether the service is running.
        if self.syssvc:
            return (
                win32serviceutil.QueryServiceStatus(self.name)[1]
                == win32service.SERVICE_RUNNING
            )

        for proc in psutil.process_iter():
            try:
                # 获取进程的名称和路径
                process_name = proc.name()
                process_path = proc.exe()

                if process_name == self.filename and process_path == self.filepath:
                    return True
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                pass
        return False

    """
    def readoutput(self):
        pass
    """


tasksvc = service(args.name)
if args.opreation:
    tasksvc.readdata()
    tasksvc.runcommands(args.opreation)
if ergs.e:
    if args.e[0] == "edit":
        pass
    elif args.e[0] == "add":
        pass
    elif args.e[0] == "del":
        pass
    tasksvc.writedata()


"""
# 启动子进程并立即获取其输出和返回值
process = subprocess.Popen(['your_program.exe', 'arg1', 'arg2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
output, error = process.communicate()
# 打印子进程的输出和返回值
print(output)
print(process.returncode)
"""
