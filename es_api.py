"""
ES.EXE 搜索 API
提供简单的函数调用 es.exe 进行文件搜索

使用方法:
    from es_api import search
    results = search("*.txt", "C:\\Users")
"""

import os
import sys
import tempfile

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
    
    # 创建临时文件用于保存输出
    temp_fd, temp_file = tempfile.mkstemp(suffix='.txt')
    os.close(temp_fd)
    
    try:
        # 构建命令行（使用直接的 CMD 方式）
        cmd_args = [es_exe_path, "-hide-empty-search-results"]
        
        if search_folder:
            cmd_args.extend(["-path", search_folder])
            
        cmd_args.append(search_text)
        
        # 构建 CMD 命令字符串
        cmd_parts = []
        for arg in cmd_args:
            # 对参数进行适当的引号处理
            if " " in arg or "\"" in arg:
                quoted_arg = f'"{arg.replace("\"", "\\\"")}"'
                cmd_parts.append(quoted_arg)
            else:
                cmd_parts.append(arg)
                
        cmd_str = " ".join(cmd_parts)
        
        # 添加输出重定向
        full_cmd = f'cmd.exe /c {cmd_str} > "{temp_file}" 2>&1'
        
        # 使用 os.system 直接调用 CMD 命令
        exit_code = os.system(full_cmd)
        
        # 读取结果文件
        try:
            with open(temp_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                results = [line.strip() for line in content.splitlines() if line.strip()]
        except Exception as e:
            raise RuntimeError(f"读取结果文件时出错: {str(e)}")
        
        # 检查执行状态
        if exit_code == 0:
            return results
        else:
            # 构建错误消息
            error_msg = f"搜索失败，错误代码: {exit_code}"
            if results:  # 如果有错误输出
                error_msg += f"\n错误信息: {' '.join(results)}"
            
            # 根据错误代码提供更具体的提示
            if exit_code == 8 * 256:  # os.system 返回的错误码乘以 256
                error_msg += "\n未找到 Everything IPC 窗口。请确认 Everything 程序已运行，或使用非GUI模式运行。"
            
            raise RuntimeError(error_msg)
            
    finally:
        # 删除临时文件
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except:
            pass

if __name__ == "__main__":
    # 简单的命令行测试
    if len(sys.argv) > 1:
        try:
            search_str = sys.argv[1]
            folder = sys.argv[2] if len(sys.argv) > 2 else None
            
            print(f"正在搜索: {search_str}")
            if folder:
                print(f"在文件夹: {folder}")
                
            results = search(search_str, folder)
            
            print(f"找到 {len(results)} 个结果:")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r}")
        except Exception as e:
            print(f"错误: {e}")
    else:
        print("使用方法: python es_api.py <搜索字符串> [搜索文件夹]") 