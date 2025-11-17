from PIL import Image, ImageDraw
import math

class DrawingTools:
    """Collection of drawing tools for the image editor"""
    
    def __init__(self, image):
        # Convert to RGBA if needed for drawing
        if image.mode != 'RGBA':
            self.image = image.convert('RGBA')
        else:
            self.image = image
        self.draw = ImageDraw.Draw(self.image, 'RGBA')
    
    def pencil(self, x0, y0, x1, y1, color, size=1):
        """Draw a line using pencil tool"""
        self.draw.line([(x0, y0), (x1, y1)], fill=color, width=size)
    
    def brush(self, x, y, color, size=5):
        """Draw a filled circle (brush stroke)"""
        radius = size // 2
        self.draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=color
        )
    
    def eraser(self, x, y, size=5):
        """Erase by drawing transparent circles"""
        radius = size // 2
        self.draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=(0, 0, 0, 0)
        )
    
    def rectangle(self, x0, y0, x1, y1, color, filled=False, width=1):
        """Draw a rectangle"""
        if filled:
            self.draw.rectangle([(x0, y0), (x1, y1)], fill=color)
        else:
            self.draw.rectangle([(x0, y0), (x1, y1)], outline=color, width=width)
    
    def ellipse(self, x0, y0, x1, y1, color, filled=False, width=1):
        """Draw an ellipse"""
        if filled:
            self.draw.ellipse([(x0, y0), (x1, y1)], fill=color)
        else:
            self.draw.ellipse([(x0, y0), (x1, y1)], outline=color, width=width)
    
    def line(self, x0, y0, x1, y1, color, width=1):
        """Draw a straight line"""
        self.draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    
    def bucket_fill(self, x, y, color, threshold=10):
        """Flood fill from a point"""
        # Convert image to RGBA if needed
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')
        
        # Get the target color
        try:
            target = self.image.getpixel((int(x), int(y)))
        except:
            return
        
        # Perform flood fill
        ImageDraw.floodfill(self.image, (int(x), int(y)), color, thresh=threshold)


class ImageAdjustments:
    """Image adjustment filters"""
    
    @staticmethod
    def brightness(image, factor):
        """Adjust brightness (factor > 1 = brighter, < 1 = darker)"""
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def contrast(image, factor):
        """Adjust contrast (factor > 1 = more contrast)"""
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def saturation(image, factor):
        """Adjust color saturation"""
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def hue_rotate(image, angle):
        """Rotate hue by angle (0-360)"""
        from PIL import ImageEnhance
        # Simple implementation - just adjust saturation as placeholder
        return image
    
    @staticmethod
    def blur(image, radius=2):
        """Apply blur filter"""
        from PIL import ImageFilter
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    @staticmethod
    def sharpen(image, factor=1.0):
        """Sharpen image"""
        from PIL import ImageFilter
        return image.filter(ImageFilter.SHARPEN)
    
    @staticmethod
    def grayscale(image):
        """Convert to grayscale"""
        return image.convert('L').convert('RGB')
    
    @staticmethod
    def invert(image):
        """Invert colors"""
        from PIL import ImageOps
        return ImageOps.invert(image)
