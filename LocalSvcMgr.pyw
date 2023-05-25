from tkinter import Tk, filedialog
from ttkbootstrap import Style, ttk, tk
import subprocess
import platform
from core.procpass import *

if platform.system() == 'Windows' and platform.release() >= '10':  # dark mode
    import winreg

    def is_dark_mode_enabled():
        try:
            value = not winreg.QueryValueEx(winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"), "AppsUseLightTheme")[0]
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
    popup.geometry("+%d+%d" % (root.winfo_x()+50, root.winfo_y()+50))
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
        # 创建一个列表框
        self.listbox = tk.Listbox(master)
        self.listbox.pack()
        # 把输出中的元素添加到列表框中
        for item in Svclist:
            self.listbox.insert(tk.END, item)


# 创建一个窗口
root = Tk()
# 设置窗口标题
root.title("Service Manager")
switcher = ThemeSwitcher()
switcher.start()

# 创建一个用于放置按钮和状态栏的框架
frame = tk.Frame(root, borderwidth=1)
frame.pack(side="bottom", fill="x")
# 创建一个状态栏
statusbar = tk.Label(frame, text="Running...")
statusbar.pack(side="left", fill="x")


def on_bar_option_selected(option):
    # 根据选择的选项执行相应的操作
    if option == "Add":
        print("选项1已选中。")
    elif option == "选项2":
        print("选项2已选中。")
    elif option == "选项3":
        print("选项3已选中。")


# 创建一个下拉式菜单
bar_options = ["Add", "选项2", "选项3"]
bar_selected_option = tk.StringVar()
bar_selected_option.set(bar_options[0])
bar_option_menu = tk.OptionMenu(
    frame, bar_selected_option, *bar_options, command=on_bar_option_selected)
bar_option_menu.pack(side="right")
bar_option_menu.configure(indicatoron=False)

# 创建一个按钮
button = tk.Button(frame, text="+", command=lambda: popupedit())
button.pack(side="right")


def open_file():
    # 打开文件对话框，并获取选择的文件路径
    file_path = filedialog.askopenfilename()
    # TODO: 执行打开文件操作


def save_file():
    # 打开文件对话框，并获取选择的文件路径
    file_path = filedialog.asksaveasfilename()
    # TODO: 执行保存文件操作


# 创建一个菜单栏
menubar = tk.Menu(root)
root.config(menu=menubar)
# 创建一个"文件"菜单
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
# 添加"打开文件"菜单项
file_menu.add_command(label="Open", command=open_file)
# 添加"保存文件"菜单项
file_menu.add_command(label="Save", command=save_file)


# 获取List
Svclist = cli(['-o', 'search', '*'])
if Svclist == []:
    ttk.Label(root, text="No Service").pack()
    button = ttk.Button(root, text='Add Service',
                        command=lambda: popupedit())
    button.pack()
    statusbar.config(text="No Service.")
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
