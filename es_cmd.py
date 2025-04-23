import sys
import os
from es_search import search_files

def main():
    """
    ES.EXE 命令行工具
    使用方法: python es_cmd.py <搜索字符串> [搜索文件夹]
    """
    
    # 检查参数
    if len(sys.argv) < 2:
        print("使用方法: python es_cmd.py <搜索字符串> [搜索文件夹]")
        print("例如: python es_cmd.py \"*.txt\" \"C:\\Users\"")
        return
    
    # 获取搜索字符串
    search_text = sys.argv[1]
    
    # 获取搜索文件夹（如果有）
    search_folder = None
    if len(sys.argv) > 2:
        search_folder = sys.argv[2]
    
    print(f"正在搜索: {search_text}")
    if search_folder:
        print(f"在文件夹: {search_folder}")
    
    try:
        # 执行搜索
        results = search_files(search_text, search_folder)
        
        # 显示结果
        if results:
            print(f"\n找到 {len(results)} 个结果:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result}")
        else:
            print("\n未找到任何结果。")
            
    except Exception as e:
        print(f"搜索过程中发生错误: {str(e)}")
    
if __name__ == "__main__":
    main() 