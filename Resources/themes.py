import tkinter as tk
from ttkbootstrap import Style

THEMES = {
    "Current (Black & Yellow)": {
        "bg": "#2c3e50",
        "fg": "white",
        "accent": "#FFD700",
        "button_bg": "#34495e",
        "button_fg": "white",
        "button_active_bg": "#2980b9",
        "button_active_fg": "white",
        "meter_bg": "#3498db",
        "progressbar_bg": "#2c3e50",
        "canvas_bg": "#2c3e50",
        "input_bg": "#4a4a4a",
        "input_fg": "white",
        "hover_bg": "#3498db",
        "dropdown_bg": "#34495e",
        "dropdown_fg": "white",
        "dropdown_highlight": "#FFD700"
    },
    "Light Mode": {
        "bg": "#ffffff",
        "fg": "#2c3e50",
        "accent": "#4299e1",
        "button_bg": "#e3f2fd",
        "button_fg": "#1a365d",
        "button_active_bg": "#90cdf4",
        "button_active_fg": "#1a365d",
        "meter_bg": "#4299e1",
        "progressbar_bg": "#e2e8f0",
        "canvas_bg": "#ffffff",
        "input_bg": "#f7fafc",
        "input_fg": "#2d3748",
        "hover_bg": "#bee3f8",
        "dropdown_bg": "#f7fafc",
        "dropdown_fg": "#2d3748",
        "dropdown_highlight": "#4299e1"
    },
    "Dark Mode": {
        "bg": "#1a202c",
        "fg": "#a0aec0",
        "accent": "#805ad5",
        "button_bg": "#2d3748",
        "button_fg": "#e2e8f0",
        "button_active_bg": "#4a5568",
        "button_active_fg": "#ffffff",
        "meter_bg": "#805ad5",
        "progressbar_bg": "#2d3748",
        "canvas_bg": "#171923",
        "input_bg": "#2d3748",
        "input_fg": "#e2e8f0",
        "hover_bg": "#4a5568",
        "dropdown_bg": "#2d3748",
        "dropdown_fg": "#e2e8f0",
        "dropdown_highlight": "#805ad5"
    },
    "Nature Mode": {
        "bg": "#2F4F4F",
        "fg": "#98FB98",
        "accent": "#32CD32",
        "button_bg": "#3CB371",
        "button_fg": "#F0FFF0",
        "button_active_bg": "#006400",
        "button_active_fg": "#F0FFF0",
        "meter_bg": "#32CD32",
        "progressbar_bg": "#2F4F4F",
        "canvas_bg": "#1B4D3E",
        "input_bg": "#3CB371",
        "input_fg": "#F0FFF0",
        "hover_bg": "#006400",
        "dropdown_bg": "#3CB371",
        "dropdown_fg": "#F0FFF0",
        "dropdown_highlight": "#32CD32"
    },
    "Neon Mode": {
        "bg": "#000000",
        "fg": "#00ff00",
        "accent": "#ff00ff",
        "button_bg": "#1a1a1a",
        "button_fg": "#00ff00",
        "button_active_bg": "#333333",
        "button_active_fg": "#ff00ff",
        "meter_bg": "#ff00ff",
        "progressbar_bg": "#1a1a1a",
        "canvas_bg": "#000000",
        "input_bg": "#1a1a1a",
        "input_fg": "#00ff00",
        "hover_bg": "#333333",
        "dropdown_bg": "#1a1a1a",
        "dropdown_fg": "#00ff00",
        "dropdown_highlight": "#ff00ff"
    },
    "Sunset Mode": {
        "bg": "#2C0E37",
        "fg": "#FFB6C1",
        "accent": "#FF6B6B",
        "button_bg": "#4A1259",
        "button_fg": "#FFB6C1",
        "button_active_bg": "#6B1B7B",
        "button_active_fg": "#FFC0CB",
        "meter_bg": "#FF6B6B",
        "progressbar_bg": "#2C0E37",
        "canvas_bg": "#1E0B26",
        "input_bg": "#4A1259",
        "input_fg": "#FFB6C1",
        "hover_bg": "#6B1B7B",
        "dropdown_bg": "#4A1259",
        "dropdown_fg": "#FFB6C1",
        "dropdown_highlight": "#FF6B6B"
    },
    "Ocean Mode": {
        "bg": "#001B48",
        "fg": "#00FFFF",
        "accent": "#1E90FF",
        "button_bg": "#002D5A",
        "button_fg": "#87CEEB",
        "button_active_bg": "#004080",
        "button_active_fg": "#00FFFF",
        "meter_bg": "#1E90FF",
        "progressbar_bg": "#001B48",
        "canvas_bg": "#001433",
        "input_bg": "#002D5A",
        "input_fg": "#87CEEB",
        "hover_bg": "#004080",
        "dropdown_bg": "#002D5A",
        "dropdown_fg": "#87CEEB",
        "dropdown_highlight": "#1E90FF"
    }
}

