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
        # 构建命令行
        # 使用 -csv 参数以获取简洁的输出
        cmd_args = [es_exe_path, "-hide-empty-search-results", "-csv"]
        
        if search_folder:
            cmd_args.extend(["-path", search_folder])
            
        cmd_args.append(search_text)
        
        # 构建 CMD 命令字符串 - 增强引号处理
        cmd_parts = []
        for arg in cmd_args:
            # 对包含空格或特殊字符的参数加引号
            if " " in arg or "\"" in arg or "'" in arg or "&" in arg or "|" in arg or ">" in arg or "<" in arg:
                # 正确处理参数中的引号
                if "\"" in arg:
                    arg = arg.replace("\"", "\\\"")
                quoted_arg = f'"{arg}"'
                cmd_parts.append(quoted_arg)
            else:
                cmd_parts.append(arg)
                
        cmd_str = " ".join(cmd_parts)
        
        # 强制使用输出编码，避免中文乱码
        # ANSI = 936 (GBK), UTF-8 = 65001
        chcp_cmd = "chcp 65001 > nul & "
        
        # 添加输出重定向
        full_cmd = f'cmd.exe /c {chcp_cmd}{cmd_str} > "{temp_file}" 2>&1'
        
        # 使用 os.system 直接调用 CMD 命令
        exit_code = os.system(full_cmd)
        
        # 尝试不同编码读取结果文件
        encodings_to_try = ['utf-8', 'gbk', 'cp950', 'big5', 'gb18030']
        raw_lines = []
        success = False
        
        # Unicode 替换字符，表示无法解码的字符
        replacement_char = "\ufffd"
        
        for encoding in encodings_to_try:
            try:
                with open(temp_file, 'r', encoding=encoding) as f:
                    content = f.read()
                    if content:
                        temp_lines = [line.strip() for line in content.splitlines() if line.strip()]
                        # 简单检查编码是否有效 - 如果有过多乱码字符，可能不是正确的编码
                        if temp_lines and not any(replacement_char in line for line in temp_lines[:min(3, len(temp_lines))]):
                            raw_lines = temp_lines
                            success = True
                            break
            except UnicodeDecodeError:
                continue
        
        # 如果所有编码都失败，使用 latin1（不会失败，但可能有乱码）
        if not success and not raw_lines:
            try:
                with open(temp_file, 'r', encoding='latin1', errors='replace') as f:
                    content = f.read()
                    raw_lines = [line.strip() for line in content.splitlines() if line.strip()]
            except Exception as e:
                raise RuntimeError(f"读取结果文件时出错: {str(e)}")
        
        # 处理 CSV 格式输出
        results = []
        if raw_lines:
            # 移除第一行（通常是标题行，如 "Filename"）
            if len(raw_lines) > 1 and (raw_lines[0].lower() == "filename" or 
                                       raw_lines[0].lower() == '"filename"'):
                data_lines = raw_lines[1:]
            else:
                data_lines = raw_lines
                
            # 处理每一行，移除多余的引号
            for line in data_lines:
                # 移除行两端的引号（如果有）
                if line.startswith('"') and line.endswith('"'):
                    line = line[1:-1]
                results.append(line)
        
        # 检查执行状态
        if exit_code == 0:
            return results
        else:
            # 构建错误消息
            error_msg = f"搜索失败，错误代码: {exit_code}"
            if raw_lines:  # 如果有错误输出
                error_msg += f"\n错误信息: {' '.join(raw_lines)}"
            
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