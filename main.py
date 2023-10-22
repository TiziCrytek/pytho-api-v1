import os, tkinter, json, webbrowser, threading
import customtkinter as ctk
from PIL import Image, ImageTk
from time import sleep

import requests, uuid, os

class Client:
    def __init__(self, window, version):
        self.url = 'https://api-v1.vercel.app/'

        self.window = window
        self.version = version
        self.code = 15142
    
    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.mac = ":".join([mac[e:e+2] for e in range(0, 11, 2)])

    def sender(self, method):
        if method == 'version':
            res = requests.post(self.url + 'version', json={ "version": self.version, "code": self.code }).status_code
        elif method == 'connect':
            res = requests.post(self.url + 'connect', json={ "code": self.code }).status_code
        elif method == 'login':
            res = requests.post(self.url + 'login', json={ "key": self.key, "mac": self.mac, "code": self.code }).json()
        elif method == 'save':
            res = requests.post(self.url + 'save', json={"key": self.key, "mac": self.mac, "code": self.code }).status_code
        elif method == 'delete_device':
            res = requests.post(self.url + 'delete', json={"key": self.key, "code": self.code }).status_code
        
        return res

    def connect(self):
        res = True

        if requests.post(self.url).status_code != 200:
            if self.window.toplevel_window is None or not self.window.toplevel_window.winfo_exists():
                self.window.toplevel_window = Alert('no_connect', self.window)
                self.window.toplevel_window.focus()
                self.window.toplevel_window.grab_set()
                self.window.key.delete(0, 'end')

                res = False

        elif self.sender('connect') != 200:
            if self.window.toplevel_window is None or not self.window.toplevel_window.winfo_exists():
                self.window.toplevel_window = Alert('disconnect', self.window)
                self.window.toplevel_window.focus()
                self.window.toplevel_window.grab_set()
                self.window.key.delete(0, 'end')

                res = False

        elif self.sender('version') != 200:
            if self.window.toplevel_window is None or not self.window.toplevel_window.winfo_exists():
                self.window.toplevel_window = Alert('update', self.window)
                self.window.toplevel_window.focus()
                self.window.toplevel_window.grab_set()
                self.window.key.delete(0, 'end')

                res = False

        return res

    def login(self):
        if os.path.exists(self.window.key_path):
            with open(self.window.key_path, 'r') as file:
                self.key = file.readline().strip()
                file.close()
        else:
            self.key = self.window.key.get()

        if self.key:
            if self.connect():
                self.get_mac_address()
                res = self.sender('login')
                print(res)

                if res['key']['status'] == 'ok':
                    if res['key']['device'] == '':
                        if self.window.toplevel_window is None or not self.window.toplevel_window.winfo_exists():
                            self.window.toplevel_window = Device(self, self.window)
                            self.window.toplevel_window.focus()
                            self.window.toplevel_window.grab_set()
                    elif res['key']['device'] == self.mac:
                        self.window.new_app = res['app']
                        self.window.destroy()
                    else:
                        if self.window.toplevel_window is None or not self.window.toplevel_window.winfo_exists():
                            self.window.toplevel_window = Alert('error_device', self.window)
                            self.window.toplevel_window.focus()
                            self.window.toplevel_window.grab_set()
                            self.window.key.delete(0, 'end')
                elif res['key']['status'] == 'no_key':
                    self.window.msg.configure(text='КЛЮЧ НЕ НАЙДЕН')
                    self.window.key.delete(0, 'end')

    def device_remove(self):
        with open(self.window.key_path, 'r') as file:
            self.key = file.readline().strip()
            file.close()

        if self.connect():
            if self.sender('delete_device') == 200:
                os.remove(self.window.key_path)
                self.window.destroy()

