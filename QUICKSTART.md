# TimEdit Getting Started Guide

## 🎨 Welcome to TimEdit!

TimEdit is a professional image editor for PS1 TIM files with features like Photoshop!

## ⚡ Quick Start (2 minutes)

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Run
```bash
python main.py
```

### Step 3: Create Your First Image
1. Click **File → New**
2. Enter dimensions (256×256 is standard for PS1)
3. Click **Create**
4. Select **Pencil** from toolbar
5. Click color box to choose a color
6. Draw on the canvas!
7. **File → Save As** to save as TIM

## 🖌️ Toolbar Guide

| Tool | Purpose | Usage |
|------|---------|-------|
| **Pencil** | Draw thin lines | Click and drag |
| **Brush** | Paint with soft edges | Click to paint |
| **Eraser** | Remove content | Click to erase |
| **Line** | Draw straight lines | Click start, click end |
| **Rectangle** | Draw boxes | Click and drag |
| **Ellipse** | Draw circles/ovals | Click and drag |
| **Bucket Fill** | Fill regions | Click on area |
| **Color Picker** | Sample colors | Click on color |

## 🎯 Common Tasks

### Opening a TIM File
1. **File → Open TIM**
2. Select your .tim file
3. Image appears in canvas
4. Make edits
5. **File → Save** to overwrite, or **File → Save As** for new file

### Importing Other Image Formats
1. **File → Open Image**
2. Select PNG, JPG, or BMP
3. Edit as normal
4. **File → Export As** to save as PNG/JPG

### Changing Colors
1. Click the colored box in Color section
2. Select color from picker
3. Color box updates
4. All drawing tools use this color

### Adjusting Brush Size
- Use the **Brush Size** slider (1-50 pixels)
- Larger = thicker strokes
- Reset by sliding left

### Using Layers
1. Click **+ New** in Layers panel to create layer
2. Each layer is independent
3. Draw on active (highlighted) layer
4. Click eye icon area to toggle visibility
5. Drag to reorder layers
6. When done, **File → Save** flattens layers

### Applying Filters
1. **Image → [Filter Name]**
2. Adjust parameters if dialog appears
3. Click **Apply**
4. Filter applied to image

Available filters:
- Brightness/Contrast
- Saturation
- Blur
- Sharpen
- Grayscale
- Invert Colors

### Undoing Mistakes
- Press **Ctrl+Z** to undo
- Press **Ctrl+Y** to redo
- Up to 50 steps of history

### Zooming & Panning
- **Mouse Wheel**: Zoom in/out (centered on cursor)
- **Right-Click + Drag**: Pan around image
- **Scroll with Zoom**: Navigate large images

## 📐 Dimensions & Formats

### Common PS1 TIM Sizes
- **256×256** - Standard texture
- **512×256** - Wide texture
- **128×128** - Small texture
- **512×512** - Large texture

### Color Formats
- **16-bit** - Full RGB color (recommended)
- **8-bit** - 256 colors with palette
- **4-bit** - 16 colors with palette

**Tip**: Use 16-bit for best color quality!

## 🔧 Advanced Features

### Saving Different Formats

| Format | Extension | When to Use |
|--------|-----------|------------|
| TIM | .tim | PS1 games, emulators |
| PNG | .png | Web, high quality |
| JPEG | .jpg | Smaller file size |
| BMP | .bmp | Simple format |

### Layer Management
- **New Layer**: Click + New
- **Delete Layer**: Select and click - Delete
- **Merge Layers**: Export/Save flattens all
- **Layer Order**: Top = rendered last (on top)
- **Opacity**: Affects final appearance

### Selection & Editing
- **Bucket Fill**: Click to fill entire region
- **Eraser**: Makes content transparent
- **Copy Area**: Not yet implemented

## 💡 Pro Tips

1. **Always save frequently** - Use Ctrl+S or File menu
2. **Use layers** - Non-destructive editing
3. **Keep backups** - Undo is limited to 50 steps
4. **Start large** - Scale down if needed
5. **Use Ctrl+Z liberally** - Undo is your friend

## ❌ Troubleshooting

### "Not a valid TIM file"
- File is corrupted or not a real TIM
- Try opening with hex editor to verify magic bytes
- Recreate from PNG/JPG instead

### Image looks wrong
- Try adjusting brightness/contrast
- Verify original TIM format (4/8/16-bit)
- Ensure color range is correct for bit depth

### Very slow performance
- Image might be too large
- Try 256×256 or smaller
- Close other applications
- Reduce undo history limit

### Colors look wrong
- Verify bit depth (16-bit recommended)
- Try exporting and reimporting
- Check if original file is damaged

### Can't draw on image
- Make sure you have a layer selected (highlighted in Layers panel)
- Ensure layer isn't locked
- Try creating a new layer

## 📚 Learn More

- **README.md** - Full feature list
- **DEVELOPER.md** - Technical documentation
- **examples.py** - Code examples
- **SETUP.md** - Installation details

## 🚀 Getting Creative

### Project Ideas
- **Sprite Sheet**: Create custom sprites for games
- **Texture Pack**: Make textures for 3D models
- **Pixel Art**: Draw digital art
- **Game Assets**: Create UI graphics
- **Photo Edit**: Adjust and enhance images

### Workflow Example
1. Create 256×256 image
2. Use Pencil for line art
3. Use Brush to fill areas
4. Adjust Saturation for color
5. Add Eraser for transparency
6. Save as TIM for game use

## 🎓 Next Steps

1. **Experiment**: Try each tool
2. **Practice**: Create simple drawings
3. **Explore**: Use filters creatively
4. **Build**: Make actual game assets
5. **Share**: Export and show your work!

## ⚙️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Scroll Wheel | Zoom |
| Right-Click + Drag | Pan |

## 🤝 Contributing

Want to help improve TimEdit?
- Fix bugs in the code
- Add new tools
- Improve performance
- Enhance documentation

## 📝 License

Free to use and modify!

---

**Happy Editing! 🎨**

Have fun creating with TimEdit!
