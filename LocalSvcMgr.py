from tkinter import Tk
from ttkbootstrap import Style, ttk, tk
import subprocess
import platform
from core.procpass import *

if platform.system() == 'Windows' and platform.release() >= '10':# dark mode
    import winreg

    def is_dark_mode_enabled():
        try:
            value = not winreg.QueryValueEx(winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"), "AppsUseLightTheme")[0]
        except:
            value = False
        return value

    class ThemeSwitcher:
        def __init__(self, style_name='minty'):
            self.style = Style(theme=style_name)
            self.current_value = None

        def switch_theme(self):
            value = is_dark_mode_enabled()
            if value != self.current_value:
                self.current_value = value
                theme_name = 'cyborg' if value else 'minty'
                self.style.theme_use(theme_name)
            # Call this method again after 100ms
            root.after(100, self.switch_theme)

        def start(self):
            # Start the theme switcher
            self.switch_theme()

if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)


# 定义一个关闭弹出窗口的函数
def close_popup(popup_object):
    popup_object.grab_release()
    popup_object.destroy()


def popupedit():
    popup = tk.Toplevel(root)
    popup.title('Edit')
    popup.geometry('200x100')
    popup.grab_set()
    # 在弹出窗口中添加一些小部件
    label = tk.Label(popup, text='Edit.')
    label.pack()
    # 在弹出窗口中添加一个“确定”按钮
    ok_button = ttk.Button(
        popup, text='OK', command=lambda: close_popup(popup))
    ok_button.pack()


class svcui:
    def __init__(self):
        pass


class App:
    def __init__(self, master):
        # 创建一个标签
        self.label = tk.Label(master, text="Services List")
        self.label.pack()
        # 创建一个Notebook小部件
        notebook = ttk.Notebook(master, style='TNotebook')
        # 把输出中的元素添加到列表框中
        for item in Svclist:
            tab1 = ttk.Frame(notebook)
            # 将选项卡添加到Notebook中
            notebook.add(tab1, text=item)
            # 在选项卡中添加小部件
            label1 = tk.Label(tab1, text=item)
        label1.pack(padx=20, pady=20)
        # 在标签页小部件上创建一个Canvas部件
        canvas = tk.Canvas(notebook)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 创建一个Scrollbar部件并将其附加到Canvas部件上
        scrollbar = ttk.Scrollbar(
            notebook, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        # 在Canvas部件上创建一个Frame部件以包含您的内容小部件
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')
        # 创建您的内容小部件并将其添加到Frame部件中
        label = tk.Label(
            frame, text='This is a long label that requires scrolling.')
        label.pack()
        # 更新Canvas部件以确保其适合内容大小
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))
        # 将标签页小部件添加到Tkinter窗口中
        notebook.add(canvas, text='Tab with scrollbar')
        # 显示Notebook小部件
        notebook.pack()


# 创建一个窗口
root = Tk()
# 设置窗口标题
root.title("Service Manager")
switcher = ThemeSwitcher()
switcher.start()

'''
# 使窗口没有默认的标题栏
root.overrideredirect(True)
# 创建一个包含标题栏的框架
title_bar = tk.Frame(root, bg="red", relief="raised", bd=0)
# 创建一个标签，用于显示窗口的标题
title_label = tk.Label(title_bar, text="Service Manager", bg="red", fg="white")
# 将标签放置在标题栏中
title_label.pack(side="left", padx=5)
# 将标题栏放置在窗口中
title_bar.pack(expand=1, fill="x")
# 创建一个用于关闭窗口的按钮
close_button = tk.Button(title_bar, text="×", bg="red", fg="white", command=root.destroy)
# 将按钮放置在标题栏中
close_button.pack(side="right", padx=5)
'''

# 获取List
Svclist = cli(['-o', 'search', '*'])
if Svclist == []:
    ttk.Label(root, text="No Service").pack()
    button = ttk.Button(root, text='Add Service',
                        command=lambda: popupedit())
    button.pack()
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
