import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import math

class ImageViewer(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg="gray20")
        self.pack(fill="both", expand=True)

        self.img = None
        self.tkimg = None
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Drawing state
        self.is_drawing = False
        self.last_x = 0
        self.last_y = 0
        self.current_tool = None
        self.tool_callback = None
        
        # Selection state
        self.selection_start = None
        self.selection_rect = None

        self.bind("<MouseWheel>", self.on_zoom)
        self.bind("<Button-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.bind("<Button-3>", self.on_pan_start)
        self.bind("<B3-Motion>", self.on_pan)
        self.bind("<Motion>", self.on_mouse_move)

    def set_image(self, img):
        if isinstance(img, Image.Image):
            img = img.copy()
            # Convert paletted images to RGB for proper display
            if img.mode == "P":
                img = img.convert("RGB")
            self.img = img
        else:
            self.img = img
        self.render()

    def screen_to_image_coords(self, screen_x, screen_y):
        """Convert screen coordinates to image coordinates"""
        img_x = (screen_x - self.pan_x) / self.zoom
        img_y = (screen_y - self.pan_y) / self.zoom
        return (img_x, img_y)

    def render(self):
        if self.img is None:
            return

        w = int(self.img.width * self.zoom)
        h = int(self.img.height * self.zoom)

        resized = self.img.resize((w, h), Image.Resampling.LANCZOS)
        self.tkimg = ImageTk.PhotoImage(resized)

        self.delete("all")
        self.create_image(self.pan_x, self.pan_y, anchor="nw", image=self.tkimg)

    def on_zoom(self, event):
        if event.delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom /= 1.1
        self.render()

    def on_pan_start(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_pan(self, event):
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.pan_x += dx
        self.pan_y += dy
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.render()

    def on_mouse_down(self, event):
        if self.img is None:
            return
        self.is_drawing = True
        img_x, img_y = self.screen_to_image_coords(event.x, event.y)
        self.last_x = img_x
        self.last_y = img_y
        self.selection_start = (img_x, img_y)
        
        if self.tool_callback:
            self.tool_callback("start", img_x, img_y)

    def on_mouse_drag(self, event):
        if not self.is_drawing or self.img is None:
            return
        img_x, img_y = self.screen_to_image_coords(event.x, event.y)
        
        if self.tool_callback:
            self.tool_callback("drag", img_x, img_y, self.last_x, self.last_y)
        
        self.last_x = img_x
        self.last_y = img_y

    def on_mouse_up(self, event):
        if not self.is_drawing or self.img is None:
            return
        self.is_drawing = False
        img_x, img_y = self.screen_to_image_coords(event.x, event.y)
        
        if self.tool_callback:
            self.tool_callback("end", img_x, img_y)

    def on_mouse_move(self, event):
        pass
