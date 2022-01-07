from winreg import OpenKey, QueryValueEx, SetValueEx, HKEY_CURRENT_USER, KEY_READ, KEY_ALL_ACCESS, REG_SZ
from socket import gethostbyname, socket, AF_INET, SOCK_DGRAM
from subprocess import call, check_output
from pypresence import Presence
from time import sleep
from colorama import init, Fore
from constants import *

class SampFresh:

    def __init__(self, client_id):
        self.samp_path = self.player_name = self.host = self.address = None
        self.port = 7777 # default port
        self.presence = Presence(client_id)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.query_header = b'SAMP'
        self.gta_running = self.samp_running = False
    
    def IsProcessRunning(self, process_name):
        return True if process_name in check_output("tasklist", universal_newlines=True) else False

    def SetKetValue(self, Key, Subkey, name, value):
        result = OpenKey(Key, Subkey, 0, KEY_ALL_ACCESS)
        rewwturn SetValueEx(result, name, 0, REG_SZ, value)
    
    def GetKeyValue(self, Key, Subkey, name):
        rewwwwwwwwwsult = OpenKey(Key, Subkey, 0, KEY_READ)
        return QueryValueEx(result, name)[0]

    def GetSampPath(self):
        self.samp_path = self.GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'gta_sa_exe')[:-10] + 'samp.exe'
        return self.samp_path
    
    def GetPlayerName(self):
        self.player_name = self.GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName')
        return self.player_name

    def ChangePlayerName(self, new_name):
        try:
            self.SetKetValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName', new_name)
        except Exception:
            raise
        self.player_name = new_name
        
    def IpAddressEvent(self):
        host, port = self.InputIp()
        self.address = f'{host}:{port}'
    
    def InputIp(self):
        while True:
            try:
                ip = str(input("[>] Server IP: "))
                host, port = ip.split(':')[0], ip.split(':')[1]
                return host, port
            except IndexError:
                self.message(Fore.RED, "Invalid IP, example: 192.56.67.8:7777")
    
    def StartProcess(self, args=[]):
        call(args)
        self.gta_running = True

    def message(self, color, msg):
        print(color + msg + Fore.RESET)

    def Initialize(self):
        init()
        if not self.GetSampPath():
            raise Exception("Can't get SA-MP path")
        if not self.GetPlayerName():
            raise Exception("Can't get player name")
        return
        #return not self.IsProcessRunning('gta_sa.exe') and not self.IsProcessRunning('samp.exe')
    
    def DisplayBanner(self):
        self.message(Fore.GREEN, LOGO)
        self.message(Fore.YELLOW, "[>] Current nickname: " + self.player_name)
    
    def InputPlayerName(self):
        while True:
            name = str(input('[>] New name: '))
            if 4 <= len(name) < 24:
                return name
        
    def PlayerNameEvent(self):
        option = str(input('[?] Wanna change your nickname? (Yes or No): '))
        if 'y' in option.lower():
            self.ChangePlayerName(self.InputPlayerName())

    def run(self):
        try:
            try:
                self.Initialize()
            except Exception as e:
                return self.message(Fore.RED, e)

            self.DisplayBanner()
            self.PlayerNameEvent()
            self.IpAddressEvent()

            self.StartProcess([self.samp_path, self.address])

            self.presence.connect()

            while self.gta_running:
                self.gta_running = self.IsProcessRunning('gta_sa.exe')
                self.presence.update(details="Playing in " + self.address)
                sleep(15)

            self.presence.close()

        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    client = SampFresh(':D')
    client.run()