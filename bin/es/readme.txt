使用方法
es.exe [options] [search text]

[option]

可选选项。


<option>

必须选项。



常规命令行选项

以下命令兼容于任意版本 Everything。


-r

-regex

使用正则表达式搜索。


-i

-case

匹配大小写。


-w

-ww

-whole-word

-whole-words

匹配全字。


-p

-match-path

匹配全路径和文件名。


-h

-help

显示帮助。


-o <offset>

-offset <offset>

以以零为基础偏移显示搜索结果。


-n <num>

-max-results <num>

限定结果显示数目为 <num>。


-s

以全路径排序。


Everything 1.4 命令行选项

以下参数需要 Everything 1.4 或更新版本。


-a

-diacritics

匹配变音标记。


-name

-path-column

-full-path-and-name

-filename-column

-extension

-ext

-size

-date-created

-dc

-date-modified

-dm

-date-accessed

-da

-attributes

-attribs

-attrib

-file-list-file-name

-run-count

-date-run

-date-recently-changed

-rc

显示指定分栏。如果指定名称、路径或全路径和分栏名称，则默认使用全路径和名称分栏。

分栏可以以指定排序显示。


-sort name

-sort path

-sort size

-sort extension

-sort date-created

-sort date-modified

-sort date-accessed

-sort attributes

-sort file-list-file-name

-sort run-count

-sort date-recently-changed

-sort date-run

-sort-name

-sort-path

-sort-size

-sort-extension

-sort-date-created

-sort-date-modified

-sort-date-accessed

-sort-attributes

-sort-file-list-file-name

-sort-run-count

-sort-date-recently-changed

-sort-date-run

-sort name-ascending

-sort name-descending

-sort path-ascending

-sort path-descending

-sort size-ascending

-sort size-descending

-sort extension-ascending

-sort extension-descending

-sort date-created-ascending

-sort date-created-descending

-sort date-modified-ascending

-sort date-modified-descending

-sort date-accessed-ascending

-sort date-accessed-descending

-sort attributes-ascending

-sort attributes-descending

-sort file-list-file-name-ascending

-sort file-list-file-name-descending

-sort run-count-ascending

-sort run-count-descending

-sort date-recently-changed-ascending

-sort date-recently-changed-descending

-sort date-run-ascending

-sort date-run-descending

-sort-name-ascending

-sort-name-descending

-sort-path-ascending

-sort-path-descending

-sort-size-ascending

-sort-size-descending

-sort-extension-ascending

-sort-extension-descending

-sort-date-created-ascending

-sort-date-created-descending

-sort-date-modified-ascending

-sort-date-modified-descending

-sort-date-accessed-ascending

-sort-date-accessed-descending

-sort-attributes-ascending

-sort-attributes-descending

-sort-file-list-file-name-ascending

-sort-file-list-file-name-descending

-sort-run-count-ascending

-sort-run-count-descending

-sort-date-recently-changed-ascending

-sort-date-recently-changed-descending

-sort-date-run-ascending

-sort-date-run-descending

指定排序方式。搜索结果默认以名称排序。


-sort-ascending

-sort-descending

设置排序顺序。例如，以大小升序排列：-sort size -sort-ascending

如果不指定：大小则最大在前，最近日期在前和最大运行次数在前，其他排序以字母顺序排列。


-instance <name>

连接唯一实例名。

查阅多实例以获取更多信息。


-highlight

高亮结果。

高亮过多结果将会降低 "Everything" 性能。


-highlight-color <color>

<color> 为以下任一代码格式：

command prompt console colors and codes

高亮颜色 0x00-0xFF。

默认高亮颜色 0x0a (黑中亮绿)。


-csv

-efu

-txt

-m3u

-m3u8

更改显示格式。

使用 > 以重定向到文件或 | 管道到其他程序。

查阅以下 -export 选项来写入到文件。


-export-csv <out.csv>

-export-efu <out.efu>

-export-txt <out.txt>

-export-m3u <out.m3u>

-export-m3u8 <out.m3u8>

导出到文件。屏幕不是显示输出。


