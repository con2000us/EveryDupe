# Everything 搜索工具

这是一个基于 Everything 搜索引擎的简单搜索工具，使用 Python 编写，提供了命令行和图形界面两种使用方式。

## 文件说明

- `es_api.py`: 核心 API 模块，提供简单的 search 函数调用 es.exe
- `es_cmd.py`: 简单的命令行工具，基于 es_api.py
- `es_search.py`: 包含检测和启动 Everything 程序的搜索模块
- `es_search_gui.py`: 图形用户界面，基于 tkinter 实现
- `example.py`: 使用 es_api.py 的示例程序
- `bin/es/`: Everything 搜索引擎命令行工具目录 (需要手动添加 es.exe)

## 安装依赖

1. 安装 Python 依赖库：

```
pip install -r requirements.txt
```

2. 获取并安装 es.exe：
   - 下载并安装 [Everything 搜索引擎](https://www.voidtools.com/zh-cn/)
   - 从安装目录复制 `es.exe` 到 `bin/es/` 目录
   - 或下载 [ES 命令行工具](https://www.voidtools.com/zh-cn/downloads/) 并解压到 `bin/es/` 目录

## 功能特点

- 可以指定搜索字符串和搜索文件夹
- 返回搜索结果列表
- 支持多种编码（解决中文编码问题）
- 自动检测并尝试启动 Everything 程序（仅在 es_search.py/GUI 版本）
- 提供简单的 API 接口，方便在其他程序中调用

## 使用方法

### API 方式（推荐）

最简单的使用方式是导入 `es_api.py` 模块：

```python
from es_api import search

# 搜索整个系统中的所有文本文件
results = search("*.txt")

# 在指定文件夹中搜索 Python 文件
results = search("*.py", "C:\\Projects")

# 打印结果
for result in results:
    print(result)
```

### 命令行方式

可以使用 `es_cmd.py` 在命令行中快速搜索：

```
python es_cmd.py "*.txt" "C:\Users"
```

### 图形界面方式

直接运行 `es_search_gui.py` 文件：

```
python es_search_gui.py
```

在打开的图形界面中：
1. 输入要搜索的字符串
2. 可选：指定要搜索的文件夹（如果不指定则在 Everything 索引的全部位置搜索）
3. 点击"搜索"按钮开始搜索
4. 结果将显示在下方的文本区域

## 编码问题解决

此工具解决了中文环境下的编码问题，采用以下策略：
1. 不使用自动解码，而是获取原始字节输出
2. 尝试多种编码方式（utf-8、gbk、cp950、big5、gb18030）
3. 如果所有编码都失败，使用替换模式解码

## 示例程序

`example.py` 文件提供了使用 `es_api.py` 的完整示例：
- 在当前目录搜索 Python 文件
- 在 C 盘搜索文本文件
- 使用正则表达式搜索
- 搜索包含特定词的文件

## Git 仓库说明

- `bin/es/` 目录中的文件已在 `.gitignore` 中设置为不上传 GitHub
- 克隆本仓库后，需要手动添加 es.exe 到 `bin/es/` 目录
- 请查看 `bin/es/README.md` 获取更多信息

## 注意事项

- 确保系统中已安装 Everything 搜索软件
- 使用 es_search.py 或 GUI 版本时，会自动检测并尝试启动 Everything 程序
- 使用 es_api.py 时，需要确保 Everything 程序已在运行
- 本工具依赖于 `bin/es/es.exe` 命令行工具
- 需要 Python 3.6 或更高版本
- 图形界面需要 tkinter 支持（通常 Python 标准安装已包含） 