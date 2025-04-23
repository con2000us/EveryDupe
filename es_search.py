import subprocess
import os
import sys
import ctypes

def is_everything_running():
    """
    检查 Everything 程序是否在运行
    
    返回:
        bool: 如果 Everything 在运行，则返回 True，否则返回 False
    """
    try:
        # 使用 Windows API 检查进程名称
        if sys.platform == 'win32':
            # 导入 Windows API
            import psutil
            # 检查进程名称
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'everything' in proc.info['name'].lower():
                    return True
        return False
    except:
        # 如果检查失败，我们假设 Everything 没有运行
        return False

def start_everything():
    """
    尝试启动 Everything 程序
    
    返回:
        bool: 如果启动成功，则返回 True，否则返回 False
    """
    try:
        # 尝试在标准安装位置查找 Everything.exe
        potential_paths = [
            r"C:\Program Files\Everything\Everything.exe",
            r"C:\Program Files (x86)\Everything\Everything.exe",
        ]
        
        for path in potential_paths:
            if os.path.exists(path):
                # 使用 subprocess 启动 Everything
                subprocess.Popen([path], shell=True)
                # 等待 Everything 启动
                import time
                time.sleep(2)
                return True
                
        # 如果无法找到 Everything 程序，显示消息
        print("无法找到 Everything 程序。请确保已安装 Everything 搜索工具。")
        return False
    except Exception as e:
        print(f"启动 Everything 时出错: {e}")
        return False

def search_files(search_text, search_folder=None):
    """
    使用 es.exe 搜索文件
    
    参数:
        search_text (str): 搜索字符串
        search_folder (str, optional): 搜索文件夹路径
    
    返回:
        list: 搜索结果列表
    """
    # 检查 Everything 是否在运行
    if not is_everything_running():
        print("Everything 程序未运行。正在尝试启动...")
        if not start_everything():
            print("无法启动 Everything 程序。请手动启动该程序后再试。")
            return []
    
    # 获取 es.exe 的完整路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    es_exe_path = os.path.join(current_dir, "bin", "es", "es.exe")
    
    # 构建命令
    command = [es_exe_path]
    
    # 添加搜索文件夹参数（如果提供）
    if search_folder:
        command.extend(["-path", search_folder])
    
    # 添加搜索文本
    command.append(search_text)
    
    try:
        # 使用subprocess直接调用命令，不尝试解码输出
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=False  # 不自动解码
        )
        
        # 读取原始字节输出
        stdout_data, stderr_data = process.communicate()
        
        # 尝试多种编码方式解码
        encodings = ['utf-8', 'gbk', 'cp950', 'big5', 'gb18030']
        
        # 先尝试解码stdout
        result_text = None
        for encoding in encodings:
            try:
                result_text = stdout_data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        # 如果所有编码都失败，使用 'replace' 模式
        if result_text is None:
            result_text = stdout_data.decode('utf-8', errors='replace')
        
        # 解码stderr (如有需要)
        error_text = None
        if stderr_data:
            for encoding in encodings:
                try:
                    error_text = stderr_data.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if error_text is None:
                error_text = stderr_data.decode('utf-8', errors='replace')
        
        # 检查执行状态
        if process.returncode == 0:
            # 分割输出行
            if result_text and result_text.strip():
                return [line for line in result_text.strip().split('\n') if line.strip()]
            return []
        else:
            # 执行失败
            print(f"搜索失败，错误代码: {process.returncode}")
            if error_text:
                print(f"错误信息: {error_text}")
            
            # 根据错误代码提供更具体的提示
            if process.returncode == 8:
                print("未找到 Everything IPC 窗口。请确认 Everything 程序已运行。")
            
            return []
            
    except Exception as e:
        print(f"执行搜索时发生错误: {str(e)}")
        return []

if __name__ == "__main__":
    # 测试函数
    results = search_files("*.txt", "C:\\")
    for result in results:
        print(result) 