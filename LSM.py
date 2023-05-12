import argparse
from core.svcm import *
from core.procpass import *


# get arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", type=str)
parser.add_argument("-o", "--opreation", choices=[
                    "start", "stop", "server", "kill", "restart", "check", "search"], type=str)
# start/stop/server/kill/restart/check/search
parser.add_argument("-e", nargs=2, type=str)
# edit/add/del
args = parser.parse_args()


tasksvc = service(args.name)
if args.opreation:
    tasksvc.runcommands(args.opreation)
elif args.e:
    if args.e[0] == "edit":
        pass
    elif args.e[0] == "add":
        pass
    elif args.e[0] == "del":
        pass
    tasksvc.writedata()
else:
    print("no operation")
