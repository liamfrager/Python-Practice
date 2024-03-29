import tkinter as tk
import tkinter.filedialog as fd
from PIL import Image, ImageTk


TITLE = "Watermark Applicator"
BG_COLOR = "lightgray"
CONTROLS_BG = "darkgray"
ACCEPTED_FILES = ".jpg .png"
WATERMARK_SIZE = 2 - (1 + 5 ** 0.5) / 2


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.config(padx=30, pady=30, bg=BG_COLOR)
        # Layout
        self.img_frame = tk.Frame(bg=BG_COLOR)
        self.img_frame.grid(column=0, row=0, padx=10)
        self.img_display = tk.Label(self.img_frame, bg=BG_COLOR)
        self.img_display.pack()
        # Controls menu
        self.controls = tk.Frame(self, bg=CONTROLS_BG)
        self.controls.grid(column=0, row=0, sticky='n', padx=10, ipady=3)
        # Select image
        self.upload_button = tk.Button(
            self.controls,
            text='Open Image',
            command=self.open_file,
            highlightbackground=CONTROLS_BG,
            width=12
        )
        self.upload_button.pack(pady=2, padx=10, anchor='w')
        # Select watermark
        self.watermark_button = tk.Button(
            self.controls,
            text='Select Watermark',
            command=self.select_watermark,
            highlightbackground=CONTROLS_BG,
            width=12
        )
        # Select watermark location
        menu_options = ['Top Left', 'Top Right',
                        'Bottom Left', 'Bottom Right', 'Center']
        self.selected_menu_option = tk.StringVar(self, 'Top Left')
        self.option_menu = tk.OptionMenu(
            self.controls,
            self.selected_menu_option,
            menu_options[0],
            *menu_options[1:],
            command=self.add_watermark,
        )
        self.option_menu.configure(
            highlightbackground=CONTROLS_BG,
            highlightthickness=0,
            width=11
        )
        # Download edited image
        self.download_button = tk.Button(
            self.controls,
            text='Save Image',
            command=self.download_file,
            highlightbackground=CONTROLS_BG,
            width=12
        )
        self.mainloop()

    def open_file(self):
        self.file_path = fd.askopenfile(
            parent=self,
            title="Select Image",
            filetypes=[("Image files", ACCEPTED_FILES)]
        ).name
        self.img = Image.open(self.file_path)
        self.update_display(self.img)
        self.upload_button.config(text='Open Image')
        self.watermark_button.config(text='Select Watermark')
        self.watermark_button.pack(pady=2, padx=10, anchor='w')
        self.controls.grid(column=1)

    def select_watermark(self):
        watermark_file_path = fd.askopenfile(
            parent=self,
            title="Select Watermark",
            filetypes=[("Image files", ACCEPTED_FILES)]
        ).name
        self.watermark = Image.open(watermark_file_path).convert("RGBA")
        self.watermark_button.config(text='Change Watermark')
        self.add_watermark('Top Left')
        self.option_menu.pack(pady=6, padx=14, anchor='w')
        self.download_button.pack(pady=2, padx=10, anchor='w')

    def add_watermark(self, position):
        self.edited_img = self.img.copy()
        w, h = tuple(
            [int(self.img.size[0] * WATERMARK_SIZE / self.watermark.size[0] * i)
             for i in (self.watermark.size[0], self.watermark.size[1])]
        )
        resized_watermark = self.watermark.resize((w, h))
        match position:
            case 'Top Left':
                coords = (0, 0)
            case 'Top Right':
                coords = (self.img.size[0] - resized_watermark.size[0], 0)
            case 'Bottom Left':
                coords = (0, self.img.size[1] - resized_watermark.size[1])
            case 'Bottom Right':
                coords = (self.img.size[0] - resized_watermark.size[0],
                          self.img.size[1] - resized_watermark.size[1])
            case 'Center':
                coords = ((self.img.size[0] - resized_watermark.size[0]) // 2,
                          (self.img.size[1] - resized_watermark.size[1]) // 2)
        self.edited_img.paste(resized_watermark, coords, resized_watermark)
        self.update_display(self.edited_img)

    def download_file(self):
        download_loc = fd.asksaveasfilename(
            parent=self,
            title="Save File",
            initialfile=f"watermark.{self.file_path.split(".")[-1]}"
        )
        self.edited_img.save(download_loc)

    def update_display(self, img):
        w = self.img.size[0]
        h = self.img.size[1]
        max_width = 500
        pixels_x, pixels_y = tuple(
            [int(max_width/w * x) for x in (w, h)]
        )
        self.preview_img = ImageTk.PhotoImage(
            img.resize((pixels_x, pixels_y)))
        self.img_display.configure(image=self.preview_img)
        self.img_display.image = self.preview_img


app = GUI()
