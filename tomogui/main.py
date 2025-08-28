
from tomogui.controllers import base


if __name__ == "__main__":
    #pythoncom.CoUninitialize()
    #pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    app = base.Controller()
    app.view.mainloop()