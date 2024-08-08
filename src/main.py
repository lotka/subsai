import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog
import os

from subsai.main import SubsAI

from platformdirs import user_data_dir
appname = "SubsAItk"
appauthor = "lotka"

USER_DATA_DIR = user_data_dir(appname, appauthor)
DATA_DIR = os.path.dirname(USER_DATA_DIR)

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

if not os.path.exists(USER_DATA_DIR):
    os.mkdir(USER_DATA_DIR)

def open_file():
    # Open a file dialog and select a file
    file_path = filedialog.askopenfilename()
    
    if file_path:
        # Get the file size
        try:
            subs_ai = SubsAI()
            model = subs_ai.create_model('API/openai/whisper', {'language': language_var.get(), 'api_key': api_key_var.get()})
            result_textbox.insert(tk.END, 'Processing {}...\n'.format(file_path))
            subs = subs_ai.transcribe(file_path, model)
            result_textbox.delete(1.0, tk.END)
            result_textbox.insert(tk.END, subs.to_string(format_='srt'))
        except Exception as e:
            result_textbox.insert(tk.END, 'ERROR\n')
            result_textbox.insert(tk.END, str(e))

    else:
        result_textbox.delete(1.0, tk.END)  # Clear previous content

# Create the main window
root = tk.Tk()
root.title("Subs AI")

# Set the size of the window (e.g., 400x300 pixels)
root.geometry("400x600")

def get_defaults(name):
    fname = os.path.join(USER_DATA_DIR,name)
    if os.path.exists(fname):
        with open(fname,'r') as f:
            return f.read()
    else:
        with open(fname,'w') as f:
            f.write('')


def create_remembered_field(name):
    def on_text_change(*args):
        fname = os.path.join(USER_DATA_DIR,name)
        if os.path.exists(fname):
            with open(fname,'w') as f:
                print(fname)
                f.write(var.get())
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.X, padx=10, pady=5)

    label = tk.Label(frame, text=name, font=('Arial', 12))
    label.pack(side=tk.LEFT, padx=5)

    var = tk.StringVar(value=get_defaults(name))
    var.trace_add('write',on_text_change)

    field = tk.Entry(frame, textvariable=var)
    field.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    return var

api_key_var = create_remembered_field('api_key')
language_var = create_remembered_field('language')


# Create and place the file open button
open_button = tk.Button(root, text="Open File", command=open_file, font=('Arial', 14))
open_button.pack(pady=10)

# Create a Frame to hold the Text widget and Scrollbar
frame = tk.Frame(root)
frame.pack(pady=5, fill=tk.BOTH, expand=True)

# Create a Scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Text widget with vertical scrolling
result_textbox = tk.Text(frame, font=('Arial', 12), yscrollcommand=scrollbar.set, wrap=tk.WORD)
result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the Scrollbar to work with the Text widget
scrollbar.config(command=result_textbox.yview)

def save_to_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".srt",
        filetypes=[("Subtitle file", "*.srt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(result_textbox.get("1.0", "end-1c"))
        print(f"Saved string to: {file_path}")

# Add the Save button at the bottom of the window
save_button = tk.Button(root, text="Save to File", command=save_to_file)
save_button.pack(side=tk.BOTTOM, pady=10)

# Run the application
root.mainloop()