class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.current_theme = "Current (Black & Yellow)"
        
    def apply_theme(self, theme_name):
        if theme_name not in THEMES:
            return
            
        theme = THEMES[theme_name]
        self.current_theme = theme_name
        
        # Update main window background
        self.app.root.configure(bg=theme["bg"])
        
        # Update style configuration
        style = Style()
        style.configure(".", 
                       background=theme["bg"], 
                       foreground=theme["fg"])
        
        # Configure Frame style
        style.configure("TFrame", 
                       background=theme["bg"])
        
        # Configure Label style
        style.configure("TLabel", 
                       background=theme["bg"], 
                       foreground=theme["fg"])
        
        # Configure Button style
        style.configure("TButton", 
                       background=theme["button_bg"], 
                       foreground=theme["button_fg"])
        style.map("TButton",
                 background=[("active", theme["button_active_bg"])],
                 foreground=[("active", theme["button_active_fg"])])
        
        # Configure Progressbar style
        style.configure("depression.Horizontal.TProgressbar", 
                       troughcolor=theme["progressbar_bg"],
                       background=theme["meter_bg"])
        
        # Update canvas colors
        self.app.canvas.configure(bg=theme["canvas_bg"])
        self.app.menu_button.configure(bg=theme["canvas_bg"])
        
        # Update circle colors
        self.app.canvas.itemconfig(self.app.circle, 
                                 fill=theme["accent"], 
                                 outline=theme["accent"])
        self.app.menu_button.itemconfig(self.app.menu_circle, 
                                      fill=theme["accent"], 
                                      outline=theme["accent"])
        
        # Update text input
        self.app.text_input.configure(
            bg=theme["input_bg"], 
            fg=theme["input_fg"],
            insertbackground=theme["fg"]  # Cursor color
        )
        
        # Configure Combobox style
        style.configure("TCombobox",
                       fieldbackground=theme["dropdown_bg"],
                       foreground=theme["dropdown_fg"],
                       arrowcolor=theme["dropdown_fg"],
                       selectbackground=theme["dropdown_highlight"],
                       selectforeground=theme["dropdown_fg"])
        
        style.map("TCombobox",
                 fieldbackground=[("readonly", theme["dropdown_bg"])],
                 selectbackground=[("readonly", theme["dropdown_highlight"])],
                 selectforeground=[("readonly", theme["dropdown_fg"])],
                 background=[("readonly", theme["dropdown_bg"])],
                 foreground=[("readonly", theme["dropdown_fg"])])
        
        # Update any open windows
        self._update_child_windows(theme)
        
    def _update_child_windows(self, theme):
        """Update all child windows with the new theme"""
        # Update all toplevel windows
        for window in self.app.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.configure(bg=theme["bg"])
                
                # Update all frames and labels in the window
                for child in window.winfo_children():
                    self._update_widget_theme(child, theme)
                        
        # Update any open specialty windows
        if hasattr(self.app, 'music_player') and self.app.music_player:
            for widget in self.app.music_player.winfo_children():
                self._update_widget_theme(widget, theme)
                
    def _update_widget_theme(self, widget, theme):
        """Recursively update a widget and its children with the new theme"""
        if isinstance(widget, (ttk.Frame, ttk.Label)):
            widget.configure(background=theme["bg"])
        elif isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg=theme["canvas_bg"])
        elif isinstance(widget, ttk.Entry):
            widget.configure(
                fieldbackground=theme["input_bg"]
            )
        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=theme["input_bg"],
                fg=theme["input_fg"],
                insertbackground=theme["fg"]
            )
        elif isinstance(widget, tk.Button):
            widget.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["button_active_bg"],
                activeforeground=theme["button_active_fg"]
            )
        elif isinstance(widget, ttk.Combobox):
            widget.configure(
                background=theme["dropdown_bg"],
                foreground=theme["dropdown_fg"],
                fieldbackground=theme["dropdown_bg"]
            )
            
        # Recursively update children
        for child in widget.winfo_children():
            self._update_widget_theme(child, theme)