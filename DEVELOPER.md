# TimEdit - Developer Guide

## Project Overview

TimEdit is a complete Photoshop-like image editor for PS1 TIM files. It combines TIM file format handling with a full-featured GUI editor built with Python and Tkinter.

## Architecture

### Core Modules

#### `timedit.py` - TIM Format Handler
Handles PlayStation 1 TIM file format:
- **Load**: Parse TIM binary format (magic bytes, flags, color palette, pixel data)
- **Save**: Encode back to TIM binary format
- **Decode**: Convert TIM pixels to PIL Image (supports 4-bit, 8-bit, 16-bit)
- **Encode**: Convert PIL Image back to TIM pixel format
- **Color Support**: 5551 RGB color format for 16-bit images

Key Classes:
- `TimImage`: Main interface for TIM file operations

#### `image_viewer.py` - Canvas & Display
Tkinter canvas subclass for image display and interaction:
- **Zoom**: Mouse wheel zoom (10% per step)
- **Pan**: Right-click drag to move around image
- **Drawing Integration**: Coordinates conversion from screen to image space
- **Event Handling**: Mouse events routed to tool callbacks

Key Classes:
- `ImageViewer(tk.Canvas)`: Main display widget

#### `tools.py` - Drawing & Filters
Drawing and image processing operations:
- **DrawingTools**: Pencil, brush, eraser, shapes, flood fill
- **ImageAdjustments**: Brightness, contrast, saturation, blur, sharpen, grayscale, invert

Key Classes:
- `DrawingTools`: Drawing operations using PIL ImageDraw
- `ImageAdjustments`: Static methods for image filters

#### `layers.py` - Layer Management
Full layer system with compositing:
- **Layer**: Individual layer with opacity and visibility
- **LayerStack**: Manages multiple layers
- **Flatten**: Composites layers into single image
- **Blending**: Opacity support and layer stacking

Key Classes:
- `Layer`: Single layer representation
- `LayerStack`: Collection of layers

#### `undo_redo.py` - History Management
Undo/redo system with configurable history depth:
- **State Saving**: Stores image copies in history
- **Undo/Redo**: Navigate through history
- **History Limit**: Max 50 states to save memory

Key Classes:
- `UndoRedoManager`: Manages undo/redo state

#### `main.py` - Main Application
Complete Tkinter GUI application:
- **Menu System**: File, Edit, Image, Help menus
- **Toolbar**: Tool selection, color picker, brush size
- **Layers Panel**: Layer management UI
- **Canvas**: Main image editing area
- **Properties Panel**: Image information display

Key Classes:
- `TimEditorApp`: Main application window

## Data Flow

```
User Input (UI)
    ↓
Tool Handler (main.py)
    ↓
DrawingTools or ImageAdjustments
    ↓
Layer Image (PIL Image)
    ↓
LayerStack.flatten() or get_merged_image()
    ↓
ImageViewer.set_image()
    ↓
Screen Display
```

## File I/O

### Opening Files
1. User selects file via dialog
2. `TimImage.load(path)` parses binary TIM format
3. Layers created with loaded image as background
4. Image displayed in viewer

### Saving Files
1. Layers are flattened to single image
2. `TimImage.save(path)` encodes to TIM binary format
3. File written to disk

## Color Handling

### 16-bit TIM Format (5551)
- Red: bits 0-4 (5 bits)
- Green: bits 5-9 (5 bits)
- Blue: bits 10-14 (5 bits)
- Alpha: bit 15 (1 bit)

Conversion:
- 8-bit value → 5-bit: `value >> 3`
- 5-bit value → 8-bit: `value << 3`

## Usage Examples

### Programmatic Image Editing
```python
from timedit import TimImage
from tools import DrawingTools

tim = TimImage()
tim.load('input.tim')

tools = DrawingTools(tim.image)
tools.brush(100, 100, (255, 0, 0), size=10)

tim.save('output.tim')
```

### Creating New Image
```python
from PIL import Image
from timedit import TimImage

img = Image.new('RGB', (256, 256), (255, 255, 255))
tim = TimImage()
tim.image = img
tim.width = 256
tim.height = 256
tim.bpp = 16
tim.save('new.tim')
```

### Layer Workflow
```python
from layers import LayerStack
from tools import DrawingTools

stack = LayerStack(256, 256)
stack.add_layer("Background", bg_image)
stack.add_layer("Drawing")

layer = stack.get_active_layer()
tools = DrawingTools(layer.image)
tools.brush(100, 100, (255, 0, 0))

merged = stack.get_merged_image()
```

## Performance Considerations

- **Image Size**: Larger images slow down operations. Optimal: ≤512×512
- **Layer Count**: Each layer requires memory. Limit to ~10 active layers
- **History**: 50-step history uses significant memory. Adjust if needed
- **Zoom**: Display zoom is efficient (PIL resize with LANCZOS)
- **Drawing**: Large brush sizes (>50px) may be slow on large images

## Extending the Editor

### Adding New Tools
1. Add method to `DrawingTools` in `tools.py`
2. Add button to toolbar in `_create_toolbar()`
3. Add case to `on_canvas_tool()` event handler

### Adding New Filters
1. Add static method to `ImageAdjustments` in `tools.py`
2. Add menu item in `_create_menu()`
3. Create adjustment dialog with parameters

### Adding New Features
- **Selection tools**: Store selection bounds, use for masked operations
- **Text tool**: Use PIL ImageFont for text rendering
- **Patterns**: Extend brush system with pattern fills
- **Animations**: Support multiple frames in TIM sequences

## Known Limitations

- 4-bit and 8-bit TIM files lose color information when converted to 16-bit
- No support for PS1 TIM animations (multi-frame)
- Limited to TIM format; no support for other PS1 texture formats
- Layer blend modes only support opacity (no multiply, screen, etc.)
- No tablet/pen pressure support

## Dependencies

- `pillow` (PIL): Image processing
- `tkinter`: GUI framework (usually included with Python)

## Testing

Run examples:
```bash
python examples.py
```

This will create sample TIM files demonstrating:
- Basic drawing operations
- Image adjustments
- Multi-layer workflows

## Future Roadmap

1. **Selection Tools**: Rectangle/free select, select by color
2. **Text Tool**: Add text overlays with custom fonts
3. **Transform Tools**: Rotate, scale, skew, perspective
4. **Advanced Blend Modes**: Multiply, screen, overlay, etc.
5. **Brush System**: Custom brushes, brush presets
6. **Animation Support**: Frame editor for TIM sequences
7. **Batch Processing**: Batch resize, convert, adjust
8. **Plugin System**: Load external tools
9. **Version Control**: Compare/merge image versions
10. **Collaboration**: Real-time collaborative editing

## Code Style

- Python 3.7+
- PEP 8 compliant
- Descriptive variable names
- Type hints where applicable
- Docstrings for public methods
