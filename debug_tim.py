"""Debug TIM file structure"""
import struct
import os

# Find a TIM file to analyze
tim_files = [f for f in os.listdir('.') if f.endswith('.tim')]

if not tim_files:
    print("No TIM files found")
    exit(1)

tim_file = tim_files[0]
print(f"Analyzing: {tim_file}\n")

with open(tim_file, 'rb') as f:
    data = f.read()

magic = struct.unpack('<I', data[0:4])[0]
flags = struct.unpack('<I', data[4:8])[0]
bpp_bits = flags & 0x03

if bpp_bits == 0:
    bpp = 4
elif bpp_bits == 1:
    bpp = 8
else:
    bpp = 16

print(f'BPP: {bpp}')
print(f'Has CLUT: {bool(flags & 0x08)}')

offset = 8
if flags & 0x08:
    clut_size = struct.unpack('<I', data[offset:offset+4])[0]
    print(f'CLUT size: {clut_size} bytes')
    offset += clut_size

img_size = struct.unpack('<I', data[offset:offset+4])[0]
x, y, w, h = struct.unpack('<4H', data[offset+4:offset+12])

print(f'\nImage dimensions: {w}x{h}')
print(f'Image block size: {img_size} bytes (including 12-byte header)')
print(f'Pixel data size: {img_size - 12} bytes')

pixel_data = data[offset+12:offset+img_size]

print(f'\nFirst 96 bytes of pixel data (hex):')
for i in range(0, min(96, len(pixel_data)), 16):
    hex_str = ' '.join(f'{b:02x}' for b in pixel_data[i:i+16])
    print(f'  {i:3d}: {hex_str}')

if bpp == 4:
    print(f'\nFor 4-bit image {w}x{h}:')
    print(f'  Pixels per row: {w}')
    print(f'  Bytes per row (linear): {(w+1)//2}')
    print(f'  Total bytes needed: {((w+1)//2) * h}')
    print(f'  Actual bytes: {len(pixel_data)}')
    
    # Try to unpack first row different ways
    print(f'\nFirst row pixels (linear, low nibble first):')
    row_bytes = (w + 1) // 2
    row_data = pixel_data[:row_bytes]
    pixels = []
    for byte_val in row_data:
        pixels.append(byte_val & 0x0F)
        pixels.append((byte_val >> 4) & 0x0F)
    print(f'  {pixels[:w]}')
    
    print(f'\nFirst row pixels (reversed, high nibble first):')
    pixels = []
    for byte_val in row_data:
        pixels.append((byte_val >> 4) & 0x0F)
        pixels.append(byte_val & 0x0F)
    print(f'  {pixels[:w]}')
