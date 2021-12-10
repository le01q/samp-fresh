from winreg import OpenKey, QueryValueEx, SetValueEx, HKEY_CURRENT_USER, KEY_READ, KEY_ALL_ACCESS, REG_SZ
from subprocess import call, check_output
from pypresence import Presence
from time import sleep
from colorama import init, Fore

AUTHORS = "le01q and manucrabral"

LOGO = f'''
{Fore.GREEN}
.d8888b.         d8888 888b     d888  8888888b.      8888888888                       888      
d88P  Y88b      d88888 8888b   d8888 888   Y88b      888                              888      
Y88b.          d88P888 88888b.d88888 888    888      888                              888      
 "Y888b.      d88P 888 888Y88888P888 888   d88P      8888888 888d888 .d88b.  .d8888b  88888b.  
    "Y88b.   d88P  888 888 Y888P 888 8888888P"       888     888P"  d8P  Y8b 88K      888 "88b 
      "888  d88P   888 888  Y8P  888 888             888     888    88888888 "Y8888b. 888  888 
Y88b  d88P d8888888888 888   "   888 888             888     888    Y8b.          X88 888  888 
 "Y8888P" d88P     888 888       888 888             888     888     "Y8888   88888P' 888  888
{Fore.RESET}

Authors: le01q & manucabral
'''

class SampFresh:
    print(LOGO)

    def __init__(self, client_id):
        self.samp_path = None
        self.player_name = None
        self.host = None
        self.port = 7777
        self.address = None
        self.presence = Presence(client_id)
        self.gta_running = False
        self.samp_running = False

    def IsProcessRunning(self, process_name):
        return True if process_name in check_output("tasklist", universal_newlines=True) else False

    def SetKetValue(self, Key, Subkey, name, value):
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

    def ChangePlayerName(self):
        new_name = str(input("[!] New name: "))
        self.SetKetValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName', new_name)
        self.player_name = new_name
        
    def SetAddress(self):
        ip = str(input("IP: "))
        self.host, self.port = ip.split(':')[0], ip.split(':')[1]
        self.address = ip

    def StartSamp(self):
        args = [self.samp_path, self.address]
        print(self.address)
        call(args)
    
    def Init(self):
        return not self.IsProcessRunning('gta_sa.exe') and not self.IsProcessRunning('samp.exe')

    def run(self):
        if not self.Init():
            print("Can't execute")
            return
        
        self.GetPlayerName()
        self.GetSampPath()

        print('[>] Current nickname: ', self.player_name)
        option = str(input('[?] Wanna change your nickname? (Yes or No): '))
        if 'Yes' in option.lower():
            self.ChangePlayerName()

        self.SetAddress()
        self.StartSamp()

        self.presence.connect()

        while self.gta_running:
            self.gta_running = self.IsGtaRunning()
            self.presence.update(details="Playing in " + self.address)
            sleep(15)

        self.presence.close()


if __name__ == '__main__':
    client = SampFresh('918675263980724264')
    client.run()