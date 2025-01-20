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