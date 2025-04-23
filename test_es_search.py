from es_search import search_files

print("测试搜索功能...")

try:
    # 在当前目录搜索 Python 文件
    results = search_files("*.py", ".")
    print(f"在当前目录找到 {len(results)} 个 Python 文件")
    
    # 显示前几个结果
    if results:
        print("前 3 个结果:")
        for r in results[:3]:
            print(r)
    else:
        print("未找到结果")
except Exception as e:
    print(f"错误: {e}")

print("测试完成") 