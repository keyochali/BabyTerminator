import cx_Freeze
import os
import sys
import os.path
import matplotlib

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR,'tcl','tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


base=None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("Beta1.py",base=base)]

cx_Freeze.setup(
    name = "BabyTerminator",
    options = {"build_exe":{"packages":["tkinter","cv2","serial","face_recognition","dlib","numpy"],
                            "include_files":["revan.jpeg",
                                             "keyo.jpg",
                                             "Godar.jpg",
                                             "Marwan.jpeg",
                                             "shape_predictor_68_face_landmarks.dat",
                                             "C:/Users/Yehya Chali/AppData/Local/Programs/Python/Python35-32/DLLs/tcl86t.dll",
                                             "C:/Users/Yehya Chali/AppData/Local/Programs/Python/Python35-32/DLLs/tk86t.dll"]}},
    version="0.01",
    description="just a baby terminator",
    executables=executables
    )
