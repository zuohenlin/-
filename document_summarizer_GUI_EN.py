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