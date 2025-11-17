from PIL import Image
import copy

class Layer:
    """Represents a single layer in the image"""
    
    def __init__(self, name, image, opacity=1.0):
        self.name = name
        self.image = image.copy() if isinstance(image, Image.Image) else image
        self.opacity = opacity
        self.visible = True
        self.locked = False
    
    def get_display_image(self):
        """Get the layer image with opacity applied"""
        if self.image.mode != 'RGBA':
            img = self.image.convert('RGBA')
        else:
            img = self.image.copy()
        
        if self.opacity < 1.0:
            alpha = img.split()[3] if len(img.split()) > 3 else Image.new('L', img.size, 255)
            alpha = alpha.point(lambda p: int(p * self.opacity))
            img.putalpha(alpha)
        
        return img


class LayerStack:
    """Manages a stack of layers"""
    
    def __init__(self, width, height):
        self.layers = []
        self.width = width
        self.height = height
        self.active_layer_idx = 0
    
    def add_layer(self, name, image=None, index=None):
        """Add a new layer"""
        if image is None:
            image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        
        layer = Layer(name, image)
        
        if index is None:
            self.layers.append(layer)
        else:
            self.layers.insert(index, layer)
        
        return layer
    
    def remove_layer(self, index):
        """Remove a layer"""
        if len(self.layers) > 1 and index < len(self.layers):
            self.layers.pop(index)
            if self.active_layer_idx >= len(self.layers):
                self.active_layer_idx = len(self.layers) - 1
    
    def get_active_layer(self):
        """Get the currently active layer"""
        if 0 <= self.active_layer_idx < len(self.layers):
            return self.layers[self.active_layer_idx]
        return None
    
    def set_active_layer(self, index):
        """Set the active layer by index"""
        if 0 <= index < len(self.layers):
            self.active_layer_idx = index
    
    def move_layer(self, old_index, new_index):
        """Move a layer to a different position"""
        if 0 <= old_index < len(self.layers) and 0 <= new_index < len(self.layers):
            layer = self.layers.pop(old_index)
            self.layers.insert(new_index, layer)
    
    def flatten(self):
        """Flatten all visible layers into one"""
        base = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        
        for layer in reversed(self.layers):
            if layer.visible:
                layer_img = layer.get_display_image()
                base.paste(layer_img, (0, 0), layer_img)
        
        return base
    
    def get_merged_image(self):
        """Get flattened image as RGB"""
        flat = self.flatten()
        if flat.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', flat.size, (255, 255, 255))
            background.paste(flat, mask=flat.split()[3])
            return background
        return flat.convert('RGB')
