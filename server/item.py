item = """

class Item(ctk.CTkFrame):
    def __init__(self, master, item_image=None, item_name=None, item_rarity=None, color=None, item_id=None, old_id=None, window=None):
        super().__init__(master)
        self.item_id = item_id
        self.old_id = old_id
        self.window = window
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "item")
        image = ctk.CTkImage(Image.open(os.path.join(image_path, item_image)), size=(150, 75))

        image_frame = ctk.CTkLabel(self, text='', image=image)
        image_frame.grid(row=0, column=0, sticky='nsew', pady=(5, 0))
        self.name = ctk.CTkLabel(self, text=item_name)
        self.name.grid(row=1, column=0, sticky='nsew')
        self.rarity = ctk.CTkLabel(self, text=item_rarity, text_color=color)
        self.rarity.grid(row=2, column=0, sticky='nsew')
        self.button = ctk.CTkButton(self, text='Применить', fg_color='grey10', hover_color='#623991', command=self.set_skin)
        self.button.grid(row=3, column=0, pady=(0, 5))

        self.toplevel_window = None

    def set_skin(self):
        if self.old_id:
            print(self.old_id)
            print(self.item_id)
            self.window.destroy()
        else:
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = SetSkin(self.item_id)
                self.toplevel_window.focus()
                self.toplevel_window.grab_set()
            else:
                self.toplevel_window.focus()

"""