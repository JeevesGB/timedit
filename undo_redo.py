from PIL import Image
import copy

class UndoRedoManager:
    """Manages undo and redo states"""
    
    def __init__(self, max_history=50):
        self.history = []
        self.current_state = 0
        self.max_history = max_history
    
    def save_state(self, image):
        """Save the current state to history"""
        # Remove any redo history after current state
        self.history = self.history[:self.current_state + 1]
        
        # Save a copy of the image
        if isinstance(image, Image.Image):
            state = image.copy()
        else:
            state = copy.deepcopy(image)
        
        self.history.append(state)
        self.current_state += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_state -= 1
    
    def undo(self):
        """Get the previous state"""
        if self.current_state > 0:
            self.current_state -= 1
            return self.history[self.current_state].copy()
        return None
    
    def redo(self):
        """Get the next state"""
        if self.current_state < len(self.history) - 1:
            self.current_state += 1
            return self.history[self.current_state].copy()
        return None
    
    def can_undo(self):
        """Check if undo is available"""
        return self.current_state > 0
    
    def can_redo(self):
        """Check if redo is available"""
        return self.current_state < len(self.history) - 1
    
    def clear(self):
        """Clear all history"""
        self.history = []
        self.current_state = 0
