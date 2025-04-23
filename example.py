"""
使用 es_api 搜索文件的示例程序

此示例展示了如何在其他 Python 程序中调用 es_api.py 中的 search 函数
"""

from es_api import search

def example_search():
    """
    演示如何使用 es_api 模块搜索文件
    """
    try:
        # 示例 1: 在当前目录搜索所有 Python 文件
        print("示例 1: 搜索所有 Python 文件")
        results = search("*.py", ".")
        print(f"找到 {len(results)} 个 Python 文件:")
        for i, path in enumerate(results, 1):
            print(f"  {i}. {path}")
        print()
        
        # 示例 2: 在 C 盘搜索所有文本文件 (可能结果较多)
        print("示例 2: 在 C 盘搜索文本文件 (限制前 5 个)")
        results = search("*.txt", "C:\\")
        print(f"找到 {len(results)} 个文本文件，显示前 5 个:")
        for i, path in enumerate(results[:5], 1):
            print(f"  {i}. {path}")
        print()
        
        # 示例 3: 使用正则表达式搜索
        print("示例 3: 使用正则表达式搜索")
        results = search("-regex .*\\.json$", ".")
        print(f"找到 {len(results)} 个 JSON 文件:")
        for i, path in enumerate(results, 1):
            print(f"  {i}. {path}")
        print()
        
        # 示例 4: 搜索带特定名称的文件
        print("示例 4: 搜索包含特定词的文件")
        results = search("search", ".")
        print(f"找到 {len(results)} 个包含 'search' 的文件:")
        for i, path in enumerate(results, 1):
            print(f"  {i}. {path}")
            
    except Exception as e:
        print(f"搜索过程中出错: {e}")

if __name__ == "__main__":
    print("ES.EXE 搜索示例")
    print("===============")
    print("注意: 确保 Everything 搜索程序正在运行")
    print()
    example_search() 