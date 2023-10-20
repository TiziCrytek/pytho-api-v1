import socket, os, json, threading

from time import sleep
from item import item
from set_skin import set_skin
from app import app

class Server():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = "127.0.0.1"
        port = 12345
        
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Сервер слушает на {host}:{port}")

        self.skins = os.path.join(os.path.dirname(os.path.realpath(__file__)), "skins.json")
        with open(self.skins, 'r') as f:
            self.skins = json.load(f)

        self.keys_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keys.json")
        self.server_status = True
        self.version_app = 'v0.1'

        threading.Thread(target=self.cmd).start()

    def start_server(self):
        while True:
            # Принимаем входящее соединение
            self.client_socket, addr = self.server_socket.accept()

            print('Connect')
            self.client_socket.send('-connect'.encode())
            threading.Thread(target=self.root).start()

    def connect(self):
        if self.server_status:
            self.client_socket.send('-connect'.encode())
        else:
            self.client_socket.send('-disconnect'.encode())

    def root(self):
        work = True
        while work:
            try:
                func = self.client_socket.recv(1024).decode()
                print(func)

                if func == '-login':
                    self.login()
                elif func == '-get_item':
                    self.get_item()
                elif func == '-version':
                    self.version()
                elif func == '-device_delete':
                    self.device_delete()
                elif func == '-ping':
                    self.connect()
                elif func == '-disconnect':
                    work = False
                    self.client_socket.close()
                    print('Disconnect | Client Disconnect')
                else:
                    work = False
                    self.client_socket.close()
                    print('Disconnect | Client Closed App')
            except:
                work = False
                print('Disconnect | Error Client')

    def send_app(self):
        self.client_socket.send('-ok'.encode())
        self.client_socket.recv(1024)
        self.client_socket.send(set_skin.encode())
        self.client_socket.recv(1024)
        self.client_socket.send(item.encode())
        self.client_socket.recv(1024)
        self.client_socket.send(app.encode())
        self.client_socket.recv(1024)

    def login(self):
        self.client_socket.send('-get'.encode())

        with open(self.keys_path, 'r') as f:
            self.keys = json.load(f)
            f.close()
        
        key = self.client_socket.recv(1024).decode()
        if key in self.keys:
            print(key)
            self.client_socket.send('-key'.encode())
            self.pc = self.client_socket.recv(1024).decode()
            self.client_socket.send('-get'.encode())
            if self.keys[key]['device'] != '' and self.pc == self.keys[key]['device']:
                self.client_socket.recv(1024)
                self.client_socket.send('-app'.encode())
                self.send_app()
            elif self.keys[key]['device'] == '':
                self.client_socket.send('-no_device'.encode())
                res = self.client_socket.recv(1024).decode()
                if res == '-save':
                    with open(self.keys_path, 'r') as f:
                        self.keys = json.load(f)
                        f.close()

                    if self.keys[key]['device'] == '':
                        self.keys[key]['device'] = self.pc
                        with open(self.keys_path, 'w') as file:
                            json.dump(self.keys, file, indent=4)
                            file.close()
                        self.client_socket.send('-ok'.encode())
                    else:
                        self.client_socket.send('-error'.encode())

                elif res == '-cancel':
                    print(res)

            elif self.pc != self.keys[key]['device']:
                self.client_socket.send('-error_device'.encode())
        else:
            self.client_socket.send('-no_key'.encode())

    def get_item(self):
        self.client_socket.send('-get'.encode())
        skins_json = json.dumps(self.skins)
        self.client_socket.send(skins_json.encode())

    def version(self):
        self.client_socket.send('-get'.encode())
        version = self.client_socket.recv(1024).decode()
        if version == self.version_app:
            self.client_socket.send('-app'.encode())
        else:
            self.client_socket.send('-update_app'.encode())

    def device_delete(self):
        self.client_socket.send('-get'.encode())
        with open(self.keys_path, 'r') as f:
            self.keys = json.load(f)

        key = self.client_socket.recv(1024).decode()
        self.client_socket.send('-get'.encode())
        if key in self.keys:
            self.keys[key]['device'] = ''
            with open(self.keys_path, 'w') as file:
                json.dump(self.keys, file, indent=4)
            self.client_socket.send('-delete'.encode())
        else:
            self.client_socket.send('-no_delete'.encode())            

    def cmd(self):
        work = True
        while work:
            command = input()
            if command:
                if command == 'server_close':
                    self.server_status = False
                    print('SERVER CLOSED')
                elif command == 'server_open':
                    self.server_status = True
                    print('SERVER OPEN')
                elif command == 'set_version':
                    v = input('Version: ')
                    self.version_app = v
                    print('VERSION SAVE')
                elif command == 'help':
                    print('All commands:')
                    print('server_open')
                    print('server_close')
                    print('set_version')
                else:
                    print('NO COMMAND')
