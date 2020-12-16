import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class QLineEditDemo(QWidget):
    def __init__(self):
        super(QLineEditDemo, self).__init__()
        self.initUI

    def initUI(self):
        edit1=QLineEdit()
        edit1.setValidator(QValidator())
        edit1.setMaxLength(4)
        edit1.setAlignment(Qt.AlignRight)
        edit1.setFont(QFont('Arial',20))

        formLayout=QFormLayout()
        formLayout.addRow('整数效验',edit1)

        self.setLayout(formLayout)
        self.setWindowTitle('QLineEdit综合案例')

if __name__=='__main__':
    app=QApplication(sys.argv)
    main=QLineEditDemo()
    main.show()
    sys.exit(app.exec())