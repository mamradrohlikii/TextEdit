import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.geometry("1000x700")


# Set the window title
root.title("MRR Software - Notebook")

# Create a line number bar
line_number_bar = tk.Text(root, width=4, padx=3, takefocus=0, border=0, background='lightgrey', state='disabled')
line_number_bar.pack(side='left', fill='y')

# Create a text box
text_box = tk.Text(root, wrap='word', undo=True)
text_box.pack(expand=True, fill='both', padx=10, pady=10)

# Create a menu
menu_bar = tk.Menu(root, font=("Arial", 10))

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".mrre", filetypes=[("MRR Editor Files", "*.mrre"), ("All Files", "*.*")])
    if not file_path:
        return
    with open(file_path, 'r') as file:
        content = file.read()
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, content)
    root.after(100, lambda: apply_formatting(file_path))
    text_box.edit_reset()  # Reset the undo/redo stack to avoid showing formatting data
    text_box.edit_modified(False)  # Reset the modified flag

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mrre", filetypes=[("MRR Editor Files", "*.mrre"), ("All Files", "*.*")])
    if not file_path:
        return
    content = text_box.get(1.0, tk.END)
    with open(file_path, 'w') as file:
        file.write(content)
    save_formatting(file_path)
    text_box.edit_modified(False)  # Reset the modified flag

def apply_formatting(file_path):
    text_box.tag_remove('all', '1.0', tk.END)
    try:
        with open(file_path + '.meta', 'r') as meta_file:
            lines = meta_file.readlines()
            for line in lines:
                if line.startswith('TAG:'):
                    tag, start, end, options = line.strip().split('|')
                    text_box.tag_add(tag[4:], start, end)
                    text_box.tag_config(tag[4:], **eval(options))
    except FileNotFoundError:
        pass

def save_formatting(file_path):
    with open(file_path + '.meta', 'w') as meta_file:
        for tag in text_box.tag_names():
            ranges = text_box.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                end = ranges[i+1]
                options = text_box.tag_config(tag)
                meta_file.write(f'TAG:{tag}|{start}|{end}|{options}\n')

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))
file_menu.add_command(label="New", command=lambda: text_box.delete(1.0, tk.END))
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Function to apply tag to selected text
def apply_tag(tag_name, **kwargs):
    try:
        text_box.tag_add(tag_name, "sel.first", "sel.last")
    except tk.TclError:
        return
    text_box.tag_config(tag_name, **kwargs)

# Create a font menu
font_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))

# Add font options
fonts = ["Arial", "Courier", "Helvetica", "Times", "Verdana", "Comic Sans MS", "Georgia", "Impact", "Lucida Console", "Tahoma", "Trebuchet MS", "Symbol"]
for font in fonts:
    font_menu.add_command(label=font, command=lambda f=font: apply_tag(f, font=(f, 12)))
menu_bar.add_cascade(label="Font", menu=font_menu)

# Create a Size menu
size_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))

# Add size options
sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
for size in sizes:
    size_menu.add_command(label=str(size), command=lambda s=size: apply_tag(f'size_{s}', font=(text_box.cget("font").split()[0], s)))
menu_bar.add_cascade(label="Size", menu=size_menu)

# Create a Color menu
color_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))

# Add color options
colors = ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink", "Brown", "Gray"]
for color in colors:
    color_menu.add_command(label=color, command=lambda c=color: apply_tag(f'color_{c}', foreground=c))
menu_bar.add_cascade(label="Color", menu=color_menu)

# Function to center the selected text
def center_text():
    try:
        text_box.tag_add('center', 'sel.first', 'sel.last')
    except tk.TclError:
        return
    text_box.tag_config('center', justify='center')

# Add Center option to the menu
align_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))
align_menu.add_command(label="Center", command=center_text)
menu_bar.add_cascade(label="Align", menu=align_menu)

# Function to align the selected text to the right
def align_right():
    try:
        text_box.tag_add('right', 'sel.first', 'sel.last')
    except tk.TclError:
        return
    text_box.tag_config('right', justify='right')

# Add Right Align option to the menu
align_menu.add_command(label="Right", command=align_right)

# Function to align the selected text to the left
def align_left():
    try:
        text_box.tag_add('left', 'sel.first', 'sel.last')
    except tk.TclError:
        return
    text_box.tag_config('left', justify='left')

# Add Left Align option to the menu
align_menu.add_command(label="Left", command=align_left)

# Create a Background Color menu
bg_color_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))

# Add background color options
bg_colors = ["White", "LightGray", "LightYellow", "LightGreen", "LightBlue", "LightPink", "LightCyan"]
for bg_color in bg_colors:
    bg_color_menu.add_command(label=bg_color, command=lambda c=bg_color: apply_tag(f'bg_color_{c}', background=c))
