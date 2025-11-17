"""
TimEdit Quick Start Example
Shows how to use the TIM editor programmatically
"""

from PIL import Image
from timedit import TimImage
from image_viewer import ImageViewer
from tools import DrawingTools, ImageAdjustments
from layers import LayerStack

def example_create_and_edit():
    """Example: Create a new image and perform edits"""
    
    # Create a new image
    img = Image.new('RGB', (256, 256), (255, 255, 255))
    
    # Create layer stack
    layers = LayerStack(256, 256)
    layers.add_layer("Background", img)
    
    # Draw on the active layer
    active = layers.get_active_layer()
    tools = DrawingTools(active.image)
    
    # Draw a red rectangle
    tools.rectangle(10, 10, 100, 100, (255, 0, 0), filled=True)
    
    # Draw a blue circle
    tools.ellipse(150, 150, 200, 200, (0, 0, 255), filled=True)
    
    # Get merged result
    result = layers.get_merged_image()
    
    # Save as TIM
    tim = TimImage()
    tim.image = result
    tim.width = result.width
    tim.height = result.height
    tim.bpp = 16
    tim.save('example.tim')
    
    print("Created example.tim with drawing")


def example_adjust_image():
    """Example: Load and adjust an image"""
    
    # Load TIM file
    tim = TimImage()
    tim.load('example.tim')
    
    # Apply adjustments
    adjusted = ImageAdjustments.brightness(tim.image, 1.5)
    adjusted = ImageAdjustments.contrast(adjusted, 1.2)
    adjusted = ImageAdjustments.saturation(adjusted, 0.8)
    
    # Save result
    tim.image = adjusted
    tim.save('example_adjusted.tim')
    
    print("Created example_adjusted.tim")


def example_layer_workflow():
    """Example: Work with multiple layers"""
    
    layers = LayerStack(256, 256)
    
    # Add background
    bg = Image.new('RGB', (256, 256), (200, 200, 200))
    layers.add_layer("Background", bg)
    
    # Add drawing layer
    draw_layer = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    layers.add_layer("Drawing", draw_layer)
    
    # Draw on top layer
    tools = DrawingTools(layers.layers[-1].image)
    tools.brush(128, 128, (255, 0, 0, 255), size=20)
    tools.brush(100, 100, (0, 255, 0, 255), size=20)
    
    # Flatten and save
    result = layers.get_merged_image()
    tim = TimImage()
    tim.image = result
    tim.width = 256
    tim.height = 256
    tim.bpp = 16
    tim.save('example_layers.tim')
    
    print("Created example_layers.tim with multiple layers")


if __name__ == "__main__":
    print("TimEdit Examples")
    print("================\n")
    
    try:
        example_create_and_edit()
        print()
        example_layer_workflow()
        print("\nExamples completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
