from PyQt5.QtCore import QThread
from core import Core

class FreshWorker(QThread):
    gta_running = True
    core = Core()
    def run(self):
        while self.gta_running:
            if not self.core.IsProcessRunning('gta_sa.exe'):
                self.gta_running = False
        return
