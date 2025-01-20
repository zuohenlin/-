# 一.在最开始我想直接调用OllamaAPI进行交互，但由于未知错误无法利用requests模块向OllamaAPI发送Http请求
![利用requests库](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145551527.png)
![Http请求](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145639633.png)
## Ollama是正常运行的
![Ollama is running.](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145723654.png)
## 但是API接口是不通的
![API is not available.](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145837387.png)
## 为了解决这个问题，我向老师请教
![观察问题](https://gitee.com/zuohenlin/picture/raw/master/img/20250120150156479.jpg)
![提出解决方案](https://gitee.com/zuohenlin/picture/raw/master/img/20250120150319713.jpg)
## 老师也不清楚问题出在哪里，但是给我们提出了解决方案
### 直接利用Ollama Python库
![Ollama Python库](https://gitee.com/zuohenlin/picture/raw/master/img/20250120150722952.png)
### 修改后
![导入库](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151048779.png)
![使用库](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151133722.png)
### 成功运行
![成功运行](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151349135.png)
# 二.我认为每一步运行都需要用户输入内容，步骤过于繁琐，产生了做出GUI界面的想法
## 利用tkinter 库实现 GUI 界面
### 导入 tkinter 相关模块的代码：
```python
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
```
### 这些模块提供了创建窗口、对话框、消息框、滚动文本框和其他 GUI 元素的功能。
## 功能实现
![GUI界面](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151918788.png)