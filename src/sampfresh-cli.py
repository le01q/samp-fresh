from winreg import OpenKey, QueryValueEx, SetValueEx, HKEY_CURRENT_USER, KEY_READ, KEY_ALL_ACCESS, REG_SZ
from socket import gethostbyname, socket, AF_INET, SOCK_DGRAM
from subprocess import call, check_output
from pypresence import Presence
from colorama import init, Fore
from constants import *
import time
import os

class SampFresh:

    def __init__(self, client_id):
        self.samp_path = self.player_name = self.host = self.address = None
        self.port = 7777
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.query_header = b'SAMP'
        self.gta_running = self.samp_running = False
    
    def IsProcessRunning(self, process_name):
        return True if process_name in check_output("tasklist", universal_newlines=True) else False

    def SetKeyValue(self, Key, Subkey, name, value):
        result = OpenKey(Key, Subkey, 0, KEY_ALL_ACCESS)
        return SetValueEx(result, name, 0, REG_SZ, value)
    
    def GetKeyValue(self, Key, Subkey, name):
        result = OpenKey(Key, Subkey, 0, KEY_READ)
        return QueryValueEx(result, name)[0]

    def GetSampPath(self):
        self.samp_path = self.GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'gta_sa_exe')[:-10] + 'samp.exe'
        return self.samp_path
    
    def GetPlayerName(self):
        self.player_name = self.GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName')
        return self.player_name

    def ChangePlayerName(self, new_name):
        try:
            self.SetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName', new_name)
        except Exception:
            raise
        self.player_name = new_name
        
    def IpAddressEvent(self):
        host, port = self.InputIp()
        self.address = f'{host}:{port}'
    
    def InputIp(self):
        while True:
            try:
                ip = str(input("[SA:MP Fresh CLI] Specify the server IP address here: "))
                host, port = ip.split(':')[0], ip.split(':')[1]
                return host, port
            except IndexError:
                self.message(Fore.RED, "[SA:MP Fresh CLI | ERROR] Please specify a valid IP address.")
    
    def StartProcess(self, args=[]):
        call(args)
        self.gta_running = True

    def message(self, color, msg):
        print(color + msg + Fore.RESET)

    def Initialize(self):
        init(autoreset=True)
        if not self.GetSampPath():
            raise Exception("Can't get SA-MP path")
        if not self.GetPlayerName():
            raise Exception("Can't get player name")
        return
    
    def DisplayBanner(self):
        self.message(Fore.RESET, MAIN)
        self.message(Fore.GREEN, "[SA:MP Fresh CLI] This is your current nickname in SA:MP: <" + self.player_name + ">")
    
    def InputPlayerName(self):
        while True:
            name = str(input("[SA:MP Fresh CLI] Write your new nickname that you will use: "))
            if 4 <= len(name) < 24:
                return name
        
    def PlayerNameEvent(self):
        option = str(input("[SA:MP Fresh CLI] You want change your current nickname? (Y/N): "))
        if 'y' in option.lower():
            self.ChangePlayerName(self.InputPlayerName())

    def CommandLineRichPresence(self):
        self.client_id = "943925992550981652"
        RPC = Presence(self.client_id)
        RPC.connect()
        
        while True:
            nickname = self.player_name
            server = self.address

            RPC.update(
                state="Server IP: " + server, 
                details="Nickname: " + nickname, 
                large_image="sampfresh_cli", 
                large_text="Playing from CLI",
            )
            time.sleep(15)

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

            while self.gta_running:
                self.CommandLineRichPresence()
                self.gta_running = self.IsProcessRunning('gta_sa.exe')

        except KeyboardInterrupt:
            return

if __name__ == '__main__':
    client = SampFresh(':D')
    client.run()
