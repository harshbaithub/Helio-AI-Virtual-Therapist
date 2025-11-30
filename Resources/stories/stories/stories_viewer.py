import json
import os
import tkinter as tk
from tkinter import ttk

class StoriesViewer:
    def __init__(self, parent, stories_file):
        self.window = tk.Toplevel(parent)
        self.window.title("Motivational Stories")
        self.window.geometry("700x600")
        self.window.configure(bg="#2c3e50")
        
        self.stories_file = stories_file
        self.stories = self._load_stories()
        self.current_story = None
        self.setup_ui()
    
    def _load_stories(self):
        """Load stories from JSON file"""
        if os.path.exists(self.stories_file):
            with open(self.stories_file, 'r') as f:
                return json.load(f)['stories']
        return []
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and category selection frame
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        ttk.Label(
            top_frame,
            text="📖 Motivational Stories",
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)
        
        # Create category combobox
        categories = sorted(list(set(story['category'] for story in self.stories)))
        self.category_var = tk.StringVar()
        
        category_frame = ttk.Frame(top_frame)
        category_frame.pack(side=tk.RIGHT)
        
        ttk.Label(
            category_frame,
            text="Category:",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_combo = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=20
        )
        self.category_combo.pack(side=tk.LEFT)
        self.category_combo.bind("<<ComboboxSelected>>", self.update_stories_list)
        
        # Stories list (now using a more compact listbox)
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Split into left (story list) and right (story content) panels
        left_panel = ttk.Frame(list_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Stories listbox with scrollbar
        self.stories_listbox = tk.Listbox(
            left_panel,
            font=("Arial", 11),
            width=30,
            bg="#34495e",
            fg="white",
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.stories_listbox.pack(side=tk.LEFT, fill=tk.Y)
        
        scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.stories_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.stories_listbox.yview)
        
        # Story content panel (right side)
        right_panel = ttk.Frame(list_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Story title
        self.story_title = ttk.Label(
            right_panel,
            text="Select a story to read",
            font=("Arial", 14, "bold"),
            wraplength=400
        )
        self.story_title.pack(fill=tk.X)
        
        # Story content in a Text widget with custom styling
        self.story_content = tk.Text(
            right_panel,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="#2c3e50",
            fg="white",
            padx=10,
            pady=10,
            relief=tk.FLAT,
            height=0  # Will expand with parent
        )
        self.story_content.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.story_content.config(state=tk.DISABLED)
        
        # Moral frame at the bottom
        moral_frame = ttk.Frame(right_panel)
        moral_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.moral_label = ttk.Label(
            moral_frame,
            text="",
            font=("Arial", 11, "italic"),
            wraplength=400
        )
        self.moral_label.pack(fill=tk.X)
        
        # Bind story selection
        self.stories_listbox.bind("<<ListboxSelect>>", self.on_story_select)
        
        # Initialize with first category
        if categories:
            self.category_combo.set(categories[0])
            self.update_stories_list()
            
        # Instructions (now more subtle)
        ttk.Label(
            main_frame,
            text="Add your own stories to the stories.json file in the stories folder",
            font=("Arial", 9),
            foreground="gray"
        ).pack(side=tk.BOTTOM, pady=(10, 0))
    
    def update_stories_list(self, event=None):
        self.stories_listbox.delete(0, tk.END)
        selected_category = self.category_var.get()
        
        # Filter stories by category
        category_stories = [s for s in self.stories if s['category'] == selected_category]
        
        # Add stories to listbox
        for story in category_stories:
            self.stories_listbox.insert(tk.END, story['title'])
    
    def on_story_select(self, event):
        selection = self.stories_listbox.curselection()
        if not selection:
            return
            
        selected_category = self.category_var.get()
        category_stories = [s for s in self.stories if s['category'] == selected_category]
        story = category_stories[selection[0]]
        self.show_story(story)
    
    def show_story(self, story):
        """Display the selected story"""
        self.story_title.config(text=story['title'])
        
        self.story_content.config(state=tk.NORMAL)
        self.story_content.delete(1.0, tk.END)
        self.story_content.insert(tk.END, story['content'])
        self.story_content.config(state=tk.DISABLED)
        
        self.moral_label.config(text=f"Moral: {story['moral']}")
        
        self.current_story = story