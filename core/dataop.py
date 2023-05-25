import CurrOS
import json
import os
import sys
sys.path.append('..')
# 拼接JSON文件路径
json_file_path = os.path.join(CurrOS.appdata_path, "LocalSvcMgr", "Svcs.json")
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