class Device(ctk.CTkToplevel):
    def __init__(self, connect: Client = None, window=None):
        super().__init__()
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon")
        self.a = 0.0
        self.an = False

        self.connect = connect
        self.window = window
        self.res = None

        self.window.update_idletasks() 
        login_x = self.window.winfo_x()  
        login_y = self.window.winfo_y()  
        login_width = self.window.winfo_width()
        login_height = self.window.winfo_height()

        test_width = 240  
        test_height = 320

        test_x = login_x + (login_width - test_width) // 2 
        test_y = login_y + (login_height - test_height) // 2

        self.overrideredirect(True)
        self.attributes("-alpha", 0.0)
        self.geometry(f"{test_width}x{test_height}+{test_x + 10}+{test_y + 30}")
        self.resizable(False, False)

        self.title = 'Новое устройстов'
        self.message = 'Хотите привязать это устройство к ключу'
        self.color = '#3f75cd'
        self.img = ctk.CTkImage(Image.open(os.path.join(image_path, "pc.png")), size=(50, 50))

        self.frame = ctk.CTkFrame(self, width=240, height=320, fg_color='gray10')
        self.frame.pack()

        self.icon = ctk.CTkFrame(self.frame, width=75, height=75, fg_color=self.color, corner_radius=5)
        self.icon.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        self.set_img = ctk.CTkLabel(self.icon, text='', image=self.img)
        self.set_img.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.ttl = ctk.CTkLabel(self.frame, text=self.title, text_color=self.color, font=ctk.CTkFont(size=17))
        self.ttl.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        self.msg = ctk.CTkLabel(self.frame, text=self.message, wraplength=220, font=ctk.CTkFont(size=13))
        self.msg.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.check = ctk.CTkCheckBox(self.frame, text='Всегда входить по этому ключу', fg_color=self.color, hover_color=self.color, border_color=self.color, checkbox_width=20, checkbox_height=20)
        self.check.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
        self.check.select()

        self.ok = ctk.CTkButton(self.frame, width=120, text='ПРИВЯЗАТЬ', fg_color='grey15', hover_color='#399157', command=self.save)
        self.ok.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        self.close_btn = ctk.CTkButton(self.frame, width=120, text='ОТМЕНА', fg_color='grey15', hover_color='#913939', command=self.close)
        self.close_btn.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)
        self.animation_on()

    def save(self):
        if self.check.get() == 1:
            with open(self.window.key_path, 'w') as file:
                file.write(self.window.key.get())
                file.close()
            self.window.connect.login()
        else:
            self.window.connect.login()

        self.connect.sender('save')

        if self.an != True:
            self.animation_off()

    def close(self):

        if self.an != True:
            self.animation_off()

    def animation_on(self):
        if self.a < 1.0:
            self.an = True
            self.a += 0.005
            self.attributes('-alpha', self.a)
            self.after(1, self.animation_on)
        else:
            self.an = False
            self.a = 1.0

    def animation_off(self):
        if self.a > 0.0:
            self.a -= 0.010
            self.attributes('-alpha', self.a)
            self.after(1, self.animation_off)
        else:
            self.destroy()
            if self.res == '-error':
                Alert('error_device', self.window)

