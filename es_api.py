"""
文件搜索 API
提供简单的函数调用系统命令搜索文件，不使用 es.exe，避免显示任何窗口

使用方法:
    from es_api import search
    results = search("*.txt", "C:\\Users")
"""

import os
import subprocess
import sys
import tempfile
import time
import ctypes
import glob

def search(search_text, search_folder=None):
    """
    搜索文件
    
    参数:
        search_text (str): 搜索字符串
        search_folder (str, optional): 搜索文件夹路径，默认为当前目录
    
    返回:
        list: 搜索结果列表
    
    异常:
        RuntimeError: 如果搜索过程中出现错误
    """
    # 设置搜索文件夹，如果未提供则使用当前目录
    if not search_folder:
        search_folder = "."
    
    # 去除文件夹路径末尾的反斜杠
    search_folder = search_folder.rstrip('\\/')
    
    # 如果搜索字符串包含通配符，使用 dir 命令搜索
    if '*' in search_text or '?' in search_text:
        return _search_with_dir(search_text, search_folder)
    else:
        # 否则使用 findstr 搜索文件内容
        return _search_with_findstr(search_text, search_folder)

def _search_with_dir(pattern, folder):
    """使用 dir 命令搜索匹配的文件"""
    try:
        # 创建临时文件以捕获输出
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_path = temp_file.name
        temp_file.close()
        
        # 搜索文件
        cmd = f'cmd /c dir /b /s "{os.path.join(folder, pattern)}" > "{temp_path}" 2>nul'
        
        # 使用不显示窗口的方式执行命令
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        subprocess.call(cmd, startupinfo=startupinfo, 
                       creationflags=subprocess.CREATE_NO_WINDOW)
        
        # 读取结果
        results = []
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            with open(temp_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        results.append(line)
        
        # 删除临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        
        return results
    except Exception as e:
        raise RuntimeError(f"搜索文件时出错: {str(e)}")

def _search_with_findstr(text, folder):
    """使用 findstr 命令搜索文件内容"""
    try:
        # 创建临时文件以捕获输出
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_path = temp_file.name
        temp_file.close()
        
        # 使用 findstr 搜索文件内容
        cmd = f'cmd /c findstr /s /m /c:"{text}" "{folder}\\*" > "{temp_path}" 2>nul'
        
        # 使用不显示窗口的方式执行命令
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        subprocess.call(cmd, startupinfo=startupinfo, 
                       creationflags=subprocess.CREATE_NO_WINDOW)
        
        # 读取结果
        results = []
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            with open(temp_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        results.append(line)
        
        # 删除临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        
        return results
    except Exception as e:
        raise RuntimeError(f"搜索文件内容时出错: {str(e)}")

def _search_with_python(pattern, folder):
    """使用 Python 的 glob 模块搜索文件"""
    try:
        results = []
        # 使用递归 glob 搜索
        for file in glob.glob(os.path.join(folder, '**', pattern), recursive=True):
            results.append(os.path.abspath(file))
        return results
    except Exception as e:
        raise RuntimeError(f"使用 Python 搜索文件时出错: {str(e)}")

if __name__ == "__main__":
    # 简单的命令行测试
    if len(sys.argv) > 1:
        try:
            results = search(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
            print(f"找到 {len(results)} 个结果:")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r}")
        except Exception as e:
            print(f"错误: {e}")
    else:
        print("使用方法: python es_api.py <搜索字符串> [搜索文件夹]") 