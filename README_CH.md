# 利用Ollama+qwen+Python实现文档摘要（TXT+DOC+PDF）
## 一.利用Ollama部署本地大语言模型
>### 1.Ollama简介
>>#### Ollama 是一个本地运行的大语言模型（LLM）工具平台，允许用户在本地设备上运行和管理大模型，而无需依赖云服务。它支持多种开源模型，并提供了用户友好的接口，非常适合开发者和企业使用。

>### 2.Ollama安装
>>#### 首先，从[Ollama官网](https://ollama.com/)下载安装包，并按照提示完成安装。
>>>##### 注:Ollama 安装不需要管理员权限，默认安装在你的用户目录中。Windows系统中，Ollama下载的模型文件默认存放在用户文件夹下的特定目录中。具体来说，默认路径通常为C:\Users\<用户名>\.ollama\models。这里，<用户名>指的是当前Windows系统的登录用户名。
##### 若想将Ollama应用程序安装在不同于用户目录的位置，请使用以下代码启动安装程序：
```powershell
OllamaSetup.exe /DIR="location" # 将location改为你想要安装的路径
```
##### 要更改 Ollama 存储下载模型的位置，而不是使用你的主目录，可以在你的用户账户中设置环境变量 OLLAMA_MODELS
>##### 1.启动设置（Windows 11）或控制面板（Windows 10）应用程序，并搜索 环境变量。
>##### 2.编辑或创建一个新的用户账户变量 OLLAMA_MODELS，设置为你希望存储模型的路径。
>##### 3.点击确定/应用以保存。（如果 Ollama 已经在运行，请退出系统托盘中的应用程序，然后从开始菜单或在保存环境变量后启动的新终端中重新启动它。）

>### 3.Ollama 命令介绍
>Ollama 提供了几个简单易用的命令，基本功能如下：

```sh
Usage:
  ollama [flags]
  ollama [command]
Available Commands:
  serve       启动 Ollama 服务
  create      从 Modelfile 创建一个模型
  show        查看模型详细信息
  run         运行一个模型
  stop        停止正在运行的模型
  pull        从注册表拉取一个模型
  push        将一个模型推送到注册表
  list        列出所有可用的模型
  ps          列出当前正在运行的模型
  cp          复制一个模型
  rm          删除一个模型
  help        获取关于任何命令的帮助信息
  Flags:
  -h, --help      help for ollama
  -v, --version   Show version information
  ```

