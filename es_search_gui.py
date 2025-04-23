import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import threading
import subprocess
import sys
# 使用新的 API 函数
from es_api import search

# 检查 Everything 是否正在运行
def is_everything_running():
    """检查 Everything 程序是否在运行"""
    try:
        # 使用 tasklist 命令检查是否有 Everything 进程
        result = subprocess.run(
            "tasklist /FI \"IMAGENAME eq Everything.exe\" /NH", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        return "Everything.exe" in result.stdout
    except:
        return False

# 无界面启动 Everything 服务
def start_everything_service():
    """尝试启动 Everything 服务，不显示 GUI"""
    try:
        # 首先尝试启动 Everything 服务
        subprocess.run(
            "sc start Everything", 
            shell=True, 
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    except:
        # 如果服务启动失败，尝试寻找 Everything.exe
        try:
            potential_paths = [
                r"C:\Program Files\Everything\Everything.exe",
                r"C:\Program Files (x86)\Everything\Everything.exe",
            ]
            
            for path in potential_paths:
                if os.path.exists(path):
                    # 使用静默模式启动
                    subprocess.Popen(
                        [path, "-startup", "-minimized", "-silent"], 
                        shell=False,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    import time
                    time.sleep(2)
                    return True
            return False
        except:
            return False

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Everything 搜索工具")
        self.root.geometry("800x600")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 搜索字符串区域
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="搜索字符串:").pack(side=tk.LEFT, padx=5)
        self.search_text = ttk.Entry(search_frame, width=50)
        self.search_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 搜索文件夹区域
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="搜索文件夹:").pack(side=tk.LEFT, padx=5)
        self.folder_path = ttk.Entry(folder_frame, width=50)
        self.folder_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(folder_frame, text="浏览...", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
        
        # 搜索按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.search_button = ttk.Button(button_frame, text="搜索", command=self.perform_search)
        self.search_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_label = ttk.Label(button_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=100, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=5)
        
        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="搜索结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建结果显示区域（带滚动条）
        self.result_area = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=80, height=20)
        self.result_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 启动时检查 Everything 是否运行
        self.check_everything_status()
        
    def check_everything_status(self):
        """检查 Everything 程序状态"""
        if not is_everything_running():
            answer = messagebox.askyesno("Everything 未运行", 
                                        "检测到 Everything 程序未运行，需要启动 Everything 服务才能进行搜索。\n\n是否尝试自动启动？")
            if answer:
                self.status_var.set("正在启动 Everything 服务...")
                self.root.update()
                if start_everything_service():
                    self.status_var.set("Everything 服务已启动，就绪")
                else:
                    self.status_var.set("无法自动启动 Everything，请手动启动")
            else:
                self.status_var.set("Everything 未运行，部分功能可能受限")
        else:
            self.status_var.set("就绪 (Everything 已运行)")
        
    def browse_folder(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.delete(0, tk.END)
            self.folder_path.insert(0, folder_selected)
    
    def perform_search(self):
        """执行搜索操作"""
        search_text = self.search_text.get().strip()
        folder_path = self.folder_path.get().strip()
        
        if not search_text:
            messagebox.showwarning("输入错误", "搜索字符串不能为空")
            return
        
        # 禁用搜索按钮，防止重复点击
        self.search_button.configure(state="disabled")
        
        # 清除之前的结果
        self.result_area.delete(1.0, tk.END)
        
        # 更新状态并显示进度条
        self.status_var.set("正在搜索...")
        self.progress.start()
        self.root.update()
        
        # 在单独的线程中执行搜索，避免界面冻结
        threading.Thread(target=self._search_thread, args=(search_text, folder_path)).start()
    
    def _search_thread(self, search_text, folder_path):
        """在单独的线程中执行搜索"""
        try:
            # 使用新的 search 函数执行搜索
            if folder_path:
                results = search(search_text, folder_path)
            else:
                results = search(search_text)
            
            # 使用主线程更新 UI
            self.root.after(0, lambda: self._update_results(results))
        except Exception as e:
            # 使用主线程显示错误
            self.root.after(0, lambda: self._show_error(str(e)))
    
    def _update_results(self, results):
        """更新搜索结果 UI"""
        # 停止进度条
        self.progress.stop()
        
        # 显示结果
        if results:
            self.result_area.insert(tk.END, f"找到 {len(results)} 个结果:\n\n")
            for i, result in enumerate(results, 1):
                self.result_area.insert(tk.END, f"{i}. {result}\n")
            self.status_var.set(f"搜索完成，找到 {len(results)} 个结果")
        else:
            self.result_area.insert(tk.END, "未找到任何结果。")
            self.status_var.set("搜索完成，未找到结果")
        
        # 重新启用搜索按钮
        self.search_button.configure(state="normal")
    
    def _show_error(self, error_message):
        """显示错误消息"""
        # 停止进度条
        self.progress.stop()
        
        # 显示错误
        messagebox.showerror("搜索错误", f"搜索过程中发生错误:\n{error_message}")
        self.status_var.set("搜索失败")
        
        # 重新启用搜索按钮
        self.search_button.configure(state="normal")
    
    def clear_fields(self):
        """清除输入字段和结果区域"""
        self.search_text.delete(0, tk.END)
        self.folder_path.delete(0, tk.END)
        self.result_area.delete(1.0, tk.END)
        self.status_var.set("就绪")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop() 