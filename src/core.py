from winreg import OpenKey, QueryValueEx, SetValueEx, HKEY_CURRENT_USER, KEY_READ, KEY_ALL_ACCESS, REG_SZ
from subprocess import call, check_output, Popen
from sys import platform
from os import getenv, makedirs


class Core:
    if platform == 'win32':
        path = getenv('USERPROFILE') + r'\Documents\SAMPFresh'

    def IsProcessRunning(self, process_name):
        return True if process_name in check_output("tasklist", universal_newlines=True) else False

    def StartProcess(self, args=[]):
        call(args)

    def OpenUrl(self, url):
        cmd = 'start ' + url
        Popen(cmd, shell=True)

    def SetKeyValue(self, Key, Subkey, name, value):
        result = OpenKey(Key, Subkey, 0, KEY_ALL_ACCESS)
        return SetValueEx(result, name, 0, REG_SZ, value)

    def GetKeyValue(self, Key, Subkey, name):
        result = OpenKey(Key, Subkey, 0, KEY_READ)
        return QueryValueEx(result, name)[0]

    def ChangePlayerName(self, new_name):
        try:
            self.SetKeyValue(HKEY_CURRENT_USER,
                             r'SOFTWARE\SAMP', 'PlayerName', new_name)
        except Exception:
            raise
        return new_name

    def GetPlayerName(self):
        try:
            name = self.GetKeyValue(
                HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName')
        except:
            name = False
        return name

    def GetSampPath(self):
        try:
            path = self.GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'gta_sa_exe')[
                :-10] + 'samp.exe'
        except:
            path = False
        return path

    def IsValidAddress(self, address):
        splitted = address.split(':')
        if len(splitted) != 2:
            return False
        return True

    def LoadServersData(self):
        lines = []
        try:
            file = open(f'{self.path}/servers.txt', 'r')
            lines = file.readlines()
            file.close()
        except Exception as e:
            pass
        return lines

    def SaveServersData(self, servers):
        if platform == 'win32':
            makedirs(self.path, exist_ok=True)
        file = open(f'{self.path}/servers.txt', 'w')
        for server in servers:
            if server:
                file.write(f'{server[0]},{server[1]}\n')
        file.close()
