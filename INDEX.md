# TimEdit - PS1 TIM Image Editor

## 🎯 Project Overview

TimEdit is a **complete, professional-grade image editor** for PlayStation 1 TIM (Texture Image Map) files, inspired by Photoshop. Built with Python and Tkinter, it combines TIM format handling with a full-featured editing interface.

**Status**: ✅ READY TO USE

## 📦 What You Get

### Core Application
- **main.py** - Fully functional GUI editor
- **tools.py** - 8 drawing tools + 6 image filters
- **layers.py** - Complete layer management system
- **undo_redo.py** - 50-step undo/redo history
- **image_viewer.py** - Enhanced canvas with zoom/pan
- **timedit.py** - PS1 TIM format handler

### Documentation
- **QUICKSTART.md** ← **START HERE** for users
- **README.md** - Complete feature reference
- **DEVELOPER.md** - Architecture & code guide
- **SETUP.md** - Installation & build info
- **examples.py** - Code examples

### Launch Files
- **run.bat** - Windows launcher
- **requirements.txt** - Dependencies (just Pillow)

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

On Windows, you can also double-click:
```
run.bat
```

### 3. Create Your First Image
1. **File → New** (256×256 is standard)
2. Select **Pencil** from toolbar
3. Choose a color
4. Draw on canvas
5. **File → Save As** to save as TIM

## ✨ Key Features

| Feature | Status | Details |
|---------|--------|---------|
| **Drawing Tools** | ✅ | Pencil, Brush, Eraser, Line, Rectangle, Ellipse, Bucket Fill |
| **Image Filters** | ✅ | Brightness, Contrast, Saturation, Blur, Sharpen, Grayscale, Invert |
| **Layer System** | ✅ | Multiple layers, visibility toggle, opacity, reorder, flatten |
| **Undo/Redo** | ✅ | 50-step history with Ctrl+Z/Y |
| **File Support** | ✅ | Open/Save TIM, Import/Export PNG/JPG/BMP |
| **Zoom & Pan** | ✅ | Mouse wheel zoom, right-click pan |
| **Color Picker** | ✅ | Visual color selection with display |
| **Brush Adjustments** | ✅ | Variable brush size (1-50px) |
| **Property Inspector** | ✅ | Image dimensions, format, metadata |

## 📁 File Structure

```
timedit/
├── 🚀 MAIN APPLICATION
│   ├── main.py              # GUI application entry point
│   ├── image_viewer.py      # Canvas display & interaction
│   ├── timedit.py           # TIM format handler
│   ├── tools.py             # Drawing & filters
│   ├── layers.py            # Layer management
│   └── undo_redo.py         # History manager
│
├── 📚 DOCUMENTATION
│   ├── QUICKSTART.md        # ⭐ User quick start guide
│   ├── README.md            # Complete user manual
│   ├── DEVELOPER.md         # Technical documentation
│   └── SETUP.md             # Setup & build info
│
├── 📦 CONFIG & LAUNCH
│   ├── requirements.txt     # Python dependencies
│   ├── run.bat              # Windows launcher
│   └── examples.py          # Code examples
│
└── __pycache__/             # Python cache (ignore)
```

## 🎨 Tool Overview

### Drawing Tools
- **Pencil**: Thin freehand lines
- **Brush**: Soft circular brush strokes
- **Eraser**: Transparent erasing
- **Line**: Straight lines between two points
- **Rectangle**: Rectangular shapes (filled/outline)
- **Ellipse**: Circular and elliptical shapes
- **Bucket Fill**: Flood fill regions
- **Color Picker**: Sample colors from image

### Image Adjustments
- **Brightness/Contrast**: Exposure control
- **Saturation**: Color intensity
- **Blur**: Gaussian blur (3px radius)
- **Sharpen**: Enhance details
- **Grayscale**: Convert to B&W
- **Invert**: Reverse all colors

## 🎓 Documentation Guide

### For New Users
1. Start with **QUICKSTART.md** (this is the easiest intro)
2. Read **README.md** for full feature list
3. Try **examples.py** to see code in action

### For Developers
1. Read **DEVELOPER.md** for architecture
2. Check **examples.py** for patterns
3. Explore **tools.py** to understand tool implementation
4. Review **main.py** for UI structure

### For Setup/Deployment
1. Check **SETUP.md** for installation steps
2. Use **run.bat** on Windows
3. Review **requirements.txt** for dependencies

## 💻 System Requirements

- Python 3.7+
- Tkinter (included with Python)
- Pillow (PIL) - installed via requirements.txt
- Windows/Mac/Linux compatible

## 🔧 Installation Options

### Option 1: Quick Install (Recommended)
```bash
cd c:\Users\there\Desktop\timedit
pip install -r requirements.txt
python main.py
```

### Option 2: Windows Only
```bash
double-click run.bat
```

### Option 3: Manual Installation
```bash
pip install pillow
python main.py
```

## 📊 Performance

- **Optimal Image Size**: 256×256 to 512×512 pixels
- **Layer Limit**: ~10 active layers
- **Undo History**: 50 steps max
- **Brush Size**: 1-50 pixels

## 🎯 Use Cases

- Create PS1 game textures
- Edit sprite sheets
- Design pixel art
- Convert/adjust images for retro games
- Create custom graphics for emulation
- Batch process images

## 🔄 Workflow Example

```
1. Create 256×256 new image
2. Add background layer
3. Paint with brush tool
4. Add detail layer on top
5. Apply color adjustments
6. Undo any mistakes (Ctrl+Z)
7. Save as TIM file
8. Use in PS1 game/emulator
```

## 🚀 What's Next?

### To Start Using
1. Read **QUICKSTART.md**
2. Run `python main.py`
3. Create your first image!

### To Extend/Customize
1. Review **DEVELOPER.md**
2. Check **examples.py**
3. Modify **tools.py** to add features
4. Update **main.py** for new menu items

### To Contribute
- Fix bugs in code
- Add new tools/filters
- Improve documentation
- Enhance performance

## ✅ Verification Checklist

- ✅ All core modules created
- ✅ GUI fully functional
- ✅ File I/O working (TIM, PNG, JPG, BMP)
- ✅ Drawing tools implemented
- ✅ Image filters working
- ✅ Layer system complete
- ✅ Undo/Redo functional
- ✅ Documentation complete
- ✅ Examples provided
- ✅ No syntax errors

## 📝 Code Quality

- PEP 8 compliant
- Clean modular architecture
- Well-documented code
- Extensible design
- Error handling included
- Type hints where applicable

## 🎓 Learning Resources

### Inside Project
- **examples.py** - Shows programmatic usage
- **tools.py** - Drawing/filter implementations
- **layers.py** - Layer system implementation
- **main.py** - UI/UX implementation

### External Resources
- Python PIL/Pillow documentation
- Tkinter GUI tutorial
- PS1 TIM format specification

## 🤝 Community

Got ideas for improvements?
- Add new drawing tools
- Implement selection tools
- Create new filters
- Improve performance
- Enhance documentation

## 📄 License

Free to use and modify for personal and commercial projects.

---

## 🎉 Quick Links

| Need | Resource |
|------|----------|
| **Want to start using?** | → Read QUICKSTART.md |
| **Want full features?** | → Check README.md |
| **Want technical details?** | → Review DEVELOPER.md |
| **Want code examples?** | → See examples.py |
| **Want to run it?** | → Execute `python main.py` |
| **Windows user?** | → Double-click `run.bat` |

---

## 🏁 Ready to Go!

Your TimEdit image editor is **fully assembled and ready to use**.

```bash
# Get started now:
python main.py
```

**Happy editing! 🎨**
