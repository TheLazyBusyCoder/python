import tkinter as tk
from tkinter import filedialog
import re
import subprocess
import os

current_file = None 

def run_file():
    if current_file:
        os.system('cls')
        save_file()
        subprocess.Popen(["python", current_file], shell=True)

def open_file():
    global current_file
    file_path = filedialog.askopenfilename()
    if file_path:
        current_file = file_path
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
            apply_formatting_to_entire_text()
            app.title(current_file)

def save_file():
    global current_file
    if current_file:
        with open(current_file, 'w') as file:
            file.write(text.get(1.0, tk.END))
    else:
        save_file_as()

def save_file_as():
    global current_file
    file_path = filedialog.asksaveasfilename()
    if file_path:
        current_file = file_path
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))

def on_key_press(event):
    if (event.state & 0x4) and event.keysym.lower() == 's':
        save_file()
    elif (event.state & 0x4) and event.keysym.lower() == 'r':
        run_file()
    elif event.keysym == 'Return':
        # Find the start and end positions of the current line
        current_line_start = text.index("insert linestart")
        current_line_end = text.index("insert lineend")
        # Find the start and end positions of the previous line
        previous_line_start = text.index("insert -1 line linestart")
        previous_line_end = text.index("insert -1 line lineend")
        # Retrieve the content of the current and previous lines
        current_line = text.get(current_line_start, current_line_end)
        previous_line = text.get(previous_line_start, previous_line_end)
        # Calculate the indentation
        indentation = ""
        for char in previous_line:
            if char.isspace():
                indentation += char
            else:
                break
        if previous_line.endswith(":"):
            text.insert("insert", "  ")
        # Insert the new line with the same indentation
        text.insert("insert", indentation)
        update_line_numbers()

    elif event.keysym == 'space':
        apply_formatting_to_current_line()
    else:
        pass

def update_line_numbers(*args):
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    num_lines = text.get("1.0", "end-1c").count("\n") + 2
    line_numbers.insert("end", "\n".join(map(str, range(1, num_lines))))
    line_numbers.config(state="disabled")
    

def on_tab(event):
    text.insert(tk.INSERT, "  ")  # Insert two spaces when Tab is pressed
    return "break"

def on_backspace(event):
    text.delete("insert-1c linestart", "insert linestart")
    update_line_numbers()

python_keywords = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
]

def apply_formatting_to_current_line():
    # Get the current line where the cursor is
    current_line_start = text.index("insert linestart")
    current_line_end = text.index("insert lineend")
    current_line_text = text.get(current_line_start, current_line_end)
    
    for keyword in python_keywords:
        # Use regular expression to find and apply formatting to Python keywords within the current line
        matches = re.finditer(rf'\b{re.escape(keyword)}\b', current_line_text)
        for match in matches:
            start_index = current_line_start + "+%dc" % match.start()
            end_index = current_line_start + "+%dc" % match.end()
            text.tag_add("bold", start_index, end_index)  # Apply bold
            text.tag_add("red", start_index, end_index)  # Apply yellow color
            text.tag_add("italic", start_index, end_index)  # Apply italics

def apply_formatting_to_entire_text():
    # Get the entire text content
    entire_text = text.get("1.0", "end")

    for keyword in python_keywords:
        # Use regular expression to find and apply formatting to Python keywords in the entire text
        matches = re.finditer(rf'\b{re.escape(keyword)}\b', entire_text)
        for match in matches:
            start_index = "1.0 +%dc" % match.start()
            end_index = "1.0 +%dc" % match.end()
            text.tag_add("bold", start_index, end_index)  # Apply bold
            text.tag_add("red", start_index, end_index)  # Apply yellow color
            text.tag_add("italic", start_index, end_index)  # Apply italics

app = tk.Tk()
app.title("Simple Text Editor")
app.geometry("800x600")

line_numbers = tk.Text(app, width=4)
line_numbers.pack(side="left", fill="y")

line_numbers.config(
    bg='#1E1E1E',  # Dark background color
    fg='white',   # Lighter text color
    insertbackground='yellow',  # Yellow cursor color
    insertwidth=3,  # Cursor width
    insertofftime=300,  # Cursor blinking on for 300 milliseconds
    insertontime=600,  # Cursor blinking off for 600 milliseconds
    font=("Consolas", 17),  # Increased font size and font family
    selectbackground='yellow',  # Selection background color
    selectforeground='black'  # Selection text color
)

text = tk.Text(app, wrap="none")
text.pack(fill="both", expand=True)

text.bind("<Configure>", update_line_numbers)

text.tag_configure("bold", font=("Consolas", 17, "bold"))
text.tag_configure("red", foreground="red")
text.tag_configure("italic", font=("Consolas", 17, "italic"))

app.tk_setPalette(background='#1E1E1E', foreground='white')

text.config(
    bg='#1E1E1E',  # Dark background color
    fg='white',   # Lighter text color
    insertbackground='yellow',  # Yellow cursor color
    insertwidth=3,  # Cursor width
    insertofftime=300,  # Cursor blinking on for 300 milliseconds
    insertontime=600,  # Cursor blinking off for 600 milliseconds
    font=("Consolas", 17),  # Increased font size and font family
    selectbackground='yellow',  # Selection background color
    selectforeground='black'  # Selection text color
)

text.bind("<Tab>", on_tab)
text.bind('<BackSpace>', on_backspace)

menu = tk.Menu(app)
app.config(menu=menu)

file_menu = tk.Menu(menu)
run_menu = tk.Menu(menu)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Run", menu=run_menu)

run_menu.add_command(label="Run", command=run_file)

file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

app.bind('<Key>', on_key_press)

update_line_numbers()

app.mainloop()
