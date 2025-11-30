import os
import pygame
import threading
from tkinter import ttk
import tkinter as tk

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.current_track = None
        self.is_playing = False
        self.tracks = self._load_tracks()
        
    def _load_tracks(self):
        """Load all music tracks from the music directory"""
        tracks = {}
        categories = {
            'nature': 'Nature Sounds',
            'classical': 'Classical Music',
            'meditation': 'Meditation Music',
            'white_noise': 'White Noise',
            'rain': 'Rain Sounds'
        }
        
        for category in categories:
            category_path = os.path.join(self.music_dir, category)
            if os.path.exists(category_path):
                tracks[categories[category]] = []
                for file in os.listdir(category_path):
                    if file.endswith(('.mp3', '.wav')):
                        tracks[categories[category]].append({
                            'name': os.path.splitext(file)[0],
                            'path': os.path.join(category_path, file)
                        })
        
        return tracks
    
    def play(self, track_path):
        if self.current_track != track_path:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play(-1)
            self.current_track = track_path
            self.is_playing = True
    
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
    
    def resume(self):
        if not self.is_playing and self.current_track:
            pygame.mixer.music.unpause()
            self.is_playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None
        self.is_playing = False

class MusicPlayerUI:
    def __init__(self, parent, music_player):
        self.window = tk.Toplevel(parent)
        self.window.title("Relaxing Music")
        self.window.geometry("500x400")
        self.window.configure(bg="#2c3e50")
        
        self.music_player = music_player
        self.current_track_widget = None
        self.setup_ui()
    
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
            text="🎵 Relaxing Music",
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)
        
        # Category selection
        categories = list(self.music_player.tracks.keys())
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
        self.category_combo.bind("<<ComboboxSelected>>", self.update_track_list)
        
        # Tracks list frame
        tracks_frame = ttk.Frame(main_frame)
        tracks_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create track listing with scrollbar
        self.tracks_canvas = tk.Canvas(
            tracks_frame,
            bg="#2c3e50",
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(tracks_frame, orient="vertical", command=self.tracks_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.tracks_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.tracks_canvas.configure(scrollregion=self.tracks_canvas.bbox("all"))
        )
        
        self.tracks_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.tracks_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the track listing components
        self.tracks_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Player controls frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Track info frame
        self.info_frame = ttk.Frame(control_frame)
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.track_name_label = ttk.Label(
            self.info_frame,
            text="No track selected",
            font=("Arial", 12),
            wraplength=400
        )
        self.track_name_label.pack()
        
        # Control buttons frame
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack()
        
        # Play/Pause button
        self.play_pause_btn = ttk.Button(
            buttons_frame,
            text="▶️",
            width=3,
            command=self.toggle_play_pause
        )
        self.play_pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_btn = ttk.Button(
            buttons_frame,
            text="⏹️",
            width=3,
            command=self.stop_music
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Initialize with first category
        if categories:
            self.category_combo.set(categories[0])
            self.update_track_list()
            
        # Instructions (subtle)
        ttk.Label(
            main_frame,
            text="Add your own music files to the respective category folders",
            font=("Arial", 9),
            foreground="gray"
        ).pack(side=tk.BOTTOM, pady=(10, 0))
    
    def update_track_list(self, event=None):
        # Clear existing tracks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        selected_category = self.category_var.get()
        tracks = self.music_player.tracks.get(selected_category, [])
        
        if not tracks:
            ttk.Label(
                self.scrollable_frame,
                text=f"No tracks available in {selected_category}.\nAdd .mp3 or .wav files to the appropriate folder.",
                font=("Arial", 11),
                wraplength=400
            ).pack(expand=True)
            return
        
        for track in tracks:
            track_frame = ttk.Frame(self.scrollable_frame)
            track_frame.pack(fill=tk.X, pady=5)
            
            # Track button (whole row is clickable)
            track_btn = tk.Button(
                track_frame,
                text=track['name'],
                font=("Arial", 11),
                bg="#34495e" if track['path'] != self.music_player.current_track else "#FFD700",  # Changed selected color to yellow
                fg="white" if track['path'] != self.music_player.current_track else "black",  # Black text on yellow background
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=5,
                command=lambda t=track: self.play_track(t)
            )
            track_btn.pack(fill=tk.X)
            
            # Store reference to current track's widget
            if track['path'] == self.music_player.current_track:
                self.current_track_widget = track_btn
    
    def play_track(self, track):
        # Update UI first
        if self.current_track_widget:
            self.current_track_widget.configure(bg="#34495e", fg="white")
        
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                btn = widget.winfo_children()[0]
                if btn['text'] == track['name']:
                    btn.configure(bg="#FFD700", fg="black")  # Yellow background with black text for selected track
                    self.current_track_widget = btn
                    break
        
        # Update track name label
        self.track_name_label.config(text=track['name'])
        
        # Update play/pause button
        self.play_pause_btn.config(text="⏸️")
        
        # Play the track
        self.music_player.play(track['path'])
    
    def toggle_play_pause(self):
        if not self.music_player.current_track:
            return
            
        if self.music_player.is_playing:
            self.music_player.pause()
            self.play_pause_btn.config(text="▶️")
        else:
            self.music_player.resume()
            self.play_pause_btn.config(text="⏸️")
    
    def stop_music(self):
        self.music_player.stop()
        self.play_pause_btn.config(text="▶️")
        self.track_name_label.config(text="No track selected")
        
        # Reset track highlighting
        if self.current_track_widget:
            self.current_track_widget.configure(bg="#34495e", fg="white")
            self.current_track_widget = None