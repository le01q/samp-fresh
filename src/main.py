# -*- coding: utf-8 -*-

from sys import argv, exit
from PyQt5.QtWidgets import QApplication
from sampfresh import SampFresh

if __name__ == "__main__":
    app = QApplication(argv)
    window = SampFresh(app, 929135097154768988)
    window.show()
    exit(app.exec_())
