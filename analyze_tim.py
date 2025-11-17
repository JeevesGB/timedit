import struct
with open('afa7n.tim', 'rb') as f:
    data = f.read()
magic = struct.unpack('<I', data[0:4])[0]
flags = struct.unpack('<I', data[4:8])[0]
print(f'Magic: {hex(magic)}')
print(f'Flags: {bin(flags)}')
bpp_bits = flags & 0x03
if bpp_bits == 0:
    bpp = 4
elif bpp_bits == 1:
    bpp = 8
else:
    bpp = 16
print(f'BPP: {bpp}')
print(f'Has CLUT: {bool(flags & 0x08)}')
print(f'File size: {len(data)} bytes')

offset = 8
if flags & 0x08:
    clut_size = struct.unpack('<I', data[offset:offset+4])[0]
    print(f'CLUT size: {clut_size}')
    offset += clut_size

img_size = struct.unpack('<I', data[offset:offset+4])[0]
x, y, w, h = struct.unpack('<4H', data[offset+4:offset+12])
print(f'Image: {w}x{h} at {x},{y}')
print(f'Image data size: {img_size} bytes')
print(f'Expected pixels: {w*h}')
if bpp == 4:
    expected_bytes = (w*h + 1) // 2
    print(f'Expected bytes for 4-bit: {expected_bytes}')
