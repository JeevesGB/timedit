# main.py
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, Scale
from tkinter import ttk
from PIL import Image
import os

from timedit import TimImage
from image_viewer import ImageViewer
from tools import DrawingTools, ImageAdjustments
from layers import LayerStack
from undo_redo import UndoRedoManager

class TimEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TimEdit - PS1 TIM Image Editor")
        self.root.geometry("1200x700")

        self.current_tim = None
        self.undo_manager = UndoRedoManager()
        self.current_color = (0, 0, 0)
        self.brush_size = 5
        self.current_tool = "pencil"
        self.layers = None
        
        # Create main layout
        self._create_menu()
        self._create_toolbar()
        self._create_ui()
        
        self.root.mainloop()
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_image)
        file_menu.add_command(label="Open TIM...", command=self.open_tim)
        file_menu.add_command(label="Open Image...", command=self.open_image)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_tim)
        file_menu.add_command(label="Save As...", command=self.save_tim_as)
        file_menu.add_command(label="Export As...", command=self.export_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Image menu
        image_menu = tk.Menu(menubar, tearoff=0)
        image_menu.add_command(label="Brightness/Contrast", command=self.adjust_brightness_contrast)
        image_menu.add_command(label="Saturation", command=self.adjust_saturation)
        image_menu.add_command(label="Blur", command=self.apply_blur)
        image_menu.add_command(label="Sharpen", command=self.apply_sharpen)
        image_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        image_menu.add_command(label="Invert Colors", command=self.apply_invert)
        menubar.add_cascade(label="Image", menu=image_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Keyboard bindings
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
    
    def _create_toolbar(self):
        """Create toolbar with tool buttons"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Tool buttons
        tools_frame = ttk.LabelFrame(toolbar, text="Tools")
        tools_frame.pack(side=tk.LEFT, padx=5)
        
        tools = [
            ("Pencil", "pencil"),
            ("Brush", "brush"),
            ("Eraser", "eraser"),
            ("Line", "line"),
            ("Rectangle", "rectangle"),
            ("Ellipse", "ellipse"),
            ("Bucket Fill", "bucket"),
            ("Color Picker", "picker"),
        ]
        
        for label, tool_name in tools:
            btn = ttk.Button(tools_frame, text=label, 
                           command=lambda t=tool_name: self.set_tool(t))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Color selector
        color_frame = ttk.LabelFrame(toolbar, text="Color")
        color_frame.pack(side=tk.LEFT, padx=5)
        
        self.color_display = tk.Canvas(color_frame, width=40, height=40, bg="#000000")
        self.color_display.pack(pady=5)
        
        ttk.Button(color_frame, text="Pick Color", 
                  command=self.pick_color).pack()
        
        # Brush size
        size_frame = ttk.LabelFrame(toolbar, text="Brush Size")
        size_frame.pack(side=tk.LEFT, padx=5)
        
        self.size_slider = Scale(size_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                                command=lambda v: setattr(self, 'brush_size', int(v)))
        self.size_slider.set(5)
        self.size_slider.pack(pady=5)
    
    def _create_ui(self):
        """Create main UI layout"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Layers
        left_panel = ttk.LabelFrame(main_frame, text="Layers")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        self.layers_listbox = tk.Listbox(left_panel, height=15, width=20)
        self.layers_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.layers_listbox.bind('<<ListboxSelect>>', self.on_layer_select)
        
        layer_buttons = ttk.Frame(left_panel)
        layer_buttons.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(layer_buttons, text="+ New", command=self.new_layer).pack(side=tk.LEFT, padx=2)
        ttk.Button(layer_buttons, text="- Delete", command=self.delete_layer).pack(side=tk.LEFT, padx=2)
        
        # Center - Canvas
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.viewer = ImageViewer(canvas_frame)
        self.viewer.tool_callback = self.on_canvas_tool
        
        # Right panel - Properties
        right_panel = ttk.LabelFrame(main_frame, text="Properties")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        ttk.Label(right_panel, text="Image Info:").pack(anchor=tk.W, padx=5, pady=5)
        self.info_text = tk.Text(right_panel, height=15, width=25, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def set_tool(self, tool):
        """Set the current tool"""
        self.current_tool = tool
        print(f"Tool changed to: {tool}")
    
    def on_canvas_tool(self, event, x, y, prev_x=None, prev_y=None):
        """Handle canvas drawing events"""
        if self.current_tim is None or self.layers is None:
            return
        
        active_layer = self.layers.get_active_layer()
        if active_layer is None or active_layer.locked:
            return
        
        x, y = int(x), int(y)
        if prev_x is not None:
            prev_x, prev_y = int(prev_x), int(prev_y)
        
        # Ensure coordinates are within bounds
        if x < 0 or x >= active_layer.image.width or y < 0 or y >= active_layer.image.height:
            return
        
        tools = DrawingTools(active_layer.image)
        color_rgba = (*self.current_color, 255)
        
        if event == "start":
            self.undo_manager.save_state(self.layers.flatten())
        
        elif event == "drag":
            if self.current_tool == "pencil":
                tools.pencil(prev_x, prev_y, x, y, color_rgba, self.brush_size)
            elif self.current_tool == "brush":
                tools.brush(x, y, color_rgba, self.brush_size)
            elif self.current_tool == "eraser":
                tools.eraser(x, y, self.brush_size)
            elif self.current_tool == "line":
                tools.line(prev_x, prev_y, x, y, color_rgba, self.brush_size)
        
        elif event == "end":
            if self.current_tool == "rectangle":
                # Would need to track selection start
                pass
            elif self.current_tool == "bucket":
                tools.bucket_fill(x, y, color_rgba)
        
        self.viewer.set_image(self.layers.get_merged_image())
    
    def pick_color(self):
        """Open color picker"""
        color = colorchooser.askcolor(color=self.current_color)
        if color[0]:
            self.current_color = color[0]
            self.color_display.config(bg=color[1])
    
    def new_image(self):
        """Create a new image"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Image")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Width:").pack()
        width_entry = ttk.Entry(dialog)
        width_entry.insert(0, "256")
        width_entry.pack()
        
        tk.Label(dialog, text="Height:").pack()
        height_entry = ttk.Entry(dialog)
        height_entry.insert(0, "256")
        height_entry.pack()
        
        def create():
            try:
                w, h = int(width_entry.get()), int(height_entry.get())
                img = Image.new('RGB', (w, h), (255, 255, 255))
                self.current_tim = TimImage()
                self.current_tim.image = img
                self.current_tim.width = w
                self.current_tim.height = h
                self.current_tim.bpp = 16
                
                self.layers = LayerStack(w, h)
                self.layers.add_layer("Background", img)
                
                self.viewer.set_image(img)
                self.update_info()
                self.refresh_layers_list()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid dimensions")
        
        ttk.Button(dialog, text="Create", command=create).pack(pady=10)
    
    def new_layer(self):
        """Add a new layer"""
        if self.layers is None:
            messagebox.showwarning("No Image", "Open or create an image first")
            return
        
        self.layers.add_layer(f"Layer {len(self.layers.layers)}")
        self.refresh_layers_list()
    
    def delete_layer(self):
        """Delete the selected layer"""
        if self.layers is None or len(self.layers.layers) <= 1:
            return
        
        idx = self.layers_listbox.curselection()
        if idx:
            self.layers.remove_layer(idx[0])
            self.refresh_layers_list()
    
    def on_layer_select(self, event):
        """Handle layer selection"""
        if self.layers is None:
            return
        
        selection = self.layers_listbox.curselection()
        if selection:
            self.layers.set_active_layer(selection[0])
    
    def refresh_layers_list(self):
        """Refresh the layers listbox"""
        self.layers_listbox.delete(0, tk.END)
        if self.layers:
            for i, layer in enumerate(reversed(self.layers.layers)):
                status = "✓" if layer.visible else "✗"
                self.layers_listbox.insert(0, f"{status} {layer.name}")
    
    def open_tim(self):
        """Open a TIM file"""
        path = filedialog.askopenfilename(filetypes=[("TIM files", "*.tim")])
        if not path:
            return

        try:
            tim = TimImage()
            tim.load(path)
            self.current_tim = tim
            
            # Create layers from loaded image
            self.layers = LayerStack(tim.width, tim.height)
            self.layers.add_layer("Background", tim.image)
            
            self.viewer.set_image(tim.image)
            self.update_info()
            self.refresh_layers_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open TIM: {str(e)}")
    
    def open_image(self):
        """Open any image file"""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.bmp *.gif")])
        if not path:
            return
        
        try:
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            self.current_tim = TimImage()
            self.current_tim.image = img
            self.current_tim.width = img.width
            self.current_tim.height = img.height
            self.current_tim.bpp = 16
            self.current_tim.file_path = path
            
            self.layers = LayerStack(img.width, img.height)
            self.layers.add_layer("Background", img)
            
            self.viewer.set_image(img)
            self.update_info()
            self.refresh_layers_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def save_tim(self):
        """Save as TIM file"""
        if not self.current_tim:
            messagebox.showwarning("No file", "Open or create an image first.")
            return

        if not self.current_tim.file_path:
            return self.save_tim_as()

        try:
            self.current_tim.image = self.layers.get_merged_image()
            self.current_tim.save(self.current_tim.file_path)
            messagebox.showinfo("Saved", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def save_tim_as(self):
        """Save as new TIM file"""
        if not self.current_tim:
            messagebox.showwarning("No file", "Open or create an image first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".tim",
            filetypes=[("TIM files", "*.tim")]
        )
        if not path:
            return

        try:
            self.current_tim.image = self.layers.get_merged_image()
            self.current_tim.save(path)
            messagebox.showinfo("Saved", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_image(self):
        """Export as PNG/JPG"""
        if not self.current_tim:
            messagebox.showwarning("No file", "Open or create an image first.")
            return
        
        path = filedialog.asksaveasfilename(
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")]
        )
        if not path:
            return
        
        try:
            img = self.layers.get_merged_image()
            img.save(path)
            messagebox.showinfo("Exported", f"Image exported to {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def adjust_brightness_contrast(self):
        """Adjust brightness and contrast"""
        if self.current_tim is None:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Brightness/Contrast")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Brightness:").pack()
        bright_scale = Scale(dialog, from_=0.1, to=3, resolution=0.1, orient=tk.HORIZONTAL)
        bright_scale.set(1.0)
        bright_scale.pack()
        
        tk.Label(dialog, text="Contrast:").pack()
        contrast_scale = Scale(dialog, from_=0.1, to=3, resolution=0.1, orient=tk.HORIZONTAL)
        contrast_scale.set(1.0)
        contrast_scale.pack()
        
        def apply_changes():
            try:
                img = self.layers.get_merged_image()
                img = ImageAdjustments.brightness(img, float(bright_scale.get()))
                img = ImageAdjustments.contrast(img, float(contrast_scale.get()))
                
                self.layers = LayerStack(img.width, img.height)
                self.layers.add_layer("Adjusted", img)
                self.viewer.set_image(img)
                self.refresh_layers_list()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Apply", command=apply_changes).pack(pady=10)
    
    def adjust_saturation(self):
        """Adjust color saturation"""
        if self.current_tim is None:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Saturation")
        dialog.geometry("300x100")
        
        tk.Label(dialog, text="Saturation:").pack()
        sat_scale = Scale(dialog, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        sat_scale.set(1.0)
        sat_scale.pack()
        
        def apply_changes():
            try:
                img = self.layers.get_merged_image()
                img = ImageAdjustments.saturation(img, float(sat_scale.get()))
                
                self.layers = LayerStack(img.width, img.height)
                self.layers.add_layer("Saturated", img)
                self.viewer.set_image(img)
                self.refresh_layers_list()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Apply", command=apply_changes).pack(pady=10)
    
    def apply_blur(self):
        """Apply blur filter"""
        if self.current_tim is None:
            return
        
        img = self.layers.get_merged_image()
        img = ImageAdjustments.blur(img, radius=3)
        
        self.layers = LayerStack(img.width, img.height)
        self.layers.add_layer("Blurred", img)
        self.viewer.set_image(img)
        self.refresh_layers_list()
    
    def apply_sharpen(self):
        """Apply sharpen filter"""
        if self.current_tim is None:
            return
        
        img = self.layers.get_merged_image()
        img = ImageAdjustments.sharpen(img)
        
        self.layers = LayerStack(img.width, img.height)
        self.layers.add_layer("Sharpened", img)
        self.viewer.set_image(img)
        self.refresh_layers_list()
    
    def apply_grayscale(self):
        """Convert to grayscale"""
        if self.current_tim is None:
            return
        
        img = self.layers.get_merged_image()
        img = ImageAdjustments.grayscale(img)
        
        self.layers = LayerStack(img.width, img.height)
        self.layers.add_layer("Grayscale", img)
        self.viewer.set_image(img)
        self.refresh_layers_list()
    
    def apply_invert(self):
        """Invert colors"""
        if self.current_tim is None:
            return
        
        img = self.layers.get_merged_image()
        img = ImageAdjustments.invert(img)
        
        self.layers = LayerStack(img.width, img.height)
        self.layers.add_layer("Inverted", img)
        self.viewer.set_image(img)
        self.refresh_layers_list()
    
    def undo(self):
        """Undo last action"""
        if not self.undo_manager.can_undo():
            return
        
        state = self.undo_manager.undo()
        if state:
            self.viewer.set_image(state)
    
    def redo(self):
        """Redo last undone action"""
        if not self.undo_manager.can_redo():
            return
        
        state = self.undo_manager.redo()
        if state:
            self.viewer.set_image(state)
    
    def update_info(self):
        """Update image information display"""
        if self.current_tim is None:
            return
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        info = f"""Image: {os.path.basename(self.current_tim.file_path or 'Untitled')}
Width: {self.current_tim.width}px
Height: {self.current_tim.height}px
BPP: {self.current_tim.bpp}
Layers: {len(self.layers.layers) if self.layers else 0}
Color Mode: {'RGBA' if self.current_tim.has_clut else 'RGB'}
"""
        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About",
            "TimEdit - PS1 TIM Image Editor\n\n"
            "A Photoshop-like image editor for PS1 TIM files\n\n"
            "Features:\n"
            "• Load and save TIM files\n"
            "• Drawing tools (pencil, brush, eraser)\n"
            "• Shape tools (rectangle, ellipse)\n"
            "• Image adjustments\n"
            "• Layer support\n"
            "• Undo/Redo")

if __name__ == "__main__":
    TimEditorApp()

