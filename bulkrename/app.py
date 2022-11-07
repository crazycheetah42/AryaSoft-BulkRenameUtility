# -*- coding: utf-8 -*-
# bulkrename/app.py

import sys
from PyQt5.QtWidgets import QApplication
from .views import Window
import qdarkstyle

def main():
    import darkdetect
    if darkdetect.isDark() == True:
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        win = Window()
        win.show()
        sys.exit(app.exec())
    else:
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec())