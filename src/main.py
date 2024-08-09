import os
import sys
# check if run as script or exe --> https://pyinstaller.org/en/stable/runtime-information.html
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    ROOT = sys._MEIPASS
else:
    ROOT = os.path.dirname(__file__)
# import sys
# sys.path
# sys.path.append(ROOT)
os.environ["PATH"] = os.environ["PATH"] + os.pathsep + ROOT
from subsai.main import SubsAI
from subsai.configs import AVAILABLE_MODELS
from platformdirs import user_data_dir
from typing import Tuple

import tkinter as tk
from tkinter import ttk, filedialog


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas widget
        canvas = tk.Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a vertical scrollbar linked to the canvas
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas for the widgets
        self.scrollable_frame = ttk.Frame(canvas)
        
        # Place the inner frame in the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the scroll event to the mousewheel for easier scrolling
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

    def _bind_to_mousewheel(self, event):
        self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.scrollable_frame.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.scrollable_frame.yview_scroll(int(-1*(event.delta/120)), "units")



class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subs AI")
        self.elements = {}
        self.scrollable_frame = None
        self.open_button = None
        self.current_model = None

        # # Create a button
        # self.button = tk.Button(root, text="Click Me", command=self.on_button_click)
        # self.button.pack(pady=10)

        # Create a label
        self.label = tk.Label(root, text="Select a model:")
        self.label.pack(pady=20)

        # Create a dropdown menu
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(root, textvariable=self.dropdown_var)
        self.dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.dropdown.current(3)  # Set default value
        self.dropdown.pack(pady=10)

        # Bind the selection event to a method
        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_click)

        self.label2 = tk.Label(root, text="Model specific config:")
        self.label2.pack(pady=20)

        self.on_dropdown_click(None)

    def clear_elements(self):
        for selected_option in self.elements:
            for key in self.elements[selected_option]:
                for element in ['label','dropdown','entry','checkbutton']:
                    if element in self.elements[selected_option][key]:
                        self.elements[selected_option][key][element].destroy()
        if self.scrollable_frame:
            self.scrollable_frame.destroy()
        if self.open_button:
            self.open_button.destroy()

    def open_file(self):
        # Open a file dialog and select a file
        file_path = filedialog.askopenfilename()

        config = {}
        for key in self.elements[self.current_model]:
            if self.elements[self.current_model][key]['type'] not in [dict,Tuple]:
                config[key] = self.elements[self.current_model][key]['var'].get()
                if config[key] == 'None' or config[key] is None or config[key] == '':
                    del config[key]
                elif self.elements[self.current_model][key]['type'] is not list:
                    config[key] = self.elements[self.current_model][key]['type'](config[key])
            else:
                config[key] = self.elements[self.current_model][key]['var']

        print(file_path)
        subs_ai = SubsAI()
        model = subs_ai.create_model(self.current_model, config)
        subs = subs_ai.transcribe(file_path, model)
        print(subs.to_string(format_='srt'))

        # Create a Frame to hold the Text widget and Scrollbar
        frame = tk.Frame(self.root)
        frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Create a Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget with vertical scrolling
        result_textbox = tk.Text(frame, font=('Arial', 12), yscrollcommand=scrollbar.set, wrap=tk.WORD)
        result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, subs.to_string(format_='srt'))

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

    def on_dropdown_click(self, event):
        print(event)

        self.clear_elements()

        selected_option = self.dropdown_var.get()
        schema = AVAILABLE_MODELS[selected_option]['config_schema']

        if selected_option not in self.elements:
            self.elements[selected_option] = {}

        self.scrollable_frame = ScrollableFrame(root)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        sframe = self.scrollable_frame.scrollable_frame

        for key in schema:
            if key not in self.elements[selected_option]:
                self.elements[selected_option][key] = {}

            current_option = self.elements[selected_option][key]
            current_option['type'] = schema[key]['type']

            if schema[key]['type'] == list:
                current_option['label'] = tk.Label(sframe, text=key)
                current_option['label'].pack(pady=1)
                if 'var' not in current_option:
                    current_option['var'] = tk.StringVar(value=schema[key]['default'])
                current_option['dropdown'] = ttk.Combobox(sframe,textvariable=current_option['var'])
                current_option['dropdown']['values'] = schema[key]['options']
                dropdown_value = current_option['var'].get()
                if dropdown_value == '' or dropdown_value == 'None':
                    dropdown_value = None
                current_option['dropdown'].current(schema[key]['options'].index(dropdown_value))
                current_option['dropdown'].pack(pady=10)
            elif schema[key]['type'] in [str,int,float]:
                current_option['label'] = tk.Label(sframe,text=key, font=('Arial', 12))
                current_option['label'].pack()
                if 'var' not in current_option:
                    current_option['var'] = tk.StringVar(value=schema[key]['default'])
                current_option['entry'] = tk.Entry(sframe,textvariable=current_option['var'])
                current_option['entry'].pack(padx=5, fill=tk.X, expand=True)
            elif schema[key]['type'] == bool:
                if 'var' not in current_option:
                    current_option['var'] = tk.BooleanVar(value=schema[key]['default'])
                current_option['checkbutton'] = tk.Checkbutton(sframe, text=key, variable=current_option['var'])
                current_option['checkbutton'].pack(pady=10)
            # elif schema[key]['type'] == float:
            #     current_option['label'] = tk.Label(sframe,text=key, font=('Arial', 12))
            #     current_option['label'].pack()
            #     if 'var' not in current_option:
            #         current_option['var'] = tk.DoubleVar(value=schema[key]['default'])
            #     current_option['entry'] = tk.Entry(sframe,textvariable=current_option['var'])
            #     current_option['entry'].pack(padx=5, fill=tk.X, expand=True)
            # elif schema[key]['type'] == int:
            #     current_option['label'] = tk.Label(sframe,text=key, font=('Arial', 12))
            #     current_option['label'].pack()
            #     if 'var' not in current_option:
            #         current_option['var'] = tk.IntVar(value=schema[key]['default'])
            #     current_option['entry'] = tk.Entry(sframe,textvariable=current_option['var'])
            #     current_option['entry'].pack(padx=5, fill=tk.X, expand=True)
            elif schema[key]['type'] == dict or schema[key]['type'] == Tuple:
                current_option['var'] = schema[key]['default']
                # current_option['label'] = tk.Label(sframe,text=key, font=('Arial', 12))
                # current_option['label'].pack()
                # if 'var' not in current_option:
                #     current_option['var'] = tk.StringVar(value=str(schema[key]['default']))
                # current_option['entry'] = tk.Entry(sframe,textvariable=current_option['var'])
                # current_option['entry'].pack(padx=5, fill=tk.X, expand=True)

        self.current_model = selected_option

        # Create and place the file open button
        self.open_button = tk.Button(root, text="Open and transcribe video", command=self.open_file, font=('Arial', 14))
        self.open_button.pack(pady=10)

    def setup_env(self):
        appname = "SubsAItk"
        appauthor = "lotka"

        self.user_data_dir = user_data_dir(appname, appauthor)
        self.data_dir = os.path.dirname(self.user_data_dir)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        if not os.path.exists(self.user_data_dir):
            os.mkdir(self.user_data_dir)

# Create the main window
root = tk.Tk()

# Create an instance of the MyApp class
app = MyApp(root)

# Run the main event loop
root.mainloop()
