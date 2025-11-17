# TimEdit - PS1 TIM Image Editor

A Photoshop-like image editor for PS1 TIM (Texture Image Map) files, written in Python with Tkinter GUI.

## Features

### Core Functionality
- **Load/Save TIM Files**: Open and save PlayStation 1 TIM format images
- **Import/Export**: Load PNG, JPG, BMP and export to standard image formats
- **Multiple Layers**: Full layer support with visibility toggles
- **Undo/Redo**: Up to 50 steps of history (Ctrl+Z, Ctrl+Y)

### Drawing Tools
- **Pencil**: Draw freehand lines with precise control
- **Brush**: Paint with soft circular brush strokes
- **Eraser**: Remove content with transparency support
- **Line**: Draw straight lines between two points
- **Rectangle**: Draw rectangular shapes (filled or outline)
- **Ellipse**: Draw elliptical/circular shapes
- **Bucket Fill**: Flood fill regions with color
- **Color Picker**: Select colors from images

### Image Adjustments
- **Brightness/Contrast**: Fine-tune image exposure
- **Saturation**: Adjust color intensity
- **Blur**: Apply Gaussian blur effects
- **Sharpen**: Enhance image details
- **Grayscale**: Convert to black and white
- **Invert**: Reverse all colors

### UI Features
- **Zoom & Pan**: Mouse wheel to zoom, right-click drag to pan
- **Layer Manager**: Create, delete, and reorder layers
- **Real-time Preview**: See changes instantly
- **Color Display**: Visual feedback of current brush color
- **Brush Size Control**: Adjustable from 1-50 pixels
- **Image Properties**: View dimension and metadata info

## Requirements

```bash
pip install pillow
```

## Installation

1. Ensure Python 3.7+ is installed
2. Install Pillow: `pip install pillow`
3. Run the application: `python main.py`

## Usage

### Opening Files
- **File → New**: Create a new blank image
- **File → Open TIM**: Load a TIM file
- **File → Open Image**: Load PNG/JPG/BMP files

### Editing
1. Select a tool from the toolbar
2. Click the color box to change brush color
3. Adjust brush size with the slider
4. Draw on the canvas
5. Use layers panel to manage multiple layers

### Keyboard Shortcuts
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo

### Saving
- **File → Save**: Save to current TIM file
- **File → Save As**: Save as new TIM file
- **File → Export As**: Export to PNG/JPG/BMP

## File Structure

```
timedit/
├── main.py              # Main application entry point
├── timedit.py           # TIM file format handler
├── image_viewer.py      # Canvas and image display
├── tools.py             # Drawing tools and filters
├── layers.py            # Layer management system
├── undo_redo.py         # Undo/redo history manager
└── README.md            # This file
```

## TIM Format Support

- **4-bit indexed**: 16 colors with palette
- **8-bit indexed**: 256 colors with palette
- **16-bit direct**: Full RGB color (5551 format)

## Tips

- Use layers to non-destructively edit complex images
- Larger images = slower operations; start small for testing
- The color picker tool lets you sample colors from anywhere
- Undo history is limited to 50 steps to save memory

## Future Enhancements

- Selection tools (rectangle select, free select)
- Text tool
- Transform tools (rotate, scale, skew)
- More blend modes
- Animation frame support
- Batch processing
- Custom brushes

## Troubleshooting

**"Not a valid TIM file"**: Ensure the file is a genuine PS1 TIM format image.

**Image looks distorted**: TIM files use specific aspect ratios for PS1 hardware. Try resizing to standard dimensions (256x256, 512x256, etc.).

**Performance issues**: Work with smaller image sizes (512x512 max recommended) for smoother operation.

## License

Free to use and modify for personal projects.