>### 3.下载大模型
>#### 在[Ollama官网](https://ollama.com/)的[Models页面](https://ollama.com/search)中，可以找到Ollama支持的大模型列表。
>##### 本文利用qwen2.5:0.5b和qwen2.5:7b作为示例
>![Ollama Models页面](https://gitee.com/zuohenlin/picture/raw/master/img/20250120100333049.png)
查看模型信息
  选择一个模型后，点击进入可以查看模型的详细信息。
  ![查看模型详细信息](https://gitee.com/zuohenlin/picture/raw/master/img/20250120110352578.png)
  使用 ollama run 命令可以在拉取模型后直接进入交互窗口。如果只想下载模型而不进入交互界面，可以使用 ollama pull 命令。
  ```powershell
  ollama run qwen2.5:0.5b
  ollama run qwen2.5:7b
  ```
  等待模型下载完成后，会直接进入交互界面。
  在命令行中输入消息，即可与模型进行交互。
### 交互窗口命令
在交互窗口中输入 /? 可以查看可用命令。
```sh
Available Commands:
  /set            设置会话变量
  /show           显示模型信息
  /load <model>   加载会话或模型
  /save <model>   保存当前会话
  /clear          清除会话上下文
  /bye            退出会话
  /?, /help       显示命令帮助
  /? shortcuts    显示快捷键帮助

Use """ to begin a multi-line message.
```
## 二.使用Python实现文档摘要
### 所需依赖库安装
``` python
pip install python-docx PyPDF2 ollama
```
以下是使用Python和Ollama实现文档摘要的示例代码：
```python
import os
from docx import Document
import PyPDF2
from ollama import chat
from ollama import ChatResponse
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# 读取文本文件内容
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        messagebox.showerror("错误", f"读取文件时发生错误：{e}")
        return None

# 读取.docx文件内容
def read_docx_file(file_path):
    try:
        doc = Document(file_path)
        content = '\n'.join([para.text for para in doc.paragraphs])
        return content
    except Exception as e:
        messagebox.showerror("错误", f"读取文件时发生错误：{e}")
        return None

# 读取PDF文件内容
def read_pdf_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
        return content
    except Exception as e:
        messagebox.showerror("错误", f"读取文件时发生错误：{e}")
        return None

# 创建摘要提示
def create_summary_prompt(content, language, length):
    prompt = f"Summarize the following text in {language} with a length of about {length} words:\n{content}"
    return prompt

# 使用Ollama模型生成摘要
def generate_summary(model, prompt):
    try:
        response: ChatResponse = chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        return response.message.content
    except Exception as e:
        messagebox.showerror("错误", f"生成摘要时发生错误：{e}")
        return None

# 检查摘要字数并重新生成
def generate_summary_with_length_check(model, content, language, target_length, tolerance=10):
    prompt = create_summary_prompt(content, language, target_length)
    summary = generate_summary(model, prompt)
    if summary is None:
        return None

    # 检查摘要字数
    summary_length = len(summary.split())
    while abs(summary_length - target_length) > tolerance:
        # 调整长度参数并重新生成
        if summary_length > target_length:
            target_length -= 10
        else:
            target_length += 10
        prompt = create_summary_prompt(content, language, target_length)
        summary = generate_summary(model, prompt)
        if summary is None:
            break
        summary_length = len(summary.split())

    return summary

# 选择文件并读取内容
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("DOCX files", "*.docx"), ("PDF files", "*.pdf")])
    if file_path:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.txt':
            content = read_text_file(file_path)
        elif file_extension == '.docx':
            content = read_docx_file(file_path)
        elif file_extension == '.pdf':
            content = read_pdf_file(file_path)
        else:
            messagebox.showerror("错误", "不支持的文件格式")
            return
        
        if content is not None:
            global file_content
            file_content = content
            language_menu.config(state='normal')
            language_menu.set('')  # 清空当前选择
            language_menu.focus()  # 聚焦到语言选择下拉菜单
        else:
            messagebox.showerror("错误", "文件内容读取失败")
    else:
        messagebox.showerror("错误", "未选择文件")

# 选择语言后启用字数输入框
def on_language_selected(event):
    length_entry.config(state='normal')
    length_entry.delete(0, tk.END)  # 清空当前输入
    length_entry.focus()  # 聚焦到字数输入框

# 生成摘要
def generate_summary_button():
    language = language_var.get()
    length = length_var.get()
    model = model_var.get()
    content = file_content

    if language and length and model and content:
        try:
            target_length = int(length)
            summary = generate_summary_with_length_check(model, content, language, target_length)
            if summary is not None:
                summary_text.delete(1.0, tk.END)
                summary_text.insert(tk.END, summary)
            else:
                messagebox.showerror("错误", "摘要生成失败")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的字数")
    else:
        messagebox.showerror("错误", "请确保所有信息已填写")

# 创建主窗口
root = tk.Tk()
root.title("文档摘要生成器")

# 创建变量
language_var = tk.StringVar()
length_var = tk.StringVar()
model_var = tk.StringVar()
file_content = None  # 保存文件内容的全局变量

# 创建文件选择按钮
tk.Label(root, text="选择文件：").grid(row=0, column=0, padx=10, pady=10)
select_file_button = tk.Button(root, text="选择文件", command=select_file)
select_file_button.grid(row=0, column=1, padx=10, pady=10)

# 创建摘要语言选择下拉菜单
tk.Label(root, text="摘要语言：").grid(row=1, column=0, padx=10, pady=10)
languages = ['English', 'Chinese', 'Spanish']  # 示例语言列表
language_menu = ttk.Combobox(root, textvariable=language_var, values=languages, state='disabled')
language_menu.grid(row=1, column=1, padx=10, pady=10)
language_menu.bind('<<ComboboxSelected>>', on_language_selected)

# 创建摘要长度输入框
tk.Label(root, text="摘要长度：").grid(row=2, column=0, padx=10, pady=10)
length_entry = tk.Entry(root, textvariable=length_var, state='disabled')
length_entry.grid(row=2, column=1, padx=10, pady=10)

# 创建模型选择下拉菜单
tk.Label(root, text="选择模型：").grid(row=3, column=0, padx=10, pady=10)
models = ["qwen2.5:0.5b", "qwen2.5:7b", "model3"]  # 示例模型列表
model_menu = ttk.Combobox(root, textvariable=model_var, values=models)
model_menu.grid(row=3, column=1, padx=10, pady=10)

# 创建生成摘要按钮
generate_button = tk.Button(root, text="生成摘要", command=generate_summary_button)
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# 创建摘要显示文本框
summary_text = scrolledtext.ScrolledText(root, width=80, height=20)
summary_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# 运行主循环
root.mainloop()
```
