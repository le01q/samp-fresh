from winreg import OpenKey, QueryValueEx, SetValueEx, HKEY_CURRENT_USER, KEY_READ, KEY_ALL_ACCESS, REG_SZ
from subprocess import call, check_output
from pypresence import Presence
from time import sleep

class SampFresh:
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
        new_name = str(input("New name: "))
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
        
        print('Current nickname: ', self.player_name)
        option = str(input('Wanna change your nickname? (Yes or No)'))
        if 'y' in option.lower():
            self.ChangePlayerName()

        self.SetAddress()
        self.StartSamp()

        self.presence.connect()

        while self.gta_running:
            self.gta_running = self.IsGtaRunning()
            self.presence.update(details="Playing in" + self.address)
            sleep(15)

        self.presence.close()


if __name__ == '__main__':
    client = SampFresh(':D')
    client.run()