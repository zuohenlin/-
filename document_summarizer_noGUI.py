import os
from docx import Document
import PyPDF2
from ollama import chat
from ollama import ChatResponse

def read_text_file(file_path):
    """
    读取文本文件内容。

    参数:
    file_path (str): 文本文件的路径。

    返回:
    str: 文件内容，如果文件不存在或读取失败则返回None。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"文件{file_path}未找到")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

def read_docx_file(file_path):
    """
    读取.docx文件内容。

    参数:
    file_path (str): .docx文件的路径。

    返回:
    str: 文件内容，如果文件不存在或读取失败则返回None。
    """
    try:
        doc = Document(file_path)
        content = '\n'.join([para.text for para in doc.paragraphs])
        return content
    except FileNotFoundError:
        print(f"文件{file_path}未找到")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

def read_pdf_file(file_path):
    """
    读取PDF文件内容。

    参数:
    file_path (str): PDF文件的路径。

    返回:
    str: 文件内容，如果文件不存在或读取失败则返回None。
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
        return content
    except FileNotFoundError:
        print(f"文件{file_path}未找到")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

def create_summary_prompt(content, language, length):
    """
    创建摘要提示。

    参数:
    content (str): 文本文件的内容。
    language (str): 摘要的语言（如 'English'、'Chinese' 等）。
    length (int): 摘要的长度（词数）。

    返回:
    str: 摘要提示。
    """
    prompt = f"Summarize the following text in {language} with a length of about {length} words:\n{content}"
    return prompt

def generate_summary(model, prompt):
    """
    使用 Ollama 模型生成摘要。

    参数:
    model (str): 模型名称。
    prompt (str): 摘要提示。

    返回:
    str: 生成的摘要，如果通信失败则返回None。
    """
    try:
        response: ChatResponse = chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        return response.message.content
    except Exception as e:
        print(f"生成摘要时发生错误：{e}")
        return None

def main():
    """
    主函数，执行文档摘要生成流程。
    """
    file_path = input("请输入文本文件路径：")
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.txt':
        content = read_text_file(file_path)
    elif file_extension == '.docx':
        content = read_docx_file(file_path)
    elif file_extension == '.pdf':
        content = read_pdf_file(file_path)
    else:
        print("不支持的文件格式")
        return

    if content is None:
        return

    language = input("请输入摘要语言（如English、Chinese等）：")
    length = int(input("请输入摘要长度（词数）："))
    model = input("请输入要使用的 Ollama 模型名称：")

    prompt = create_summary_prompt(content, language, length)
    summary = generate_summary(model, prompt)

    if summary is not None:
        print("生成的摘要如下：")
        print(summary)

if __name__ == "__main__":
    main()