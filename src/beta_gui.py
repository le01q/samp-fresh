from winreg import OpenKey, QueryValueEx, SetValueEx, HKEY_CURRENT_USER, KEY_READ, KEY_ALL_ACCESS, REG_SZ 
from subprocess import call, check_output
from os import path
import tkinter as tk
from tkinter import ttk

SIZE = "800x600"
WIDTH, HEIGHT = 800, 600
TITLE = "SA:MP Fresh"
DARK_COLOR = "#202124"
DEFAULT_FONT = ('san-serf', 20)

class SampFresh:
    def __init__(self, root):
        self.root = root
        self.servers = []
        self.servers_frame = None
        self.input_player_name = self.input_server_ip = None

    def __CreateButton(self, x, y, text, callback):
        btn = tk.Button(self.root, text=text, bd=0, font=DEFAULT_FONT, fg="white", bg="GREEN", height=1, width=10, command=callback)
        btn.place(x=x, y=y)

    def __CreateInput(self, x, y, reference=None, default_value=""):
        entry = tk.Entry(self.root, width=20, justify="center", font=DEFAULT_FONT)
        entry.insert(tk.END, default_value)
        entry.place(x=x, y=y)
        return entry

    def __CreateLabel(self, x, y, text):
        label = tk.Label(self.root, text=text, font=DEFAULT_FONT, fg="WHITE")
        label['background'] = DARK_COLOR
        label.place(x=x, y=y)

    def __SetKeyValue(self, Key, Subkey, name, value):
        result = OpenKey(Key, Subkey, 0, KEY_ALL_ACCESS)
        return SetValueEx(result, name, 0, REG_SZ, value)
    
    def __GetKeyValue(self, Key, Subkey, name):
        result = OpenKey(Key, Subkey, 0, KEY_READ)
        return QueryValueEx(result, name)[0]
    
    def GetFavoriteServers(self):
        data = []
        with open(path.expanduser(r'~\Documents\GTA San Andreas User Files\SAMP\USERDATA.DAT'), "rb") as f:
            f.seek(8) # header: SAMP, 1
            servers_count = int.from_bytes(f.read(4), 'little')
            count = 0
            while count < servers_count:
                ip_len = int.from_bytes(f.read(4), 'little')
                server_ip = f.read(ip_len).decode()
                server_port = int.from_bytes(f.read(4), 'little')
                name_len = int.from_bytes(f.read(4), 'little')
                server_name = f.read(name_len).decode('unicode_escape')
                data.append((server_name, server_ip, server_port))
                f.read(8)
                count += 1
        return data
    
    def GetSampPath(self):
        self.samp_path = self.__GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'gta_sa_exe')[:-10] + 'samp.exe'
        return self.samp_path
    
    def GetPlayerName(self):
        self.player_name = self.__GetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName')
        return self.player_name

    def StartProcess(self, args=[]):
        call(args)
        self.gta_running = True

    def Connect(self, event):
        item = self.servers_tree.selection()
        print(self.servers_tree.item(item, "values")[0])

    def ChangeIpInput(self, event):
        item = self.servers_tree.selection()
        if not item:
            return
        address = self.servers_tree.item(item, "values")[1]
        ip = self.servers_tree.item(item, "values")[2]
        self.input_server_ip.delete(0, tk.END)
        self.input_server_ip.insert(tk.END, f'{address}:{ip}')

    def EventConnect(self):
        name = self.input_player_name.get()
        print(name)
        try:
            self.__SetKeyValue(HKEY_CURRENT_USER, r'SOFTWARE\SAMP', 'PlayerName', name)
        except Exception:
            raise
    
    def AddServersInFrame(self):
        for i in range(len(self.servers)):
            self.servers_tree.insert("", tk.END, values=self.servers[i])
        self.servers_tree.bind("<Double-1>", self.Connect)
        self.servers_tree.bind("<Button-1>", self.ChangeIpInput)

    def __CreateServersTree(self):
        self.servers_frame = tk.Frame(self.root, width=100, height=100, background="bisque")
        self.servers_frame.pack(fill=None, expand=False)
        self.servers_frame.place(x=10, y=150)
        ttk.Style().configure('Treeview', rowheight=40)
        self.servers_tree = ttk.Treeview(self.servers_frame, style="Treeview", columns=('server_name','server_address', 'server_port'))
        self.servers_tree.column("#0", width=0,  stretch=tk.NO)
        self.servers_tree.column("server_name", anchor=tk.CENTER, width=280)
        self.servers_tree.column("server_port", anchor=tk.CENTER, width=60)
        self.servers_tree.column("server_address", anchor=tk.CENTER, width=160)
        self.servers_tree.heading("server_name",text="Hostname",anchor=tk.CENTER)
        self.servers_tree.heading("server_port",text="Port",anchor=tk.CENTER)
        self.servers_tree.heading("server_address",text="Address",anchor=tk.CENTER)
        self.servers_tree.pack()

    def __gui_initialize(self):
        self.root.geometry(SIZE)
        self.root.resizable(width=tk.FALSE, height=tk.FALSE)
        self.root.title(TITLE)
        self.root['background'] = DARK_COLOR
        self.__CreateLabel(x=10, y=30, text="Your nickname")
        self.input_player_name = self.__CreateInput(x=210, y=30, default_value=self.GetPlayerName())
        self.__CreateButton(x=550, y=20, text="Connect", callback=self.EventConnect)
        self.__CreateLabel(x=10, y=90, text="Server Address")
        self.input_server_ip = self.__CreateInput(x=210, y=90, default_value="192.168.0.3:8888")
        self.__CreateServersTree()
        self.AddServersInFrame()
    
    def __initialize(self):
        if not self.GetSampPath():
            raise Exception("Can't get SA-MP path")
        if not self.GetPlayerName():
            raise Exception("Can't get player name")
        self.servers = self.GetFavoriteServers()
        self.__gui_initialize()
    
    def run(self):
        self.__initialize()
        self.servers = self.GetFavoriteServers()
        self.root.mainloop()

client = SampFresh(tk.Tk())
client.run()
