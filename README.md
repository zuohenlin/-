# [Switch to the Chinese version](https://github.com/zuohenlin/document_summarizer/blob/main/README_CH.md)
# Implementing Document Summarization with Ollama + Qwen + Python (TXT + DOC + PDF)
## 一.Deploying a Local Large Language Model with Ollama
>### 1.Introduction to Ollama
>>#### Ollama is a local large language model (LLM) tool platform that allows users to run and manage large models on their local devices without relying on cloud services. It supports various open-source models and provides a user-friendly interface, making it suitable for developers and enterprises.

>### 2.Installation of Ollama
>>#### First, download the installation package from the [Ollama official website](https://ollama.com/) and follow the instructions to complete the installation.
>>>##### Note: Ollama installation does not require administrative privileges and is installed by default in your user directory. On Windows systems, the downloaded model files are stored by default in a specific directory under the user folder, usually located at C:\Users\<username>\.ollama\models. Here, <username> refers to the current Windows system login username.
##### If you want to install the Ollama application in a location other than the user directory, you can use the following command to start the installation program:
```powershell
OllamaSetup.exe /DIR="location" # Replace "location" with your desired installation path
```
##### To change the location where Ollama stores the downloaded models (instead of using your home directory), you can set the OLLAMA_MODELS environment variable in your user account:
>##### 1.Open the Settings (Windows 11) or Control Panel (Windows 10) application and search for "Environment Variables".
>##### 2.Edit or create a new user account variable named OLLAMA_MODELS and set it to the desired path.
>##### 3.Click "OK" or "Apply" to save the changes. (If Ollama is already running, exit the application from the system tray and restart it from the Start menu or a new terminal after saving the environment variable.)

>### 3.Ollama Command Introduction
>Ollama provides several easy-to-use commands with the following basic functions:

```sh
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start the Ollama service
  create      Create a model from a Modelfile
  show        Display detailed information about a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from the registry
  push        Push a model to the registry
  list        List all available models
  ps          List currently running models
  cp          Copy a model
  rm          Delete a model
  help        Get help for any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information
  ```

>### 3.Downloading Large Models
>#### On the [Models page of the Ollama official website](https://ollama.com/search), you can find a list of large models supported by Ollama.
>##### In this article, we use qwen2.5:0.5b and qwen2.5:7b as examples.
>![Models page of the Ollama official website](https://gitee.com/zuohenlin/picture/raw/master/img/20250120100333049.png)
Check Model Information
  After selecting a model, click to view its detailed information.
  ![View detailed information about the model](https://gitee.com/zuohenlin/picture/raw/master/img/20250120110352578.png)
  You can use the ollama run command to directly enter the interactive window after pulling the model. If you only want to download the model without entering the interactive interface, you can use the ollama pull command.
  ```powershell
  ollama run qwen2.5:0.5b
  ollama run qwen2.5:7b
  ```
  After the model download is complete, you will be directly taken to the interactive interface. You can interact with the model by entering messages in the command line.

### Interactive Window Commands
In the interactive window, you can enter /? to view available commands:
```sh
Available Commands:
  /set            Set session variables
  /show           Display model information
  /load <model>   Load a session or model
  /save <model>   Save the current session
  /clear          Clear session context
  /bye            Exit the session
  /?, /help       Display command help
  /? shortcuts    Display shortcut help

Use """ to begin a multi-line message.
```
## 二.Implementing Document Summarization with Python
### Required Dependencies Installation
``` python
pip install python-docx PyPDF2 ollama
```
Below is an example code for implementing document summarization using Python and Ollama:
```python
import os
from docx import Document
import PyPDF2
from ollama import chat
from ollama import ChatResponse
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# Read the content of a text file
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return None

# Read the content of a .docx file
def read_docx_file(file_path):
    try:
        doc = Document(file_path)
        content = '\n'.join([para.text for para in doc.paragraphs])
        return content
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return None

# Read the content of a PDF file
def read_pdf_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
        return content
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return None

# Create a summary prompt
def create_summary_prompt(content, language, length):
    prompt = f"Summarize the following text in {language} with a length of about {length} words:\n{content}"
    return prompt

# Use the Ollama model to generate a summary
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
        messagebox.showerror("Error", f"An error occurred while generating the summary: {e}")
        return None

# Check the summary length and regenerate if necessary
def generate_summary_with_length_check(model, content, language, target_length, tolerance=10):
    prompt = create_summary_prompt(content, language, target_length)
    summary = generate_summary(model, prompt)
    if summary is None:
        return None

    # Check the summary length
    summary_length = len(summary.split())
    while abs(summary_length - target_length) > tolerance:
        # Adjust the length parameter and regenerate
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

# Select a file and read its content
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
            messagebox.showerror("Error", "Unsupported file format")
            return
        
        if content is not None:
            global file_content
            file_content = content
            language_menu.config(state='normal')
            language_menu.set('')  # Clear the current selection
            language_menu.focus()  # Focus on the language selection dropdown
        else:
            messagebox.showerror("Error", "Failed to read file content")
    else:
        messagebox.showerror("Error", "No file selected")

# Enable the word count input box after selecting a language
def on_language_selected(event):
    length_entry.config(state='normal')
    length_entry.delete(0, tk.END)  # Clear the current input
    length_entry.focus()  # Focus on the word count input box

# Generate the summary
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
                messagebox.showerror("Error", "Summary generation failed")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid word count")
    else:
        messagebox.showerror("Error", "Please ensure all information is filled in")

# Create the main window
root = tk.Tk()
root.title("Document Summary Generator")

# Create variables
language_var = tk.StringVar()
length_var = tk.StringVar()
model_var = tk.StringVar()
file_content = None  # Global variable to store file content

# Create file selection button
tk.Label(root, text="Select File:").grid(row=0, column=0, padx=10, pady=10)
select_file_button = tk.Button(root, text="Select File", command=select_file)
select_file_button.grid(row=0, column=1, padx=10, pady=10)

# Create summary language selection dropdown
tk.Label(root, text="Summary Language:").grid(row=1, column=0, padx=10, pady=10)
languages = ['English', 'Chinese', 'Spanish']  # Example language list
language_menu = ttk.Combobox(root, textvariable=language_var, values=languages, state='disabled')
language_menu.grid(row=1, column=1, padx=10, pady=10)
language_menu.bind('<<ComboboxSelected>>', on_language_selected)

# Create summary length input box
tk.Label(root, text="Summary Length:").grid(row=2, column=0, padx=10, pady=10)
length_entry = tk.Entry(root, textvariable=length_var, state='disabled')
length_entry.grid(row=2, column=1, padx=10, pady=10)

# Create model selection dropdown
tk.Label(root, text="Select Model:").grid(row=3, column=0, padx=10, pady=10)
models = ["qwen2.5:0.5b", "qwen2.5:7b", "model3"]  # Example model list
model_menu = ttk.Combobox(root, textvariable=model_var, values=models)
model_menu.grid(row=3, column=1, padx=10, pady=10)

# Create generate summary button
generate_button = tk.Button(root, text="Generate Summary", command=generate_summary_button)
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Create summary display text box
summary_text = scrolledtext.ScrolledText(root, width=80, height=20)
summary_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()
```