menu_bar.add_cascade(label="Background Color", menu=bg_color_menu)

def find_and_replace():
    find_replace_window = tk.Toplevel(root)
    find_replace_window.title("Find and Replace")

    tk.Label(find_replace_window, text="Find:", font=("Arial", 10)).grid(row=0, column=0, padx=4, pady=4)
    find_entry = tk.Entry(find_replace_window, width=30, font=("Arial", 10))
    find_entry.grid(row=0, column=1, padx=4, pady=4)

    tk.Label(find_replace_window, text="Replace:", font=("Arial", 10)).grid(row=1, column=0, padx=4, pady=4)
    replace_entry = tk.Entry(find_replace_window, width=30, font=("Arial", 10))
    replace_entry.grid(row=1, column=1, padx=4, pady=4)

    def find_text():
        text_box.tag_remove('found', '1.0', tk.END)
        find_text = find_entry.get()
        if find_text:
            idx = '1.0'
            while True:
                idx = text_box.search(find_text, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                lastidx = f'{idx}+{len(find_text)}c'
                text_box.tag_add('found', idx, lastidx)
                idx = lastidx
            text_box.tag_config('found', foreground='white', background='blue')

    def replace_text():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
        content = text_box.get('1.0', tk.END)
        new_content = content.replace(find_text, replace_text)
        text_box.delete('1.0', tk.END)
        text_box.insert('1.0', new_content)

    tk.Button(find_replace_window, text="Find", command=find_text, font=("Arial", 10)).grid(row=2, column=0, padx=4, pady=4)
    tk.Button(find_replace_window, text="Replace", command=replace_text, font=("Arial", 10)).grid(row=2, column=1, padx=4, pady=4)

# Add Find and Replace to the menu
edit_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))
edit_menu.add_command(label="Find and Replace", command=find_and_replace)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0, font=("Arial", 10))
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "MRR Software - Notebook\nVersion 1.0\nDeveloped by MRR Software"))
menu_bar.add_cascade(label="Help", menu=help_menu)

# Add the menu bar to the root window
root.config(menu=menu_bar)

# Create a toolbar
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Resize images to fit the buttons
button_size = 40  # Increased button size
icons = {}
icon_files = ["new", "open", "save", "cut", "copy", "paste", "undo", "redo"]
for icon in icon_files:
    img = Image.open(f"icons/{icon}.png")
    img = img.resize((button_size, button_size), Image.LANCZOS)
    icons[icon] = ImageTk.PhotoImage(img)

# Create toolbar buttons with resized images
tk.Button(toolbar, image=icons["new"], command=lambda: text_box.delete(1.0, tk.END), width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="New", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["open"], command=open_file, width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Open", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["save"], command=save_file, width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Save", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["cut"], command=lambda: text_box.event_generate("<<Cut>>"), width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Cut", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["copy"], command=lambda: text_box.event_generate("<<Copy>>"), width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Copy", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["paste"], command=lambda: text_box.event_generate("<<Paste>>"), width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Paste", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["undo"], command=text_box.edit_undo, width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Undo", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

tk.Label(toolbar, text=" ", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)  # Add spacing

tk.Button(toolbar, image=icons["redo"], command=text_box.edit_redo, width=button_size, height=button_size).pack(side=tk.LEFT, padx=2, pady=2)
tk.Label(toolbar, text="Redo", font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)

# Create a status bar
status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Function to count words
def count_words():
    text_content = text_box.get(1.0, tk.END)
    words = text_content.split()
    word_count = len(words)
    status_bar.config(text=f"Line: {text_box.index(tk.INSERT).split('.')[0]} | Column: {text_box.index(tk.INSERT).split('.')[1]} | Words: {word_count}")

# Update status bar with cursor position and word count
def update_status():
    row, col = text_box.index(tk.INSERT).split('.')
    text_content = text_box.get(1.0, tk.END)
    words = text_content.split()
    word_count = len(words)
    status_bar.config(text=f"Line: {row} | Column: {col} | Words: {word_count}")

# Function to update line numbers
def update_line_numbers():
    line_numbers = "\n".join(map(str, range(1, int(text_box.index('end').split('.')[0]))))
    line_number_bar.config(state='normal')
    line_number_bar.delete(1.0, tk.END)
    line_number_bar.insert(1.0, line_numbers)
    line_number_bar.config(state='disabled')

text_box.bind('<KeyRelease>', lambda event: update_status())
text_box.bind('<ButtonRelease>', lambda event: update_status())
text_box.bind('<KeyRelease>', lambda event: update_line_numbers())
text_box.bind('<ButtonRelease>', lambda event: update_line_numbers())

# Run the application
root.mainloop()
