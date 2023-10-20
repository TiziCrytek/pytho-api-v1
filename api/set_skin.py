set_skin = """

class SetSkin(ctk.CTkToplevel):
    def __init__(self, old_id):
        super().__init__()
        ctk.set_appearance_mode('dark')

        self.title("SkinChanger")

        window_width = 720
        window_height = 450
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.scroll.grid(row=0, column=0, sticky='nsew', padx=(35, 0))

        skins_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "common.json")
        with open(skins_file_path, 'r') as json_file: 
            self.data = json.load(json_file)
        
        r = 0
        c = 0

        for skin in self.data:
            image = self.data[skin]['image']
            name = self.data[skin]['name']
            rarity = self.data[skin]['rarity']
            item_id = self.data[skin]['id']
            color = self.data[skin]['color']
            if c == 4:
                c = 0
                r += 1
            self.menu = Item(self.scroll, image, name, rarity, color, item_id, old_id, self)
            self.menu.grid(row=r, column=c, padx=(0, 10), pady=(0, 10), sticky='nsew')
            c += 1

"""