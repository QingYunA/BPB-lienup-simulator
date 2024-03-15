import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from Ui_lineup import LineUpSimulator  # 导入你写的界面类


path = "./assets"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = LineUpSimulator(path=path)
    myWin.setMouseTracking(True)
    myWin.show()
    sys.exit(app.exec_())
