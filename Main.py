"""
    Author: j1193
    Time: 2020/11/24 21:24
"""

import sys
from PyQt5.QtWidgets import QApplication

from PaintWindow import PaintWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pw = PaintWindow()
    pw.show()
    sys.exit(app.exec_())