-size-format <format>

格式代码可以为以下任一数值：

数值	说明
0	自动
1	字节
2	KB
3	MB

-pause

-more

输出满页时暂停。


-hide-empty-search-results

无指定搜索时不显示结果。


-empty-search-help

无指定搜索时显示帮助。


-timeout <milliseconds>

发送查询前等待载入 Everything 数据库超时毫秒数。


-filename-color <color>

-name-color <color>

-path-color <color>

-extension-color <color>

-size-color <color>

-date-created-color <color>

-dc-color <color>

-date-modified-color <color>

-dm-color <color>

-date-accessed-color <color>

-da-color <color>

-attributes-color <color>

-file-list-filename-color <color>

-run-count-color <color>

-date-run-color <color>

-date-recently-changed-color <color>

-rc-color <color>

<color> 为以下任一代码格式：

command prompt console colors and codes

设置分栏颜色 0x00-0xFF。


-filename-width <width>

-name-width <width>

-path-width <width>

-extension-width <width>

-size-width <width>

-date-created-width <width>

-dc-width <width>

-date-modified-width <width>

-dm-width <width>

-date-accessed-width <width>

-da-width <width>

-attributes-width <width>

-file-list-filename-width <width>

-run-count-width <width>

-date-run-width <width>

-date-recently-changed-width <width>

-rc-width <width>

设置分栏宽度 0-200。


-size-leading-zero

-run-count-leading-zero

格式化为有前导零的数字，使用 -no-digit-grouping。


-no-digit-grouping

不以逗号分组数字。


-path <path>

搜索路径下子文件夹和文件。


-parent-path <path>

搜索父目录下子文件夹和文件。


-parent <path>

搜索指定父目录下子文件。


/o[sort]

DIR 排序样式。

排序必须为以下任一排序：

排序	说明
N	名称 升序。
-N	名称 降序。
S	大小 升序。
-S	大小 降序。
E	扩展名 升序。
-E	扩展名 降序。
D	修改时间 升序。
-D	修改时间 降序。

/ad

仅文件夹。


/a-d

仅文件。


/a[attributes]

DIR 属性搜索。

属性必须为以下任一属性：

属性	说明
R	只读。
H	隐藏。
S	系统。
D	目录。
A	存档。
V	设备。
N	常规。
T	临时。
P	稀疏文件
L	重分析点。
C	压缩。
O	离线。
I	未索引内容。
E	加密。
排除属性，使用 a - 前缀。

例如，查找非只读属性文件：es.exe /a-r

目录属性由 Everything 中结果是文件或文件夹决定，而不是文件属性。以属性：d 搜索真实目录属性。


-set-run-count <filename> <count>

设置指定文件名运行次数。不执行搜索操作。


-inc-run-count <filename>

增加指定文件名运行次数。不执行搜索操作。


-get-run-count <filename>

显示指定文件名运行次数。不执行搜索操作。


-save-settings

-clear-settings

保存或清除设置。不执行搜索操作。

设置保存在 es.exe 同目录下 es.ini 文件中。


限制
ES 无法访问书签或筛选器。


例子
导出全部 mp3 文件为 Everything 文件列表 mp3.efu：

es.exe *.mp3 -export-efu mp3.efu

显示最大的 10 个文件：

es.exe -sort size -n 10

显示最近修改的 10 个文件：

es.exe -sort dm -n 10

高亮搜索关键词 foo bar：

es.exe foo bar -highlight

使 ES 显示大小分栏、修改日期分栏和设置颜色且为默认设置：

es.exe -size -dm -sizecolor 0x0d -dmcolor 0x0b -save-settings

返回代码
ES 能返回以下任一错误级别代码：

错误级别	说明
0	无已知错误，搜索成功。
1	注册窗口类失败。
2	创建监听窗口失败。
3	内存溢出。
4	缺失额外的命令行选项参数。
5	创建导出文件失败。
6	未知参数。
7	发送查询到 Everything IPC 失败。
8	未找到 Everything IPC 窗口。请确认 Everything 客户端已运行。
