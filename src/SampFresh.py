# -*- coding: utf-8 -*-
# pyuic5 -o t.py t.ui

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from requests import get, exceptions as rexceptions
from gui import Ui_MainWindow
from pypresence import Presence, exceptions as pexceptions
from core import Core
from freshworker import FreshWorker
from time import time, sleep
from threading import Thread


class SampFresh(QMainWindow):
    gta_running = False
    player_name = samp_path = address = hostname = ''

    def __init__(self, app, client_id):
        super().__init__()
        self.app = app
        self.core = Core()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.client_id = client_id 
        self.Initialize()

    def closeEvent(self, event):
        if self.gta_running and self.presence:
            self.presence.close()
        event.accept()
        
    def GetSampPath(self):
        self.samp_path = self.core.GetSampPath()
        return self.samp_path

    def GetPlayerName(self):
        self.player_name = self.core.GetPlayerName()
        return self.player_name

    def OnChangePlayerName(self, text):
        self.player_name = self.core.ChangePlayerName(new_name=text)

    def AddNewServer(self, hostname=None, address=False, savefile=True):
        if not hostname:
            hostname = self.ui.hostnameLine.text() if self.ui.hostnameLine.text() else 'Server'
        if not address:
            address = self.ui.addressLine.text()
        if not self.core.IsValidAddress(address):
            return
        position = int(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.insertRow(position)
        self.ui.tableWidget.setItem(position, 0, QTableWidgetItem(
            hostname if hostname else 'Server'))
        self.ui.tableWidget.setItem(position, 1, QTableWidgetItem(address))
        if savefile:
            self.SaveFavoriteServers()
    
    def LoadSampFavoriteServers(self):
        servers = self.core.LoadSampFavoriteServers()
        if not servers:
            return
        for server in servers:
            self.AddNewServer(hostname=server[0], address=f'{server[1]}:{server[2]}', savefile=False)
    
    def LoadServers(self):
        self.ClearAllServers()
        if self.SampFavoritesEnabled():
            self.LoadSampFavoriteServers()
        else:
            self.LoadFavoriteServers()
        
    def LoadFavoriteServers(self):
        servers = self.core.LoadFavoriteServers()
        if not servers:
            return
        for server in servers:
            if server != '\n':
                splitted = server.split(',')
                self.AddNewServer(
                    hostname=splitted[0], address=splitted[1], savefile=False)
    
    def ClearAllServers(self):
        self.ui.tableWidget.setRowCount(0)

    def SaveConfiguration(self):
        self.LoadServers()
        if self.SampFavoritesEnabled():
            self.ui.addBtn.setEnabled(False)
            self.ui.deleteBtn.setEnabled(False)
        else:
            self.ui.addBtn.setEnabled(True)
            self.ui.deleteBtn.setEnabled(True)
        data = {
            'discordrpc': self.DiscordEnabled(),
            'sampfavorites': self.SampFavoritesEnabled(), 
        }
        self.core.SaveConfig(**data)

    def SaveFavoriteServers(self):
        table = self.ui.tableWidget
        data = []
        rows = table.rowCount()
        columns = table.columnCount()
        for row in range(rows):
            data.append([])
            for column in range(columns):
                field = table.item(row, column)
                data[row].append(field.text())
        self.core.SaveFavoriteServers(data)

    def SelectServer(self, row, column):
        address_object = self.ui.tableWidget.item(row, 1)
        if address_object:
            self.ui.tableWidget.item(row, 0).setSelected(True)
            self.ui.tableWidget.item(row, 1).setSelected(True)

    def DeleteServer(self, row):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        [self.ui.tableWidget.removeRow(index.row()) for index in indexes]
        self.SaveFavoriteServers()

    def error(self, title='Error', text='An error ocurred', info=None, icon=QMessageBox.Critical):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setStyleSheet('color:white;')
        msg.setWindowTitle(title)
        msg.setText(text)
        if info:
            msg.setInformativeText(info)
        msg.show()
        return

    def SampFavoritesEnabled(self):
        return self.ui.favServersCheckbox.isChecked()

    def DiscordEnabled(self):
        return self.ui.discordCheckbox.isChecked()

    def GetSelectedServer(self):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        if not indexes:
            return False
        selected = indexes[0]
        self.address = self.ui.tableWidget.item(selected.row(), 1).text()
        self.hostname = self.ui.tableWidget.item(selected.row(), 0).text()
        return self.address, self.hostname

    def ConnectRichPresence(self):
        try:
            self.presence = Presence(self.client_id)
            self.presence.connect()
            data = {
                'state': self.GetPlayerName(),
                'details': self.address,
                'start': time(),
                'large_image': self.core.GetServerLogo(self.address) if self.core.IsSpecialAddress(self.address) else 'sampfresh',
                'small_image': 'sampfresh',
                'small_text': 'SA:MP Fresh',
                'large_text': self.hostname,
                'buttons': [
                    {
                        'label': 'Add server to favorites',
                        'url': 'samp://' + self.address
                    },
                    {
                        'label': 'Download Launcher',
                        'url': 'https://le01q.github.io/samp-fresh/'
                    }
                ]
            }
            self.presence.update(**data)
        except pexceptions.DiscordNotFound:
            return self.error('Discord Error', 'Discord process not found in your PC ...', 'Open or install Discord application.')
        except pexceptions.InvalidPipe:
            return self.error('Discord Error', 'Discord Pipe not found', 'Please open Discord app')
        except pexceptions.ServerError:
            return self.error('Discord Error', 'Invalid SA:MP Ip Address', "Can't run Rich Presence")
    
    def Connect(self):
        if not self.samp_path:
            return self.error('SA:MP Not Found', 'SA:MP is not installed on your machine.', 'Install SA:MP to continue.')

        if self.core.IsProcessRunning('gta_sa.exe'):
            return self.error('GTA Process', 'GTA is currently running.', 'Close it to connect.')

        if not self.GetSelectedServer():
            return self.error('Invalid Server', "Can't connect to 'Empty' server.", 'Select a server to continue.', icon=QMessageBox.Warning)

        self.address, self.hostname = self.GetSelectedServer()

        self.core.StartProcess([self.samp_path, self.address])
        self.gta_running = True

        if self.DiscordEnabled():
           self.ConnectRichPresence()

        self.worker = FreshWorker()
        self.worker.start()
        self.ui.discordCheckbox.setEnabled(False)
        self.worker.finished.connect(self.OnGTAClose)

    def OnGTAClose(self):
        self.gta_running = False
        self.ui.discordCheckbox.setEnabled(True)
        if self.DiscordEnabled():
            self.presence.close()
        
    def ConnectElements(self):
        # buttons
        self.ui.connectBtn.clicked.connect(self.Connect)
        self.ui.addBtn.clicked.connect(self.AddNewServer)
        self.ui.deleteBtn.clicked.connect(self.DeleteServer)

        # checkboxes
        self.ui.favServersCheckbox.stateChanged.connect(self.SaveConfiguration)
        self.ui.discordCheckbox.stateChanged.connect(self.SaveConfiguration)

        self.ui.nicknameLine.textChanged.connect(self.OnChangePlayerName)
        self.ui.tableWidget.cellClicked.connect(self.SelectServer)
        self.ui.actionGithub_repositoryh.triggered.connect(self.OpenGithubRepo)

    def OpenGithubRepo(self):
        self.core.OpenUrl('https://github.com/le01q/samp-fresh')

    def LoadConfig(self):
        data = self.core.LoadConfig()
        if not data:
            return
        self.ui.discordCheckbox.setChecked(data['discordrpc'])
        self.ui.favServersCheckbox.setChecked(data['sampfavorites'])

    def CheckUpdates(self):
        try:
            res = get('https://api.github.com/repos/le01q/samp-fresh/releases')
            res.raise_for_status()
        except rexceptions.ConnectionError:
            return self.error('Connection Error', "Can't connect to internet ...", 'Please verify your internet connection.')
        except:
            return self.error('SA:MP Fresh Updates', "Can't check new updates", icon=QMessageBox.Critical)
        versions = []
        for key in res.json():
            versions.append(key['tag_name'])
        if versions[0] != self.core.VERSION:
            return self.error('SA:MP Fresh Updates', f"A new update {versions[0]} is available", f'Your current version is {self.core.VERSION}', icon=QMessageBox.Warning)

    def Initialize(self):
        self.ConnectElements()
        self.GetSampPath()
        self.LoadConfig()
        self.CheckUpdates()
        self.LoadServers()
        if self.samp_path:
            self. ui.nicknameLine.setText(self.GetPlayerName())
        self.gta_running = self.core.IsProcessRunning('gta_sa.exe')
        self.ui.versionLabel.setText(f'Version: {self.core.VERSION}')
