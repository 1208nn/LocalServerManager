import tkinter as tk
import tkinter.ttk as ttk
import subprocess
from core.procpass import *


class App:
    def __init__(self, master):
        # 创建一个标签
        self.label = tk.Label(master, text="Services List")
        self.label.pack()

        # 获取List
        output = cli(['-o', 'search', '*'])

        # 创建一个列表框
        self.listbox = tk.Listbox(master)
        self.listbox.pack()

        # 把输出中的元素添加到列表框中
        for item in output:
            self.listbox.insert(tk.END, item)


# 创建一个窗口
root = tk.Tk()
# 设置窗口标题
root.title("Service Manager")
# 创建一个App实例
app = App(root)
# 进入事件循环
root.mainloop()
