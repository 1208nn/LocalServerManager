import subprocess
import psutil
import os
import sys
import ast
import win32service


def proccheck(name, syssvc=False, fname=None, fpath=None):
    # Check whether the service is running.
    if syssvc and os.name == "nt":
        import win32serviceutil

        return (
            win32serviceutil.QueryServiceStatus(name)[1] == win32service.SERVICE_RUNNING
        )
    for proc in psutil.process_iter():
        try:
            # 获取进程的名称和路径
            process_name = proc.name()
            process_path = proc.exe()

            if process_name == fname and process_path == fpath:
                return True
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass
    return False


def prockill(name, path):
    # 获取所有正在运行的进程
    for proc in psutil.process_iter():
        try:
            # 获取进程的名称和路径
            process_name = proc.name()
            process_path = proc.exe()
            # 如果进程的名称为"filename"，且路径为"filepath"，则终止该进程
            if process_name == name and process_path == path:
                proc.kill()
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass
    return


def proccreate(args):
    return subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=False,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def cli(args):
    if hasattr(sys, "_MEIPASS"):
        os.chdir(os.path.dirname(sys.executable))
        cliapp = ["LSM.exe"]
    else:
        # 切换到procpass.py上级目录
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cliapp = ["python", "LSM.py"]
    output = (
        subprocess.run(cliapp + args, stdout=subprocess.PIPE).stdout.decode().strip()
    )
    try:
        ast.parse(output)
        return ast.literal_eval(output)
    except SyntaxError:
        return output
