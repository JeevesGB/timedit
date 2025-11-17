from PIL import Image
import struct

class TimImage:
    def __init__(self):
        self.bpp = 0
        self.has_clut = False
        self.clut = []
        self.width = 0
        self.height = 0
        self.image = None
        self.file_path = None

    def load(self, path):
        """Load a TIM file"""
        self.file_path = path

        with open(path, "rb") as f:
            data = f.read()

        # Check magic number
        if len(data) < 8:
            raise ValueError("File too small to be TIM")
        
        magic = struct.unpack("<I", data[0:4])[0]
        if magic != 0x00000010:
            raise ValueError(f"Not a valid TIM file (magic: {hex(magic)})")

        # Parse flags
        flags = struct.unpack("<I", data[4:8])[0]
        self.has_clut = bool(flags & 0x08)
        bpp_flag = flags & 0x03

        if bpp_flag == 0:
            self.bpp = 4
        elif bpp_flag == 1:
            self.bpp = 8
        elif bpp_flag == 2:
            self.bpp = 16
        else:
            raise ValueError(f"Unsupported BPP flag: {bpp_flag}")

        offset = 8

        # Load color lookup table if present
        if self.has_clut:
            if offset + 4 > len(data):
                raise ValueError("Invalid CLUT block")
            
            clut_size = struct.unpack("<I", data[offset:offset+4])[0]
            if offset + clut_size > len(data):
                raise ValueError("CLUT block extends beyond file")
            
            clut_start = offset + 12
            num_colors = (clut_size - 12) // 2
            
            self.clut = []
            for i in range(num_colors):
                color_offset = clut_start + i * 2
                color_word = struct.unpack("<H", data[color_offset:color_offset+2])[0]
                rgb = self._decode5551(color_word)
                self.clut.append(rgb)
            
            offset += clut_size

        # Load image data block
        if offset + 12 > len(data):
            raise ValueError("Invalid image block header")
        
        img_size = struct.unpack("<I", data[offset:offset+4])[0]
        x, y, w16, h16 = struct.unpack("<4H", data[offset+4:offset+12])
        
        # w16 and h16 are texture memory dimensions (in 16-bit word units)
        # Calculate actual pixel dimensions based on BPP
        if self.bpp == 4:
            # w16 is number of 16-bit words per scanline
            # Each word holds 4 pixels (4 bits per pixel)
            px_width = w16 * 4
        elif self.bpp == 8:
            # w16 is number of 16-bit words per scanline
            # Each word holds 2 pixels (8 bits per pixel)
            px_width = w16 * 2
        else:  # 16-bit
            # w16 is number of 16-bit words per scanline
            # Each word holds 1 pixel (16 bits per pixel)
            px_width = w16
        
        self.width = px_width
        self.height = h16
        
        pixel_data_start = offset + 12
        pixel_data_size = img_size - 12
        
        if pixel_data_start + pixel_data_size > len(data):
            raise ValueError("Pixel data extends beyond file")
        
        raw_pixels = data[pixel_data_start:pixel_data_start + pixel_data_size]
        
        # Decode pixels
        self.image = self._decode_pixels(raw_pixels, self.width, self.height, self.bpp)

    def _decode5551(self, color_word):
        """Decode a 5551 color word to RGB"""
        r = ((color_word >> 0) & 0x1F) << 3
        g = ((color_word >> 5) & 0x1F) << 3
        b = ((color_word >> 10) & 0x1F) << 3
        return (r, g, b)

    def _encode5551(self, r, g, b):
        """Encode RGB to 5551 color word"""
        r5 = (r >> 3) & 0x1F
        g5 = (g >> 3) & 0x1F
        b5 = (b >> 3) & 0x1F
        return (b5 << 10) | (g5 << 5) | r5

    def _decode_pixels(self, raw_data, width, height, bpp):
        """Decode raw pixel data based on bit depth"""
        if bpp == 16:
            return self._decode_16bit(raw_data, width, height)
        elif bpp == 8:
            return self._decode_8bit(raw_data, width, height)
        elif bpp == 4:
            return self._decode_4bit(raw_data, width, height)
        else:
            raise ValueError(f"Unsupported BPP: {bpp}")

    def _decode_16bit(self, raw_data, width, height):
        """Decode 16-bit direct color - matching pPainter algorithm exactly"""
        # pPainter reads sequentially, one word per pixel
        pixel_data = []
        offset = 0
        
        for y in range(height):
            for x in range(width):
                if offset + 1 < len(raw_data):
                    color_word = struct.unpack("<H", raw_data[offset:offset+2])[0]
                    r = (color_word >> 0) & 0x1F
                    g = (color_word >> 5) & 0x1F
                    b = (color_word >> 10) & 0x1F
                    # Expand 5-bit to 8-bit
                    r = (r << 3) | (r >> 2)
                    g = (g << 3) | (g >> 2)
                    b = (b << 3) | (b >> 2)
                    pixel_data.append((r, g, b))
                else:
                    pixel_data.append((0, 0, 0))
                offset += 2
        
        img = Image.new("RGB", (width, height))
        img.putdata(pixel_data)
        return img

    def _decode_8bit(self, raw_data, width, height):
        """Decode 8-bit paletted color - matching pPainter algorithm exactly"""
        # Create palette
        if not self.clut:
            palette = list(range(256)) * 3
        else:
            palette = []
            for r, g, b in self.clut:
                palette.extend([r, g, b])
            while len(palette) < 768:
                palette.extend([0, 0, 0])
        
        # pPainter reads in words (16-bit chunks) and extracts 2 pixels per word
        px_width = width
        w16 = (width + 1) // 2  # Number of 16-bit words needed per scanline
        
        pixel_indices = []
        offset = 0
        
        for y in range(height):
            for x in range(w16):
                if offset + 1 < len(raw_data):
                    word = struct.unpack("<H", raw_data[offset:offset+2])[0]
                else:
                    word = 0
                offset += 2
                
                # Extract 2 pixels from this word
                lo = word & 0xFF
                hi = (word >> 8) & 0xFF
                pixel_indices.append(lo)
                pixel_indices.append(hi)
        
        # Trim to exact dimensions
        pixel_indices = pixel_indices[:width * height]
        
        img = Image.new("P", (width, height))
        img.putpalette(palette)
        img.putdata(pixel_indices)
        return img

    def _decode_4bit(self, raw_data, width, height):
        """Decode 4-bit paletted color - matching pPainter algorithm exactly"""
        # Create palette
        if not self.clut:
            palette = list(range(16)) * 3
        else:
            palette = []
            for r, g, b in self.clut:
                palette.extend([r, g, b])
            while len(palette) < 48:
                palette.extend([0, 0, 0])
        
        # pPainter reads in words (16-bit chunks) and extracts 4 pixels per word
        # Each pixel is 4 bits, so: pixels[0:4] come from shifts 0,4,8,12
        px_width = width
        w16 = (width + 3) // 4  # Number of 16-bit words needed per scanline
        
        pixel_indices = []
        offset = 0
        
        for y in range(height):
            for x in range(w16):
                if offset + 1 < len(raw_data):
                    word = struct.unpack("<H", raw_data[offset:offset+2])[0]
                else:
                    word = 0
                offset += 2
                
                # Extract 4 pixels from this word (shifts 0, 4, 8, 12)
                for i in range(4):
                    idx = (word >> (4 * i)) & 0x0F
                    pixel_indices.append(idx)
        
        # Trim to exact dimensions
        pixel_indices = pixel_indices[:width * height]
        
        img = Image.new("P", (width, height))
        img.putpalette(palette)
        img.putdata(pixel_indices)
        return img

    def encode(self):
        """Encode the image back to raw pixel data"""
        if self.image is None:
            raise ValueError("No image to encode")
        
        if self.bpp == 16:
            return self._encode_16bit()
        elif self.bpp == 8:
            return self._encode_8bit()
        elif self.bpp == 4:
            return self._encode_4bit()
        else:
            raise ValueError(f"Unsupported BPP: {self.bpp}")

    def _encode_16bit(self):
        """Encode to 16-bit direct color"""
        raw = bytearray()
        
        if self.image.mode != "RGB":
            img = self.image.convert("RGB")
        else:
            img = self.image
        
        for pixel in img.getdata():
            r, g, b = pixel
            color_word = self._encode5551(r, g, b)
            raw.extend(struct.pack("<H", color_word))
        
        return bytes(raw)

    def _encode_8bit(self):
        """Encode to 8-bit paletted color"""
        raw = bytearray()
        
        if self.image.mode == "P":
            raw.extend(self.image.tobytes())
        else:
            img = self.image.quantize(colors=256)
            raw.extend(img.tobytes())
        
        return bytes(raw)

    def _encode_4bit(self):
        """Encode to 4-bit paletted color"""
        raw = bytearray()
        
        if self.image.mode == "P":
            pixel_data = list(self.image.getdata())
        else:
            img = self.image.quantize(colors=16)
            pixel_data = list(img.getdata())
        
        for i in range(0, len(pixel_data), 2):
            low = pixel_data[i] & 0x0F
            high = (pixel_data[i+1] & 0x0F) if i+1 < len(pixel_data) else 0
            byte_val = low | (high << 4)
            raw.append(byte_val)
        
        return bytes(raw)

    def build_file(self):
        """Build complete TIM file data"""
        file_data = bytearray()
        
        file_data.extend(struct.pack("<I", 0x00000010))
        
        flags = 0
        if self.has_clut:
            flags |= 0x08
        flags |= (self.bpp == 4 and 0) or (self.bpp == 8 and 1) or (self.bpp == 16 and 2)
        file_data.extend(struct.pack("<I", flags))
        
        if self.has_clut and self.clut:
            clut_data = bytearray()
            num_colors = len(self.clut)
            clut_size = 12 + num_colors * 2
            clut_data.extend(struct.pack("<I", clut_size))
            clut_data.extend(struct.pack("<HHHH", 0, 0, num_colors, 1))
            
            for r, g, b in self.clut:
                color_word = self._encode5551(r, g, b)
                clut_data.extend(struct.pack("<H", color_word))
            
            file_data.extend(clut_data)
        
        pixel_data = self.encode()
        img_block = bytearray()
        img_block_size = 12 + len(pixel_data)
        img_block.extend(struct.pack("<I", img_block_size))
        img_block.extend(struct.pack("<HHHH", 0, 0, self.width, self.height))
        img_block.extend(pixel_data)
        
        file_data.extend(img_block)
        
        return bytes(file_data)

    def save(self, path):
        """Save image as TIM file"""
        if self.image is None:
            raise ValueError("No image to save")
        
        self.width = self.image.width
        self.height = self.image.height
        
        data = self.build_file()
        with open(path, "wb") as f:
            f.write(data)
        
        self.file_path = path