class Alert(ctk.CTkToplevel):
    def __init__(self, alert_type=None, window=None):
        super().__init__()
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon")
        self.a = 0.0
        self.an = False

        self.window = window
        self.update_app = None
        self.alert_type = alert_type

        self.window.update_idletasks() 
        login_x = self.window.winfo_x()  
        login_y = self.window.winfo_y()  
        login_width = self.window.winfo_width()
        login_height = self.window.winfo_height()

        self.test_width = 240  
        self.test_height = 320

        self.test_x = login_x + (login_width - self.test_width) // 2 + 9
        test_y = login_y + (login_height - self.test_height) // 2

        self.overrideredirect(True)
        self.attributes("-alpha", 0.0)
        self.geometry(f"{self.test_width}x{self.test_height}+{self.test_x}+{test_y + 100}")
        self.resizable(False, False)

        self.y = self.winfo_y()

        if self.alert_type == 'no_connect':
            self.title = 'Ошибка подключения'
            self.message = 'Сервер не в сети, повторите попытку позже'
            self.color = '#cd983f'
            self.img = ctk.CTkImage(Image.open(os.path.join(image_path, "server_no_conenct.png")), size=(50, 50))
        elif self.alert_type == 'update':
            self.title = 'Доступна новая версия'
            self.message = 'Обновите клиента до последней версии'
            self.color = '#60cd3f'
            self.img = ctk.CTkImage(Image.open(os.path.join(image_path, "download.png")), size=(50, 50))
            self.update_app = True
        elif self.alert_type == 'disconnect':
            self.title = 'Не удалось подключиться'
            self.message = 'Сервер отклонил запрос на подключение'
            self.color = '#cd783f'
            self.img = ctk.CTkImage(Image.open(os.path.join(image_path, "alerts.png")), size=(50, 50))
            self.telegram_img = ctk.CTkImage(Image.open(os.path.join(image_path, "telegram.png")), size=(18, 18))
        elif self.alert_type == 'error_device':
            self.title = 'Ошибка подключения'
            self.message = 'Этот ключ уже привязан к другому устройсту'
            self.color = '#cd783f'
            self.img = ctk.CTkImage(Image.open(os.path.join(image_path, "pc_error.png")), size=(50, 50))
            self.telegram_img = ctk.CTkImage(Image.open(os.path.join(image_path, "telegram.png")), size=(18, 18))
        else:
            self.title = 'Title'
            self.message = 'Message'
            self.color = '#a1a1a1'
            self.img = ctk.CTkImage(Image.open(os.path.join(image_path, "server_no_conenct.png")), size=(50, 50))

        self.frame = ctk.CTkFrame(self, width=240, height=320, fg_color='gray10')
        self.frame.pack()

        self.icon = ctk.CTkFrame(self.frame, width=75, height=75, fg_color=self.color, corner_radius=5)
        self.icon.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        self.set_img = ctk.CTkLabel(self.icon, text='', image=self.img)
        self.set_img.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.ttl = ctk.CTkLabel(self.frame, text=self.title, text_color=self.color, font=ctk.CTkFont(size=17))
        self.ttl.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        self.msg = ctk.CTkLabel(self.frame, text=self.message, wraplength=220, font=ctk.CTkFont(size=13))
        self.msg.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        if self.update_app:
            self.telegram = ctk.CTkButton(self.frame, width=120, text='ОБНОВИТЬ', fg_color='grey15', hover_color='#60cd3f', command=self.open_tg)
            self.telegram.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        if self.alert_type == 'disconnect' or self.alert_type == 'error_device':
            self.telegram = ctk.CTkButton(self.frame, width=120, text='TELEGRAM', fg_color='grey15', hover_color='#3fadcd', image=self.telegram_img, command=self.open_tg2)
            self.telegram.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        self.close_btn = ctk.CTkButton(self.frame, width=120, text='CLOSE', fg_color='grey15', hover_color='#913939', command=self.close)
        self.close_btn.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)
        self.animation_on()
    
    def animation_on(self):
        if self.y > 382:
            self.an = True
            self.geometry(f"{self.test_width}x{self.test_height}+{self.test_x}+{self.y}")
            self.y -= 1
            self.after(1, self.animation_on)

        if self.a < 1.0:
            self.attributes('-alpha', self.a)
            self.a += 0.005
            if self.y == 382:
                self.after(1, self.animation_on)
        else:
            self.an = False
            self.a = 1.0

    def animation_off(self):
        if self.a > 0.0:
            self.a -= 0.010
            self.attributes('-alpha', self.a)
            self.after(1, self.animation_off)
        else:
            self.destroy()
            if self.update_app:
                self.window.destroy()

    def open_tg(self):
        self.animation_off()
        webbrowser.open('https://t.me/paytex_official')

    def open_tg2(self):
        self.animation_off()
        webbrowser.open('https://t.me/paytex_official')

    def close(self):
        if self.an != True:
            self.animation_off()
        

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.new_app = ''
        self.folder = 'D:/Paytex/SkinChanger/'
        ctk.set_appearance_mode('dark')
        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon")
        # self.login_img = ctk.CTkImage(Image.open(os.path.join(image_path, "login.ico")), size=(20, 20))

        self.title("Login")
        window_width = 520
        window_height = 520
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.key_path = os.path.join(self.folder, "save_key.txt")

        self.frame = ctk.CTkFrame(self, width=320, height=380, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.l2 = ctk.CTkLabel(self.frame, text='ВХОД', font=ctk.CTkFont(size=20))
        self.l2.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        self.msg = ctk.CTkLabel(self.frame, text='', text_color='red')
        self.msg.place(relx=0.5, rely=0.27, anchor=ctk.CENTER)

        if os.path.exists(self.key_path):
            self.button = ctk.CTkButton(self.frame, width=230, text='ВОЙТИ ПО КЛЮЧУ', fg_color='gray15', hover_color='#623991', command=self.login)
            self.button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

            self.free = ctk.CTkButton(self.frame, width=230, text='УДАЛИТЬ ВХОД ПО КЛЮЧУ', fg_color='gray15', hover_color='#623991', command=self.delete_key)
            self.free.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        else:
            self.key = ctk.CTkEntry(self.frame, width=230, placeholder_text='KEY')
            self.key.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

            self.button = ctk.CTkButton(self.frame, width=230, text='ВОЙТИ', fg_color='gray15', hover_color='#623991', command=self.login)
            self.button.place(relx=0.5, rely=0.58, anchor=ctk.CENTER)

            self.free = ctk.CTkButton(self.frame, width=230, text='БЕСПЛАТНАЯ ВЕРСИЯ', fg_color='gray15', hover_color='#623991', command=self.open_free)
            self.free.place(relx=0.5, rely=0.68, anchor=ctk.CENTER)

        self.get_key = ctk.CTkButton(self.frame, width=230, text='ПОЛУЧИТЬ КЛЮЧ', fg_color='gray15', hover_color='#3f8ecd', command=self.open_url)
        self.get_key.place(relx=0.5, rely=0.88, anchor=ctk.CENTER)

        self.version = ctk.CTkLabel(self, text='v0.1', font=ctk.CTkFont(size=12))
        self.version.place(relx=0.97, rely=0.98, anchor=ctk.CENTER)

        self.toplevel_window = None
        
        self.connect = Client(self, self.version.cget('text'))

    def lock_btn(self):
        try:
            self.button.configure(state='disabled')
            self.after(2000, self.enable_btn)
        except:
            pass

    def enable_btn(self):
        self.button.configure(state='normal')

    def login(self):
        self.msg.configure(text='')
        thread = threading.Thread(target=self.lock_btn)
        thread.start()

        self.connect.login()

    def delete_key(self):
        self.connect.device_remove()

    def open_free(self):
        pass
    
    def open_url(self):
        webbrowser.open('https://t.me/paytex_official')

if __name__ == '__main__':
    if not os.path.exists('D:/Paytex/SkinChanger'):
        os.makedirs('D:/Paytex/SkinChanger')

    app = Login()
    app.mainloop()
    exec(app.new_app)