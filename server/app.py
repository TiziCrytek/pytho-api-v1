app = """

class GetSkins():
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = False

    def get(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.client_socket.send('-get_item'.encode())
            return self.client_socket.recv(10000).decode()
        except:
            pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')

        self.title("SkinChanger")
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon")
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "telegram.png")), size=(20, 20))

        window_width = 820
        window_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.sidebar_frame.grid_columnconfigure(1, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Paytex", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        self.menu = ctk.CTkFrame(self.sidebar_frame, fg_color='transparent')
        self.menu.grid(row=1, column=0, sticky='ns')
        self.menu.grid_columnconfigure(0, weight=1)

        self.button = ctk.CTkButton(self.menu, corner_radius=0, height=0, border_spacing=10, text='Пистолеты', command=self.button_1, fg_color="transparent", anchor="center", hover_color="gray30")
        self.button.grid(row=0, column=0, sticky="ew")
        self.button2 = ctk.CTkButton(self.menu, corner_radius=0, height=40, border_spacing=10, text='Пистолеты Пулиметы', command=self.button_2, fg_color="transparent", anchor="center", hover_color="gray30")
        self.button2.grid(row=1, column=0, sticky="ew")
        self.button3 = ctk.CTkButton(self.menu, corner_radius=0, height=40, border_spacing=10, text='Тяжолое Оружие', command=self.button_3, fg_color="transparent", anchor="center", hover_color="gray30")
        self.button3.grid(row=2, column=0, sticky="ew")
        self.button4 = ctk.CTkButton(self.menu, corner_radius=0, height=40, border_spacing=10, text='Винтовик', command=self.button_4, fg_color="transparent", anchor="center", hover_color="gray30")
        self.button4.grid(row=3, column=0, sticky="ew")
        self.button5 = ctk.CTkButton(self.menu, corner_radius=0, height=40, border_spacing=10, text='Снайперские Винтовик', command=self.button_5, fg_color="transparent", anchor="center", hover_color="gray30")
        self.button5.grid(row=4, column=0, sticky="ew")

        self.default = ctk.CTkFrame(self, fg_color='transparent')
        author = ctk.CTkLabel(self.default, text='SkinChanger by Paytex', font=ctk.CTkFont(size=20, weight="bold"))
        author.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)
        telegram = ctk.CTkButton(self.default, text='Telegram', image=self.image_icon_image)
        telegram.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)
        
        self.json_file = GetSkins().get()
        self.scroll = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.select_button('default')

    def button_1(self):
        self.select_button('button_1')

    def button_2(self):
        self.select_button('button_2')

    def button_3(self):
        self.select_button('button_3')

    def button_4(self):
        self.select_button('button_4')

    def button_5(self):
        self.select_button('button_5')

    def select_button(self, name):
        self.button.configure(fg_color=("gray75", "gray25") if name == "button_1" else "transparent")
        self.button2.configure(fg_color=("gray75", "gray25") if name == "button_2" else "transparent")
        self.button3.configure(fg_color=("gray75", "gray25") if name == "button_3" else "transparent")
        self.button4.configure(fg_color=("gray75", "gray25") if name == "button_4" else "transparent")
        self.button5.configure(fg_color=("gray75", "gray25") if name == "button_5" else "transparent")

        if name == 'default':
            self.all_skins = None
            self.default.grid(row=0, column=1, sticky='nsew')
        else:
            self.scroll.grid(row=0, column=1, sticky='nsew')
            self.default.grid_forget()

        if name == 'button_5':
           self.all_skins = ['awm']
        else:
            for widget in self.scroll.winfo_children():
                if isinstance(widget, Item):
                    widget.destroy()
        
        if name == 'button_1':
            self.scroll.configure(width=0, height=0)
            self.all_skins = ['g22', 'usp']
        else:
            for widget in self.scroll.winfo_children():
                if isinstance(widget, Item):
                    widget.destroy()
        
        if self.all_skins:
            self.data = json.loads(self.json_file)

            r = 0
            c = 0
            for skins in self.all_skins:
                data = self.data[skins]
                for skin in self.data[skins]:
                    image = data[skin]['image']
                    name = data[skin]['name']
                    rarity = data[skin]['rarity']
                    item_id = data[skin]['id']
                    color = data[skin]['color']
                    if c == 4:
                        c = 0
                        r += 1
                    self.menu_1 = Item(self.scroll, image, name, rarity, color, item_id)
                    self.menu_1.grid(row=r, column=c, padx=(0, 10), pady=(0, 10), sticky='nsew')
                    c += 1
            self.scroll.configure(width=200, height=200)


app = App()
app.mainloop()

"""