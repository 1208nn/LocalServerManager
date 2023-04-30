import argparse
import os
import sqlite3
import subprocess
import psutil
import win32serviceutil
from pathlib import Path

# get arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", type=str)
parser.add_argument("-o", "--opreation", type=str)
# start/stop/server/kill/restart/check
parser.add_argument("-e", nargs=2, type=str)
# edit/add/delete
args = parser.parse_args()

# 获取当前用户的AppData目录路径
appdata_path = os.getenv("APPDATA")
# 拼接数据库文件路径
db_path = os.path.join(appdata_path, "SvcMgr", "services.db")
# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
# 创建一个游标对象
c = conn.cursor()


class service:
    def __init__(self, name, filename, filepath, args, webpageport, syssvc=False):
        self.name = name
        self.filename = filename
        self.filepath = filepath
        self.args = args
        self.webpageport = webpageport
        self.syssvc = syssvc

    def readdata(self):
        c.execute(f'SELECT * FROM {self.name}')

    def writedata(self):
        pass

    def runcommands(self, op):  # finished
        os.chdir(self.filepath)
        if op.lower() == "start":  # finished
            if self.syssvc:
                win32serviceutil.StartService(self.name)
                return
            # 启动命令行程序并将其作为后台进程运行
            proc = subprocess.Popen(
                [self.filename, self.args[0]],
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
                [self.filename, self.args[1]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        elif op.lower() == "server":  # finished
            proc = subprocess.Popen(
                [self.filename, self.args[2]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        elif op.lower() == "kill":  # finished
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
            # restart the win32 service
            win32serviceutil.RestartService(self.name)
            return
        return proc

    def checkrunning(self):  # finished
        # check whether the service is running
        if self.syssvc:
            return win32serviceutil.QueryServiceStatus(self.name)[1] == win32service.SERVICE_RUNNING

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

    '''
    def readoutput(self):
        pass
    '''


'''
# 创建一个表
c.execute(''CREATE TABLE IF NOT EXISTS stocks (date text, trans text, symbol text, qty real, price real)'')
# 插入一些数据
c.execute("INSERT INTO stocks VALUES ('2021-01-02','BUY','AAPL',100,135.0)")
c.execute("INSERT INTO stocks VALUES ('2021-01-05','SELL','AAPL',50,140.0)")
c.execute("INSERT INTO stocks VALUES ('2021-01-07','BUY','GOOG',200,240.0)")
# 保存更改
conn.commit()
# 查询数据
for row in c.execute('SELECT * FROM stocks ORDER BY price'):
    print(row)
# 关闭游标和连接
cursor.close()
conn.close()

file_path = Path(command).parent
os.chdir(file_path)
file_name =  Path(command).name


# 启动子进程并立即获取其输出和返回值
process = subprocess.Popen(['your_program.exe', 'arg1', 'arg2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
output, error = process.communicate()
# 打印子进程的输出和返回值
print(output)
print(process.returncode)
'''
