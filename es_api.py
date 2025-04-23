"""
ES.EXE 搜索 API
提供简单的函数调用 es.exe 进行文件搜索

使用方法:
    from es_api import search
    results = search("*.txt", "C:\\Users")
"""

import os
import subprocess
import sys

def search(search_text, search_folder=None):
    """
    使用 es.exe 搜索文件
    
    参数:
        search_text (str): 搜索字符串
        search_folder (str, optional): 搜索文件夹路径
    
    返回:
        list: 搜索结果列表
    
    异常:
        RuntimeError: 如果搜索过程中出现错误
    """
    # 获取 es.exe 的完整路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    es_exe_path = os.path.join(current_dir, "bin", "es", "es.exe")
    
    # 检查 es.exe 是否存在
    if not os.path.exists(es_exe_path):
        raise RuntimeError(f"找不到 es.exe 文件: {es_exe_path}")
    
    # 构建命令
    command = [es_exe_path]
    
    # 添加选项来阻止显示帮助窗口
    command.append("-hide-empty-search-results")
    
    # 添加搜索文件夹参数（如果提供）
    if search_folder:
        command.extend(["-path", search_folder])
    
    # 添加搜索文本
    command.append(search_text)
    
    try:
        # 使用subprocess调用命令
        # 在 Windows 系统上使用 CREATE_NO_WINDOW 标志避免显示命令行窗口
        creation_flags = 0
        if sys.platform == 'win32':
            creation_flags = subprocess.CREATE_NO_WINDOW
            
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # 使用 shell=False 避免额外窗口
            universal_newlines=False,  # 不自动解码
            creationflags=creation_flags
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
            # 分割输出行并返回非空行
            if result_text and result_text.strip():
                return [line for line in result_text.strip().split('\n') if line.strip()]
            return []
        else:
            # 处理错误情况
            error_msg = f"搜索失败，错误代码: {process.returncode}"
            if error_text:
                error_msg += f"\n错误信息: {error_text}"
            
            # 根据错误代码提供更具体的提示
            if process.returncode == 8:
                error_msg += "\n未找到 Everything IPC 窗口。请确认 Everything 程序已运行，或使用非GUI模式运行。"
            
            raise RuntimeError(error_msg)
            
    except Exception as e:
        raise RuntimeError(f"执行搜索时发生错误: {str(e)}")

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