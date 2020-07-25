import tkinter as tk

from tkinter import ttk
from PIL import ImageTk, Image


class Zoomer(ttk.Frame):
    def __init__(self, mainframe, path):
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('ʕ•ᴥ•ʔ')
        self.image = Image.open(path)
        self.canvas = tk.Canvas(self.master, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel_zoom)
        self.canvas.bind('<Button-5>', self.wheel_zoom)
        self.canvas.bind('<Button-4>', self.wheel_zoom)
        self.scale = 0.5
        self.image_on_canvas = None
        self.delta = 0.8
        self.text = self.canvas.create_text(0, 0, anchor='ne', text='')
        self.spawn_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),
                              bg='#7f7f7f')

    def spawn_image(self):
        if self.image_on_canvas:
            self.canvas.delete(self.image_on_canvas)
        width, height = self.image.size
        new_size = int(self.scale * width), int(self.scale * height)
        image = ImageTk.PhotoImage(self.image.resize(new_size))
        self.image_on_canvas = self.canvas.create_image(
            self.canvas.coords(self.text), anchor='nw', image=image)
        self.canvas.image = image

    def move_to(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def move_from(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def wheel_zoom(self, event):
        scale = 1.0
        if event.num == 5 or event.delta == -120:
            scale *= self.delta
            self.scale *= self.delta
        if event.num == 4 or event.delta == 120:
            scale /= self.delta
            self.scale /= self.delta
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.spawn_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
