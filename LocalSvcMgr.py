import tkinter as tk
import tkinter.ttk as ttk
import subprocess
from core.procpass import *
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)


class App:
    def __init__(self, master):
        # 创建一个标签
        self.label = tk.Label(master, text="Services List")
        self.label.pack()
        # 创建一个Notebook小部件
        notebook = ttk.Notebook(master, style='TNotebook')
        # 把输出中的元素添加到列表框中
        for item in Svclist:
            self.listbox.insert(tk.END, item)
            tab1 = ttk.Frame(notebook)
            # 将选项卡添加到Notebook中
            notebook.add(tab1, text=item)
            # 在选项卡中添加小部件
            label1 = tk.Label(tab1, text=item)
        label1.pack(padx=20, pady=20)
        # 显示Notebook小部件
        notebook.pack()


# 创建一个窗口
root = tk.Tk()
# 设置窗口标题
root.title("Service Manager")
# 获取List
Svclist = cli(['-o', 'search', '*'])
if Svclist == []:
    tk.Label(root, text="No Service").pack()
    root.mainloop()
    exit()
# 创建一个样式
style = ttk.Style()
# 设置选项卡在左侧
style.configure('TNotebook', tabposition='wn')
# 设置选项卡宽度
style.configure('TNotebook.Tab', width=8)
# 设置选项卡高度
style.configure('TNotebook.Tab', height=3)
# 创建一个App实例
app = App(root)
# 进入事件循环
root.mainloop()
