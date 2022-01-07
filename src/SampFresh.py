# -*- coding: utf-8 -*-
# pyuic5 -o t.py t.ui

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from gui import Ui_MainWindow
from pypresence import Presence
from core import Core


class SampFresh(QMainWindow):
    gta_running = False
    player_name = samp_path = ''

    def __init__(self, app, client_id):
        super().__init__()
        self.app = app
        self.core = Core()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.presence = Presence(client_id)
        self.Initialize()

    def GetSampPath(self):
        self.samp_path = self.core.GetSampPath()
        return self.samp_path

    def GetPlayerName(self):
        self.player_name = self.core.GetPlayerName()
        return self.player_name

    def OnChangePlayerName(self, text):
        self.player_name = self.core.ChangePlayerName(new_name=text)

    def AddNewServer(self, hostname=None, address=False, savefile=True):
        if not address:
            address = self.ui.addressLine.text()
            print(address)
        if not self.core.IsValidAddress(address):
            return
        position = int(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.insertRow(position)
        self.ui.tableWidget.setItem(position, 0, QTableWidgetItem(
            hostname if hostname else 'Server'))
        self.ui.tableWidget.setItem(position, 1, QTableWidgetItem(address))
        if savefile:
            self.SaveServers()

    def LoadServers(self):
        servers = self.core.LoadServersData()
        if not servers:
            return
        for server in servers:
            if server != '\n':
                splitted = server.split(',')
                print(splitted)
                self.AddNewServer(
                    hostname=splitted[0], address=splitted[1], savefile=False)

    def SaveServers(self):
        table = self.ui.tableWidget
        data = []
        rows = table.rowCount()
        columns = table.columnCount()
        for row in range(rows):
            data.append([])
            for column in range(columns):
                field = table.item(row, column)
                data[row].append(field.text())
        self.core.SaveServersData(data)

    def SelectServer(self, row, column):
        address_object = self.ui.tableWidget.item(row, 1)
        if address_object:
            self.ui.tableWidget.item(row, 0).setSelected(True)
            self.ui.tableWidget.item(row, 1).setSelected(True)

    def DeleteServer(self, row):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        [self.ui.tableWidget.removeRow(index.row()) for index in indexes]
        self.SaveServers()

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

    def GetSelectedServer(self):
        indexes = self.ui.tableWidget.selectionModel().selectedRows()
        if not indexes:
            return False
        selected = indexes[0]
        address = self.ui.tableWidget.item(selected.row(), 1).text()
        return address

    def Connect(self):
        if not self.samp_path:
            return self.error('SA:MP not found', 'SA:MP is not installed on your machine.', 'Install SA:MP to continue.')
        if self.core.IsProcessRunning('gta_sa.exe'):
            return self.error('GTA process', 'GTA is currently running.', 'Close it to connect.')
        if not self.GetSelectedServer():
            self.error('Invalid server', "Can't connect to 'Empty' server.",
                       'Select a server to continue.', icon=QMessageBox.Warning)

        address = self.GetSelectedServer()

        if self.ui.discordCheckbox.isChecked():
            print('Executing discord rich presence..')
            self.presence.connect()
            self.presence.update(details="Playing in " + address)
       
        self.core.StartProcess([self.samp_path, address])


    def ConnectElements(self):
        # buttons
        self.ui.connectBtn.clicked.connect(self.Connect)
        self.ui.addBtn.clicked.connect(self.AddNewServer)
        self.ui.deleteBtn.clicked.connect(self.DeleteServer)

        # checkboxes
        self.ui.favServersCheckbox.setCheckable(False)
        # self.ui.discordCb.stateChanged.connect(self.connect_discord)
        # self.ui.favServersCheckbox.stateChanged.connect(self.favorite_servers)

        self.ui.nicknameLine.textChanged.connect(self.OnChangePlayerName)
        self.ui.tableWidget.cellClicked.connect(self.SelectServer)
        self.ui.actionGithub_repositoryh.triggered.connect(self.OpenGithubRepo)

    def OpenGithubRepo(self):
        self.core.OpenUrl('https://github.com/le01q/samp-fresh')

    def Initialize(self):
        self.ConnectElements()
        self.GetSampPath()
        self.LoadServers()
        if self.samp_path:
            self. ui.nicknameLine.setText(self.GetPlayerName())
        self.gta_running = self.core.IsProcessRunning('gta_sa.exe')
