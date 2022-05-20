from PyQt5 import QtWidgets

from main import Form_controller

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Form_controller()
    window.show()

    sys.exit(app.exec_())
