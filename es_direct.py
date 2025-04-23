"""
直接使用 CMD 命令调用 es.exe 进行搜索，避免任何 GUI 窗口
"""

import os
import sys
import subprocess
import tempfile

def direct_search(search_text, search_folder=None):
    """
    使用与 CMD 完全相同的方式调用 es.exe
    
    参数:
        search_text (str): 搜索字符串
        search_folder (str, optional): 搜索文件夹路径
    
    返回:
        list: 搜索结果列表
    """
    # 获取 es.exe 的完整路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    es_exe_path = os.path.join(current_dir, "bin", "es", "es.exe")
    
    if not os.path.exists(es_exe_path):
        print(f"错误: 找不到 es.exe 文件: {es_exe_path}")
        return []
        
    # 创建临时文件用于保存输出
    temp_fd, temp_file = tempfile.mkstemp(suffix='.txt')
    os.close(temp_fd)
    
    try:
        # 构建命令行（不使用任何 Python 的 subprocess 功能）
        cmd_args = [es_exe_path, "-hide-empty-search-results"]
        
        if search_folder:
            cmd_args.extend(["-path", search_folder])
            
        cmd_args.append(search_text)
        
        # 构建 CMD 命令字符串
        cmd_parts = []
        for arg in cmd_args:
            # 对参数进行适当的引号处理
            if " " in arg or "\"" in arg:
                quoted_arg = f'"{arg.replace("`\"", "\\\"")}"'
                cmd_parts.append(quoted_arg)
            else:
                cmd_parts.append(arg)
                
        cmd_str = " ".join(cmd_parts)
        
        # 添加输出重定向
        full_cmd = f'cmd.exe /c {cmd_str} > "{temp_file}"'
        
        # 使用 os.system 而不是 subprocess
        # 这在行为上更接近直接在 CMD 中运行
        os.system(full_cmd)
        
        # 读取结果文件
        try:
            with open(temp_file, 'r', encoding='utf-8', errors='replace') as f:
                results = [line.strip() for line in f if line.strip()]
            return results
        except Exception as e:
            print(f"读取结果文件时出错: {e}")
            return []
            
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
        search_str = sys.argv[1]
        folder = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"正在搜索: {search_str}")
        if folder:
            print(f"在文件夹: {folder}")
            
        results = direct_search(search_str, folder)
        
        print(f"找到 {len(results)} 个结果:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r}")
    else:
        print("使用方法: python es_direct.py <搜索字符串> [搜索文件夹]") 