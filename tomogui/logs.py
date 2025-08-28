import logging
import tkinter as tk
class Log:
    def __init__(self):
        self.logger = logging.getLogger('TKLogger')
        self.logger.setLevel(logging.INFO)

class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        self.text.configure(state='normal')
        self.text.insert(tk.END, msg + '\n', record.levelname)
        self.text.configure(state='disabled')