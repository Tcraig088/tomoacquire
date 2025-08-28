import logging
import tkinter as tk
from tkinter import ttk
from .. import logs

class LoggingFrame(tk.LabelFrame, logs.Log):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text='Logging', padx=10, pady=10)
        logs.Log.__init__(self)
        self.text = tk.Text(self)
        self.text.pack(padx=2, pady=2)

        handler = logs.TextHandler(self.text)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        # Set the color of the text
        self.text.tag_config('DEBUG', foreground='green')
        self.text.tag_config('INFO', foreground='black')
        self.text.tag_config('WARNING', foreground='orange')
        self.text.tag_config('ERROR', foreground='red')
        self.text.tag_config('CRITICAL', foreground='red')
        
class BaseFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Logger = LoggingFrame(self)
        self.Logger.pack()
        self.pack(fill=tk.X)