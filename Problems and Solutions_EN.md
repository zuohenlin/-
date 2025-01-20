# 一.At first I wanted to call OllamaAPI directly for interaction, but due to an unknown error I was unable to use the requests module to send Http requests to OllamaAPI
![Using the requests library](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145551527.png)
![Http request](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145639633.png)
## Ollama is running normally
![Ollama is running.](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145723654.png)
## But the API interface is not accessible
![API is not available.](https://gitee.com/zuohenlin/picture/raw/master/img/20250120145837387.png)
## In order to solve this problem, we asked the teacher
![Observation Problem](https://gitee.com/zuohenlin/picture/raw/master/img/20250120150156479.jpg)
![Propose a solution](https://gitee.com/zuohenlin/picture/raw/master/img/20250120150319713.jpg)
## The teacher didn't know what the problem was, but gave us a solution.
### Directly using the Ollama Python library
![Ollama Python library](https://gitee.com/zuohenlin/picture/raw/master/img/20250120150722952.png)
### After modification
![Importing Libraries](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151048779.png)
![Using the Library](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151133722.png)
### Successful operation
![Successful operation](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151349135.png)
# 二.I thought that each step required user input, which was too complicated, so I came up with the idea of ​​making a GUI interface.
## Using the tkinter library to implement the GUI interface
### Code for importing tkinter related modules:
```python
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
```
### These modules provide functionality for creating windows, dialog boxes, message boxes, scrolling text boxes, and other GUI elements.
## Functionality
![GUI interface](https://gitee.com/zuohenlin/picture/raw/master/img/20250120151918788.png)