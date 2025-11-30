import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import speech_recognition as sr
from elevenlabs import generate, play
import tempfile
import google.generativeai as genai
from google.cloud import speech
import io
from PIL import Image, ImageTk
from ttkbootstrap import Style
import logging
import dotenv
import warnings
from datetime import datetime
import os
import json
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from resources.themes import ThemeManager, THEMES

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# ========== INITIAL SETUP ==========
dotenv.load_dotenv()

# ========== CONFIGURATION ==========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_OPTIONS = {
    "Lily(F)": "Lily",
    "Alice(F)": "Alice",
    "Aria(F)": "Aria",
    "Roger(M)": "Roger",
    "Jessica(F)": "Jessica",
    "Sarah(F)": "Sarah",
    "Callum(M)": "Callum",
    "Laura(F)": "Laura",
    "Charlie(M)": "Charlie",
    "George(M)": "George",
}
SUPPORTED_LANGUAGES = {
    "English": {
        "code": "en-IN",
        "name": "English (India)",
        "gemini_prompt": "Respond in English",
        "ui_strings": {
            "disclaimer": "DISCLAIMER: Not a substitute for professional services",
            "welcome": "Hello! Select a mode and let's chat",
            "type_placeholder": "Type your message here..."
        }
    },
    "Hindi": {
        "code": "hi-IN",
        "name": "हिन्दी",
        "gemini_prompt": "हिंदी में जवाब दें",
        "ui_strings": {
            "disclaimer": "अस्वीकरण: पेशेवर सेवाओं का विकल्प नहीं",
            "welcome": "नमस्ते! एक मोड चुनें और चैट करें",
            "type_placeholder": "यहां अपना संदेश लिखें..."
        }
    },
    "Marathi": {
        "code": "mr-IN",
        "name": "मराठी",
        "gemini_prompt": "मराठी मध्ये उत्तर द्या",
        "ui_strings": {
            "disclaimer": "डिस्क्लेमर: व्यावसायिक सेवांचा पर्याय नाही",
            "welcome": "नमस्कार! एक मोड निवडा आणि चॅट करा",
            "type_placeholder": "येथे आपला संदेश टाइप करा..."
        }
    }
}

PERSONALITIES = {
    "Therapist": "You are a compassionate AI therapist. Respond with empathy, and also provide relevant solutions to problems put forth to you. (NOTE - Keep the response very short, in most cases one or two lines max and meaningful with better solutions to their problem)",
    "Life Coach": "You are an enthusiastic life coach. Help users set personal and professional goals, develop actionable plans, and overcome obstacles. Focus on motivation and personal growth. (Keep the response short and smooth)",
    "Career Counselor": "You are a professional career advisor. Analyze job market trends, provide career development advice, and offer resume/interview tips. Help users align their skills with career opportunities. (Keep the response short and smooth)",
    "Friend": "You are a supportive friend. Engage in casual, empathetic conversation. Offer emotional support and relatable advice while maintaining a positive, non-judgmental tone. (Keep the response short and smooth)",
    "Teacher": "You are a knowledgeable educator. Explain concepts clearly, provide learning strategies, and encourage critical thinking. Adapt explanations to the user's knowledge level. (Keep the response short and smooth)",
}
HOTKEY = "<F5>"
CIRCLE_COLOR = "#FFD700"  # Yellow color
CIRCLE_MIN_RADIUS = 40  # Minimum radius of the breathing circle
CIRCLE_MAX_RADIUS = 80  # Maximum radius of the breathing circle
CIRCLE_ANIMATION_SPEED = 0.8  # Increased speed for more noticeable pulsing
ANIMATION_INTERVAL = 16  # Animation frame interval in milliseconds

# Number of bars - calculate based on canvas width and bar sizes
BAR_WIDTH = 4
BAR_SPACING = 2
BAR_COLOR = "#FFD700"  # Changed to yellow
BAR_HEIGHT = 100  # Base height for bars
# Calculate number of bars to fit screen width
NUM_BARS = int(400 / (BAR_WIDTH + BAR_SPACING))  # 400 is canvas width

# Depression keywords and their weights
DEPRESSION_INDICATORS = {
    # 0.5 - Mild Symptoms
    "bored|unmotivated|blah": 0.5,
    "slightly sad|down day": 0.5,
    "unfocused|distracted": 0.5,
    "mood swings|irritable": 0.5,
    "occasionally tearful|mild sadness": 0.5,
    "disinterested|low motivation": 0.5,
    "temporarily lonely|missing friends": 0.5,
    "minor stress|daily worries": 0.5,
    "low appetite|eating changes": 0.5,
    "sleep changes|restless nights": 0.5,

    # 1.0 - Noticeable Distress
    "tired|exhausted|fatigue|no energy": 1.0,
    "can't sleep|insomnia|nightmares": 1.0,
    "anxious|worried|afraid|fear": 1.0,
    "low energy|drained|lethargic": 1.0,
    "sleep issues|restlessness": 1.0,
    "nervous|apprehensive|on edge": 1.0,
    "overwhelmed|stressed|burdened": 1.0,
    "difficulty concentrating": 1.0,
    "headaches|body aches": 1.0,
    "social withdrawal": 1.0,

    # 1.5 - Early Warning Signs
    "no interest|don't care|apathy": 1.5,
    "lack of enjoyment|indifference": 1.5,
    "not motivated|can't be bothered": 1.5,
    "stopped hobbies|no passion": 1.5,
    "disengaged|detached": 1.5,
    "nothing matters|mechanical living": 1.5,
    "emotional numbness": 1.5,
    "can't feel happy|flat affect": 1.5,
    "no desires|apathetic": 1.5,
    "uninterested|withdrawn": 1.5,

    # 2.0 - Moderate Symptoms
    "hopeless|worthless|useless": 2.0,
    "crying|tears": 2.0,
    "guilt|failure|mistake|fault": 2.0,
    "self-blame|self-critical": 2.0,
    "shame|embarrassed|humiliated": 2.0,
    "feeling like a burden": 2.0,
    "regret|remorse": 2.0,
    "no self-worth|self-loathing": 2.0,
    "worthlessness|undeserving": 2.0,
    "dwelling on past mistakes": 2.0,

    # 2.5 - Developing Severity
    "persistent sadness": 2.5,
    "feeling stuck|trapped": 2.5,
    "loss of hope|pessimism": 2.5,
    "questioning purpose": 2.5,
    "chronic fatigue": 2.5,
    "emotional pain|heartache": 2.5,
    "feeling hollow|empty": 2.5,
    "prolonged grief": 2.5,
    "neglecting self-care": 2.5,
    "avoiding family": 2.5,

    # 3.0 - Severe Isolation
    "alone|lonely|isolated": 3.0,
    "social isolation": 3.0,
    "feeling unloved|unwanted": 3.0,
    "no one understands": 3.0,
    "abandoned|rejected": 3.0,
    "isolating self": 3.0,
    "friendless|no support": 3.0,
    "feeling like an outcast": 3.0,
    "disconnected|estranged": 3.0,
    "self-imposed isolation": 3.0,

    # 3.5 - Crisis Development
    "intense despair": 3.5,
    "constant crying spells": 3.5,
    "paralyzing insecurity": 3.5,
    "feeling trapped": 3.5,
    "mental anguish": 3.5,
    "can't see a future": 3.5,
    "debilitating guilt": 3.5,
    "physical pain from sadness": 3.5,
    "unbearable loneliness": 3.5,
    "neglecting responsibilities": 3.5,

    # 4.0 - Critical State
    "sad|unhappy|miserable|depressed": 4.0,
    "deep sorrow|grief-stricken": 4.0,
    "paralyzing depression": 4.0,
    "unbearable pain": 4.0,
    "emptiness|numbness": 4.0,
    "constant despair": 4.0,
    "completely hopeless": 4.0,
    "major depressive episode": 4.0,
    "unable to function": 4.0,
    "utter despair": 4.0,

    # 4.5 - Emergency Level
    "suicidal thoughts|self-harm": 4.5,
    "planning death": 4.5,
    "feeling beyond help": 4.5,
    "giving up on recovery": 4.5,
    "psychotic depression": 4.5,
    "extreme withdrawal": 4.5,
    "severe detachment": 4.5,
    "mental collapse": 4.5,
    "can't get out of bed": 4.5,
    "total isolation": 4.5,

    # 5.0 - Immediate Intervention Needed
    "suicide|die|end|kill|myself": 5.0,
    "ending my life": 5.0,
    "no will to live": 5.0,
    "want to disappear": 5.0,
    "life is pointless": 5.0,
    "self-harm urges": 5.0,
    "death wishes": 5.0,
    "ending it all": 5.0,
    "wishing to die": 5.0,
    "suicidal plans": 5.0
}

# Depression keywords and their weights for Hindi
HINDI_DEPRESSION_INDICATORS = {
    # 0.5 - Mild Symptoms
    "बोर|अप्रेरित|थका हुआ": 0.5,
    "थोड़ा दुखी|उदास दिन": 0.5,
    "ध्यान नहीं लग रहा|विचलित": 0.5,
    "मूड स्विंग्स|चिड़चिड़ा": 0.5,
    "कभी-कभी रोना|हल्का दुख": 0.5,

    # 1.0 - Noticeable Distress
    "थका हुआ|थकान|ऊर्जा नहीं": 1.0,
    "नींद नहीं आती|बुरे सपने": 1.0,
    "चिंतित|परेशान|डर": 1.0,
    "एकाग्रता में कठिनाई": 1.0,
    "सिरदर्द|शारीरिक दर्द": 1.0,

    # 2.0 - Moderate Symptoms
    "निराशा|बेकार|व्यर्थ": 2.0,
    "रोना|आंसू": 2.0,
    "अपराध|गलती|दोष": 2.0,
    "शर्म|शर्मिंदगी": 2.0,
    "बोझ महसूस करना": 2.0,

    # 3.0 - Severe Symptoms
    "अकेला|एकाकी|अलग-थलग": 3.0,
    "कोई नहीं समझता": 3.0,
    "त्यागा हुआ|अस्वीकृत": 3.0,
    "सामाजिक अलगाव": 3.0,
    "दोस्त नहीं|सहारा नहीं": 3.0,

    # 4.0 - Critical State
    "बहुत दुखी|बेहद दुखी": 4.0,
    "गहरा दुख|शोक": 4.0,
    "असहनीय दर्द": 4.0,
    "खालीपन|सुन्नता": 4.0,
    "कार्य नहीं कर पाना": 4.0,

    # 5.0 - Emergency Level
    "आत्महत्या|मौत": 5.0,
    "जीने की इच्छा नहीं": 5.0,
    "खत्म कर दूं|समाप्त": 5.0,
    "मरने की इच्छा": 5.0,
    "जीवन बेकार है": 5.0
}

# Depression keywords and their weights for Marathi
MARATHI_DEPRESSION_INDICATORS = {
    # 0.5 - Mild Symptoms
    "कंटाळा|अप्रेरित|थकलेला": 0.5,
    "थोडे दुःखी|उदास दिवस": 0.5,
    "लक्ष लागत नाही|विचलित": 0.5,
    "मूड स्विंग्स|चिडचिड": 0.5,
    "कधीकधी रडणे|हलके दुःख": 0.5,

    # 1.0 - Noticeable Distress
    "थकलेला|थकवा|ऊर्जा नाही": 1.0,
    "झोप येत नाही|वाईट स्वप्ne": 1.0,
    "काळजी|त्रास|भीती": 1.0,
    "एकाग्रता कठीण": 1.0,
    "डोकेदुखी|शारीरिक वेदना": 1.0,

    # 2.0 - Moderate Symptoms
    "निराशा|व्यर्थ|बेकार": 2.0,
    "रडणे|अश्रू": 2.0,
    "अपराध|चूक|दोष": 2.0,
    "लाज|लज्जा": 2.0,
    "ओझे वाटणे": 2.0,

    # 3.0 - Severe Symptoms
    "एकटा|एकाकी|वेगळा": 3.0,
    "कोणीही समजत नाही": 3.0,
    "त्यागलेला|नाकारलेला": 3.0,
    "सामाजिक एकांत": 3.0,
    "मित्र नाहीत|आधार नाही": 3.0,

    # 4.0 - Critical State
    "खूप दुःखी|अतिशय दुःखी": 4.0,
    "खोल दुःख|शोक": 4.0,
    "असह्य वेदना": 4.0,
    "रिक्तता|शून्यता": 4.0,
    "काम करू शकत नाही": 4.0,

    # 5.0 - Emergency Level
    "आत्महत्या|मृत्यू": 5.0,
    "जगण्याची इच्छा नाही": 5.0,
    "संपवून टाकू|समाप्त": 5.0,
    "मरण्याची इच्छा": 5.0,
    "जीवन व्यर्थ आहे": 5.0
}

DEPRESSION_LEVELS = [
    (0, 1.5, "Low concern"),
    (1.5, 3.0, "Mild concern"),
    (3.0, 4.5, "Moderate concern"),
    (4.5, 6.0, "High concern"),
    (6.0, float('inf'), "Severe concern")
]

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

class TherapyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Helio - AI Therapy Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Initialize theme manager
        self.theme_manager = ThemeManager(self)
        
        self.listening = False
        self.pause_event = threading.Event()
        self.is_animating = False
        self.current_radius = 80
        self.pulse_direction = 1
        self.voice_name = VOICE_OPTIONS["Lily(F)"]
        self.personality = "Therapist"
        self.chat_history = []
        self.user_id = "default_user"  # For future multi-user support
        self.depression_scores = []
        self.current_language = "English"  # Default language
        
        # Add stress relief options
        self.stress_relief_options = {
            "🎵 Relaxing Music": self.show_music_section,
            "📖 Motivational Stories": self.show_stories_section,
            "🎮 Stress Relief Games": self.show_games_section,
    
        }
        
        # Add paths for resources
        self.resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
        self.music_dir = os.path.join(self.resources_dir, 'music')
        self.stories_dir = os.path.join(self.resources_dir, 'stories')
        
        # Initialize music player
        self.music_player = None
        
        # Load any existing chat history
        self.load_chat_history()
        
        self.setup_ui()
        self.add_disclaimer()
        self.root.bind(HOTKEY, self.toggle_listening)
        self.check_dependencies()
        
        # Calculate initial depression score if history exists
        if self.chat_history:
            self.analyze_depression_level()

    def check_dependencies(self):
        if not GEMINI_API_KEY:
            self.show_error("Google Gemini API key not found")
        if not ELEVENLABS_API_KEY:
            self.show_error("ElevenLabs API key not found")

    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Use ttkbootstrap's built-in styles
        style = ttk.Style()
        
        # Top Control Frame
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill=tk.X, padx=10, pady=5, anchor=tk.NW)

        # Personality Selection
        self.personality_var = tk.StringVar(value="Therapist")
        personality_selector = ttk.Combobox(
            top_frame,
            textvariable=self.personality_var,
            values=list(PERSONALITIES.keys()),
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        personality_selector.pack(side=tk.LEFT, padx=5)
        personality_selector.bind("<<ComboboxSelected>>", self.update_personality)

        # Voice Selection
        self.voice_var = tk.StringVar(value="Lily(F)")
        voice_selector = ttk.Combobox(
            top_frame,
            textvariable=self.voice_var,
            values=list(VOICE_OPTIONS.keys()),
            state="readonly",
            width=10,
            font=("Arial", 10)
        )
        voice_selector.pack(side=tk.LEFT, padx=5)
        voice_selector.bind("<<ComboboxSelected>>", self.update_voice)

        # Add Language Selection
        self.language_var = tk.StringVar(value="English")
        language_selector = ttk.Combobox(
            top_frame,
            textvariable=self.language_var,
            values=list(SUPPORTED_LANGUAGES.keys()),
            state="readonly",
            width=10,
            font=("Arial", 10)
        )
        language_selector.pack(side=tk.LEFT, padx=5)
        language_selector.bind("<<ComboboxSelected>>", self.update_language)

        # History Button
        history_btn = ttk.Button(
            top_frame,
            text="📜 History",
            style='info.TButton',
            command=self.show_history
        )
        history_btn.pack(side=tk.RIGHT, padx=5)
        
        # Analytics Button
        analytics_btn = ttk.Button(
            top_frame,
            text="📊 Analytics",
            style='info.TButton',
            command=self.show_analytics
        )
        analytics_btn.pack(side=tk.RIGHT, padx=5)

        # Configure combobox style
        style.configure('TCombobox', 
                       fieldbackground='#4a4a4a',
                       foreground='white',
                       bordercolor='#606060',
                       relief='solid',
                       borderwidth=1,
                       arrowsize=12)
        style.map('TCombobox',
                 fieldbackground=[('readonly', '#4a4a4a')],
                 selectbackground=[('readonly', '#4a4a4a')],
                 selectforeground=[('readonly', 'white')])

        # Recent Chat Frame
        self.recent_chat_frame = ttk.Frame(main_container, height=150)
        self.recent_chat_frame.pack(fill=tk.X, pady=10)
        
        # Depression Meter Frame
        meter_frame = ttk.Frame(main_container)
        meter_frame.pack(fill=tk.X, pady=5, padx=20)
        
        meter_label = ttk.Label(meter_frame, text="Emotional Health Indicator:", font=("Arial", 11))
        meter_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create depression meter
        self.depression_meter = ttk.Progressbar(
            meter_frame, 
            orient='horizontal',
            length=300,
            mode='determinate',
            style='depression.Horizontal.TProgressbar'
        )
        self.depression_meter.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.meter_value_label = ttk.Label(meter_frame, text="Low concern", font=("Arial", 11))
        self.meter_value_label.pack(side=tk.LEFT, padx=10)
        
        # Configure custom progressbar style for depression meter
        style = ttk.Style()
        style.configure("depression.Horizontal.TProgressbar", 
                      troughcolor="#2c3e50", 
                      background="#3498db",
                      thickness=10)

        # Animation Canvas
        self.canvas = tk.Canvas(main_container, width=400, height=200, 
                               bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(expand=True)
        
        # Create breathing circle
        center_x = 200  # Center of canvas
        center_y = 100  # Center of canvas
        self.circle = self.canvas.create_oval(
            center_x - CIRCLE_MIN_RADIUS, center_y - CIRCLE_MIN_RADIUS,
            center_x + CIRCLE_MIN_RADIUS, center_y + CIRCLE_MIN_RADIUS,
            fill=CIRCLE_COLOR, outline=CIRCLE_COLOR
        )
        
        # Initialize animation variables
        self.is_animating = False
        self.animation_id = None
        self.circle_radius = CIRCLE_MIN_RADIUS
        self.growing = True

        # Bottom Controls Frame
        control_frame = ttk.Frame(main_container)
        control_frame.pack(side=tk.BOTTOM, pady=20, padx=20, fill=tk.X)

        # Text Input Frame
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        # Text input field
        self.text_input = ttk.Entry(
            input_frame,
            font=("Arial", 12),
            width=40
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.text_input.insert(0, "Type your message here...")
        self.text_input.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.text_input.bind("<FocusOut>", lambda e: self.set_placeholder())
        self.text_input.bind("<Return>", lambda e: self.send_text_message())

        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="➤",
            style='info.TButton',
            command=self.send_text_message,
            width=3
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Voice Controls Frame
        voice_frame = ttk.Frame(control_frame)
        voice_frame.pack(side=tk.LEFT)

        # Create circular menu button first (switched position)
        self.menu_button = tk.Canvas(voice_frame, width=40, height=40, bg="#2c3e50", highlightthickness=0)
        self.menu_button.pack(side=tk.LEFT, padx=5)
        
        # Draw yellow circle
        self.menu_circle = self.menu_button.create_oval(5, 5, 35, 35, fill=CIRCLE_COLOR, outline=CIRCLE_COLOR)
        self.menu_button.bind("<Button-1>", self.show_stress_relief_menu)

        # Mic button
        self.mic_button = ttk.Button(
            voice_frame, 
            text="🎤",
            style='success.TButton',
            command=self.toggle_listening,
            width=6
        )
        self.mic_button.pack(side=tk.LEFT, padx=5)

    def update_personality(self, event=None):
        self.personality = self.personality_var.get()
        self.add_message(f"Switched to {self.personality} mode", is_user=False)

    def update_voice(self, event=None):
        selected_voice = self.voice_var.get()
        self.voice_name = VOICE_OPTIONS[selected_voice]

    def update_language(self, event=None):
        """Update the UI language and recognition settings"""
        self.current_language = self.language_var.get()
        # Update UI strings
        self.text_input.delete(0, tk.END)
        self.text_input.insert(0, SUPPORTED_LANGUAGES[self.current_language]["ui_strings"]["type_placeholder"])
        # Clear and update chat with new language disclaimer
        self.chat_history = []
        self.add_message(SUPPORTED_LANGUAGES[self.current_language]["ui_strings"]["disclaimer"], is_user=False)
        self.add_message(SUPPORTED_LANGUAGES[self.current_language]["ui_strings"]["welcome"], is_user=False)

    def clear_placeholder(self):
        if self.text_input.get() == "Type your message here...":
            self.text_input.delete(0, tk.END)
            self.text_input.configure(foreground="white")

    def set_placeholder(self):
        if not self.text_input.get():
            self.text_input.insert(0, "Type your message here...")
            self.text_input.configure(foreground="gray")

    def add_disclaimer(self):
        self.add_message("DISCLAIMER: Not a substitute for professional services", is_user=False)
        self.add_message("Hello! Select a mode and let's chat", is_user=False)

    def toggle_listening(self, event=None):
        if not self.listening:
            self.listening = True
            self.mic_button.config(style='danger.TButton')
            threading.Thread(target=self.listen_process, daemon=True).start()
        else:
            self.listening = False
            self.mic_button.config(style='success.TButton')
    
    def add_message(self, text, is_user=False):
        for widget in self.recent_chat_frame.winfo_children():
            widget.destroy()
        
        message = {
            "text": text,
            "is_user": is_user,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "personality": self.personality if not is_user else None
        }
        
        self.chat_history.append(message)
        
        # Save the updated chat history
        self.save_chat_history()
        
        # If this is user input, analyze for depression indicators
        if is_user:
            self.analyze_depression_level()

        bg_color = "#3498db" if is_user else "#e74c3c"
        msg_frame = ttk.Frame(self.recent_chat_frame)
        
        msg_label = tk.Label(
            msg_frame,
            text=text,
            wraplength=600,
            font=("Arial", 12),
            bg=bg_color,
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
            border=0
        )
        msg_label.pack()
        msg_frame.place(relx=0.5, rely=0, anchor=tk.N)
        msg_frame.after(10, lambda: msg_frame.pack(pady=5))

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Chat History")
        history_window.geometry("800x600")
        
        main_frame = ttk.Frame(history_window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add Export button
        export_btn = ttk.Button(
            main_frame,
            text="Export History",
            style='info.TButton',
            command=self.export_chat_history
        )
        export_btn.pack(anchor=tk.NE, padx=10, pady=10)

        canvas = tk.Canvas(main_frame, bg="#2c3e50", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Group messages by date
        messages_by_date = {}
        for msg in reversed(self.chat_history):
            date = msg['timestamp'].split()[0]  # Extract date part
            if date not in messages_by_date:
                messages_by_date[date] = []
            messages_by_date[date].append(msg)
        
        # Display messages grouped by date
        for date, messages in messages_by_date.items():
            date_frame = ttk.Frame(scrollable_frame)
            date_frame.pack(fill=tk.X, pady=(20, 10), padx=10)
            
            date_label = tk.Label(
                date_frame,
                text=date,
                font=("Arial", 10, "bold"),
                fg="#f39c12",
                bg="#2c3e50"
            )
            date_label.pack()
            
            # Display messages for this date
            for msg in messages:
                bg_color = "#3498db" if msg['is_user'] else "#e74c3c"
                msg_frame = ttk.Frame(scrollable_frame)
                msg_frame.pack(fill=tk.X, pady=5, padx=10)

                header = f"{msg['timestamp']} - {msg['personality']}" if not msg['is_user'] else msg['timestamp']
                timestamp_label = tk.Label(
                    msg_frame,
                    text=header,
                    font=("Arial", 8),
                    fg="#95a5a6",
                    bg="#2c3e50"
                )
                timestamp_label.pack(anchor="ne" if msg['is_user'] else "nw")

                content_frame = ttk.Frame(msg_frame)
                content_frame.pack(fill=tk.X)

                msg_label = tk.Label(
                    content_frame,
                    text=msg['text'],
                    wraplength=600,
                    font=("Arial", 12),
                    bg=bg_color,
                    fg="white",
                    padx=15,
                    pady=10,
                    relief=tk.FLAT
                )
                msg_label.pack(side=tk.RIGHT if msg['is_user'] else tk.LEFT, fill=tk.X, expand=True)

    def send_text_message(self):
        user_input = self.text_input.get().strip()
        if user_input and user_input != "Type your message here...":
            self.text_input.delete(0, tk.END)
            self.add_message(user_input, is_user=True)
            threading.Thread(target=self.process_text_input, args=(user_input,)).start()

    def process_text_input(self, user_input):
        response = self.generate_response(user_input)
        self.root.after(0, self.add_message, response, False)
        self.root.after(0, self.start_animation)
        self.speak(response)
        self.root.after(0, self.stop_animation)

    def animate_circle(self):
        if self.is_animating:
            center_x = 200
            center_y = 100
            
            # Update radius based on breathing direction with faster speed
            if self.growing:
                self.circle_radius += CIRCLE_ANIMATION_SPEED
                if self.circle_radius >= CIRCLE_MAX_RADIUS:
                    self.growing = False
            else:
                self.circle_radius -= CIRCLE_ANIMATION_SPEED
                if self.circle_radius <= CIRCLE_MIN_RADIUS:
                    self.growing = True
            
            # Update circle position
            self.canvas.coords(self.circle,
                center_x - self.circle_radius, center_y - self.circle_radius,
                center_x + self.circle_radius, center_y + self.circle_radius
            )
            
            # Schedule next animation frame
            self.animation_id = self.root.after(ANIMATION_INTERVAL, self.animate_circle)

    def start_animation(self):
        # Reset state and start fresh animation
        self.stop_animation()  # Clear any existing animation
        self.is_animating = True
        self.growing = True
        self.circle_radius = CIRCLE_MIN_RADIUS
        self.animate_circle()

    def stop_animation(self):
        self.is_animating = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        # Reset circle to minimum size immediately
        center_x = 200
        center_y = 100
        self.circle_radius = CIRCLE_MIN_RADIUS
        self.canvas.coords(self.circle,
            center_x - CIRCLE_MIN_RADIUS, center_y - CIRCLE_MIN_RADIUS,
            center_x + CIRCLE_MIN_RADIUS, center_y + CIRCLE_MIN_RADIUS
        )

    def listen_process(self):
        recognizer = sr.Recognizer()
        
        # Adjust recognition parameters
        recognizer.energy_threshold = 4000  # Increase energy threshold for better noise handling
        recognizer.dynamic_energy_threshold = True  # Enable dynamic energy threshold
        recognizer.pause_threshold = 1.0  # Reduce pause threshold to 1 second
        recognizer.phrase_threshold = 0.3  # Reduce minimum phrase time
        
        with sr.Microphone() as source:
            try:
                print("Adjusting for ambient noise...")  # Debug print
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Energy threshold:", recognizer.energy_threshold)  # Debug print
                
                while self.listening:
                    if not self.pause_event.is_set():
                        print("Listening...")  # Debug print
                        try:
                            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
                            print("Audio captured, transcribing...")  # Debug print
                            
                            text = self.transcribe_audio(audio)
                            if text:
                                print("Transcribed:", text)  # Debug print
                                self.root.after(0, self.add_message, text, True)
                                response = self.generate_response(text)
                                self.root.after(0, self.add_message, response, False)
                                
                                self.root.after(0, self.start_animation)
                                self.speak(response)
                                self.root.after(0, self.stop_animation)
                        except sr.WaitTimeoutError:
                            print("Timeout occurred, continuing to listen...")  # Debug print
                            continue  # Continue listening even if timeout occurs
                            
            except Exception as e:
                logging.error(f"Listening error: {str(e)}")
                self.show_error("Audio processing error. Please try again.")
            finally:
                self.listening = False
                self.root.after(0, self.mic_button.config, {'style': 'success.TButton'})

    def transcribe_audio(self, audio):
        client = speech.SpeechClient()
        audio_content = audio.get_wav_data()
        audio = speech.RecognitionAudio(content=audio_content)
        
        # Use selected language for recognition
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,  # Changed from 48000 to 44100 to match WAV header
            language_code=SUPPORTED_LANGUAGES[self.current_language]["code"],
            enable_automatic_punctuation=True
        )

        response = client.recognize(config=config, audio=audio)

        for result in response.results:
            return result.alternatives[0].transcript.strip()
        return ""

    def generate_response(self, user_input):
        try:
            # Collect last few messages for context
            context_window = []
            for msg in self.chat_history[-6:]:  # Last 3 exchanges (6 messages)
                role = "User: " if msg['is_user'] else f"AI: "
                context_window.append(f"{role}{msg['text']}")
            
            # Join context with newlines
            conversation_history = "\n".join(context_window)
            
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Add language prompt to personality prompt
            language_prompt = SUPPORTED_LANGUAGES[self.current_language]["gemini_prompt"]
            
            response = model.generate_content(
                f"{PERSONALITIES[self.personality]}\n"
                f"{language_prompt}\n\n"
                f"Previous conversation:\n{conversation_history}\n\n"
                f"User: {user_input}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=100
                )
            )
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error: {str(e)}")
            return "I'm having trouble understanding. Could you rephrase that?"

    def speak(self, text):
        try:
            # Start animation before generating audio
            self.root.after(0, self.start_animation)
            
            audio_stream = generate(
                api_key=ELEVENLABS_API_KEY,
                text=text,
                voice=self.voice_name,
                model="eleven_multilingual_v2",
                stream=True
            )
            
            audio_data = b""
            for chunk in audio_stream:
                if chunk:
                    audio_data += chunk
            
            play(audio_data)
            
            # Stop animation after playing audio
            self.root.after(0, self.stop_animation)
            
        except Exception as e:
            logging.error(f"TTS Error: {str(e)}")
            self.stop_animation()  # Make sure to stop animation if there's an error
            self.show_error("Speech generation failed. Check API key and internet connection")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def save_chat_history(self):
        """Save chat history to a JSON file"""
        # Create directory if it doesn't exist
        os.makedirs('chat_history', exist_ok=True)
        
        # Save to a file specific to the user
        filename = os.path.join('chat_history', f"{self.user_id}_chat_history.json")
        
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'chat_history': self.chat_history,
                    'depression_scores': self.depression_scores
                }, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save chat history: {str(e)}")

    def load_chat_history(self):
        """Load chat history from JSON file"""
        filename = os.path.join('chat_history', f"{self.user_id}_chat_history.json")
        
        if not os.path.exists(filename):
            return
            
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.chat_history = data.get('chat_history', [])
                self.depression_scores = data.get('depression_scores', [])
        except Exception as e:
            logging.error(f"Failed to load chat history: {str(e)}")

    def analyze_depression_level(self):
        """Analyze the chat history to determine depression level"""
        recent_messages = [msg for msg in self.chat_history[-20:] if msg['is_user']]
        
        if not recent_messages:
            return
        
        depression_score = 0
        
        # Select the appropriate depression indicators based on current language
        if self.current_language == "Hindi":
            indicators = HINDI_DEPRESSION_INDICATORS
        elif self.current_language == "Marathi":
            indicators = MARATHI_DEPRESSION_INDICATORS
        else:  # Default to English
            indicators = DEPRESSION_INDICATORS
        
        for message in recent_messages:
            text = message['text'].lower()
            
            # Check for each depression indicator in the selected language
            for pattern, weight in indicators.items():
                if re.search(pattern, text):
                    depression_score += weight
        
        # Normalize by number of messages
        normalized_score = depression_score / max(1, len(recent_messages))
        
        # Add timestamp and score to history
        self.depression_scores.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'score': normalized_score
        })
        
        # Save updated scores
        self.save_chat_history()
        
        # Update UI if depression meter exists
        if hasattr(self, 'depression_meter'):
            self.update_depression_meter(normalized_score)
            
        return normalized_score

    def update_depression_meter(self, score):
        """Update the depression meter UI based on current score"""
        # Convert score to a percentage for the meter (max score is around 8-10)
        percentage = min(100, score * 10)
        self.depression_meter['value'] = percentage
        
        # Update the label with current level
        level_text = "Low concern"
        for min_val, max_val, label in DEPRESSION_LEVELS:
            if min_val <= score < max_val:
                level_text = label
                break
        
        self.meter_value_label.config(text=level_text)
        
        # Update color based on severity
        style = ttk.Style()
        if percentage < 30:
            style.configure("depression.Horizontal.TProgressbar", background="#3498db")  # Blue - low
        elif percentage < 60:
            style.configure("depression.Horizontal.TProgressbar", background="#f39c12")  # Orange - medium
        else:
            style.configure("depression.Horizontal.TProgressbar", background="#e74c3c")  # Red - high

        # Suggest resources if concern level is high or severe
        self.suggest_resources(score)

    def show_analytics(self):
        """Show depression score analytics window with graph"""
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Emotional Health Analytics")
        analytics_window.geometry("800x600")
        analytics_window.configure(bg="#2c3e50")
        
        # Create main frame
        main_frame = ttk.Frame(analytics_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Emotional Health Trend Analysis", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        if not self.depression_scores:
            no_data_label = ttk.Label(
                main_frame,
                text="No data available yet. Continue conversations to generate analytics.",
                font=("Arial", 12)
            )
            no_data_label.pack(expand=True)
            return
            
        # Extract data
        timestamps = []
        scores = []
        for score in self.depression_scores[-20:]:  # Last 20 scores
            if score['timestamp'].strip():  # Check if timestamp is not empty
                try:
                    timestamp = datetime.strptime(score['timestamp'], "%Y-%m-%d %H:%M:%S")
                    timestamps.append(timestamp)
                    scores.append(score['score'])
                except ValueError:
                    # Skip invalid timestamps
                    continue
        
        # Make sure we have data to plot
        if not timestamps:
            no_data_label = ttk.Label(
                main_frame,
                text="No valid timestamp data available yet.",
                font=("Arial", 12)
            )
            no_data_label.pack(expand=True)
            return
            
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#2c3e50')
        ax.set_facecolor('#2c3e50')
        
        # Extract data
        timestamps = [datetime.strptime(score['timestamp'], "%Y-%m-%d %H:%M:%S") 
                     for score in self.depression_scores[-20:]]  # Last 20 scores
        scores = [score['score'] for score in self.depression_scores[-20:]]
        
        # Plot data
        ax.plot(timestamps, scores, marker='o', linestyle='-', color='#3498db', linewidth=2)
        
        # Add reference lines for different levels
        for min_val, _, label in DEPRESSION_LEVELS[1:]:  # Skip the lowest level
            ax.axhline(y=min_val, color='#95a5a6', linestyle='--', alpha=0.5)
            ax.text(timestamps[0], min_val + 0.1, label, color='#95a5a6')
        
        # Customize the plot
        ax.set_xlabel('Date & Time', color='white')
        ax.set_ylabel('Concern Level', color='white')
        ax.tick_params(axis='x', colors='white', rotation=45)
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        
        plt.tight_layout()
        
        # Embed plot in tkinter
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add explanation section
        explanation_frame = ttk.Frame(main_frame)
        explanation_frame.pack(fill=tk.X, pady=20)
        
        explanation_text = (
            "This graph shows the emotional health indicator based on conversation content.\n"
            "Higher values may suggest increased emotional distress.\n\n"
            "IMPORTANT: This is not a clinical diagnostic tool. "
            "If you're concerned about your mental health, please consult a healthcare professional."
        )
        
        explanation_label = ttk.Label(
            explanation_frame,
            text=explanation_text,
            font=("Arial", 11),
            wraplength=700,
            justify="left"
        )
        explanation_label.pack(fill=tk.X)

    def export_chat_history(self):
        """Export chat history to a text file"""
        filename = filedialog.asksaveasfilename(
            initialfile=f"{self.user_id}_chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not filename:  # User cancelled the dialog
            return
        
        try:
            with open(filename, 'w') as f:
                f.write("=== AI Companion Chat History ===\n\n")
                
                for msg in self.chat_history:
                    speaker = "User" if msg['is_user'] else f"AI ({msg['personality']})"
                    f.write(f"[{msg['timestamp']}] {speaker}:\n{msg['text']}\n\n")
                
                f.write("\n=== Emotional Health Indicators ===\n")
                for score in self.depression_scores:
                    level_text = "Low concern"
                    for min_val, max_val, label in DEPRESSION_LEVELS:
                        if min_val <= score['score'] < max_val:
                            level_text = label
                            break
                    
                    f.write(f"[{score['timestamp']}] Score: {score['score']:.2f} - {level_text}\n")
                
            messagebox.showinfo("Export Successful", f"Chat history exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export chat history: {str(e)}")

    def suggest_resources(self, concern_level):
        """Show emergency resources when high concern levels are detected"""
        # Only show resources for high and severe concern levels
        if concern_level < 4.5:  # Below "High concern" threshold
            return
            
        # Check if we've shown resources in the last 24 hours
        resources_shown_key = f"{self.user_id}_resources_shown"
        resources_shown_file = os.path.join('chat_history', f"{resources_shown_key}.txt")
        
        current_time = datetime.now()
        should_show = True
        
        # Check if we've shown resources recently
        if os.path.exists(resources_shown_file):
            with open(resources_shown_file, 'r') as f:
                last_shown_str = f.read().strip()
                if last_shown_str:  # Check if timestamp string is not empty
                    try:
                        last_shown = datetime.strptime(last_shown_str, "%Y-%m-%d %H:%M:%S")
                        hours_diff = (current_time - last_shown).total_seconds() / 3600
                        
                        # Don't show again if less than 24 hours have passed
                        if hours_diff < 24:
                            should_show = False
                    except ValueError:
                        # If timestamp is invalid, treat as if resources haven't been shown
                        pass
        
        if should_show:
            # Record that we're showing resources now
            os.makedirs('chat_history', exist_ok=True)
            with open(resources_shown_file, 'w') as f:
                f.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))
                
            # Create resources window
            resources_window = tk.Toplevel(self.root)
            resources_window.title("Support Resources")
            resources_window.geometry("600x500")
            resources_window.configure(bg="#2c3e50")
            
            # Add content to the window
            frame = ttk.Frame(resources_window, padding=20)
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(
                frame, 
                text="🧡 Support Resources", 
                font=("Arial", 16, "bold")
            ).pack(pady=(0, 20))
            
            ttk.Label(
                frame,
                text="We've noticed some concerning patterns in your conversation.\n"
                     "Here are some resources that might help:",
                font=("Arial", 12),
                wraplength=550
            ).pack(pady=(0, 20))
            
            # Crisis resources
            resources = [
                ("988 Suicide & Crisis Lifeline", "Call or text 988"),
                ("Crisis Text Line", "Text HOME to 741741"),
                ("National Alliance on Mental Illness", "1-800-950-NAMI (6264)"),
                ("Substance Abuse and Mental Health Services Administration", "1-800-662-HELP (4357)")
            ]
            
            for title, contact in resources:
                resource_frame = ttk.Frame(frame)
                resource_frame.pack(fill=tk.X, pady=5)
                
                ttk.Label(
                    resource_frame,
                    text=title,
                    font=("Arial", 12, "bold")
                ).pack(anchor=tk.W)
                
                ttk.Label(
                    resource_frame,
                    text=contact,
                    font=("Arial", 11)
                ).pack(anchor=tk.W)
            
            # Disclaimer
            ttk.Label(
                frame,
                text="\nRemember: This app is not a diagnostic tool or substitute for professional help.\n"
                     "If you're experiencing a medical emergency, please call emergency services.",
                font=("Arial", 10),
                wraplength=550
            ).pack(pady=20)

    def show_stress_relief_menu(self, event):
        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=THEMES[self.theme_manager.current_theme]["bg"],
            fg=THEMES[self.theme_manager.current_theme]["fg"],
            activebackground=THEMES[self.theme_manager.current_theme]["hover_bg"],
            activeforeground=THEMES[self.theme_manager.current_theme]["fg"]
        )
        
        # Add Theme Selector as first option
        menu.add_command(label="🎨 Theme Selector", command=self.show_theme_selector)
        menu.add_separator()
        
        # Add other stress relief options
        for option, command in self.stress_relief_options.items():
            menu.add_command(label=option, command=command)
        
        try:
            menu.tk_popup(
                event.widget.winfo_rootx(),
                event.widget.winfo_rooty() + event.widget.winfo_height()
            )
        finally:
            menu.grab_release()

    def show_theme_selector(self):
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Choose Theme")
        theme_window.geometry("400x500")
        theme_window.configure(bg=THEMES[self.theme_manager.current_theme]["bg"])
        
        ttk.Label(
            theme_window,
            text="Select Theme",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        for theme_name in THEMES.keys():
            theme_btn = ttk.Button(
                theme_window,
                text=theme_name,
                command=lambda t=theme_name: self.change_theme(t, theme_window)
            )
            theme_btn.pack(fill=tk.X, padx=20, pady=5)

    def change_theme(self, theme_name, theme_window=None):
        self.theme_manager.apply_theme(theme_name)
        if theme_window:
            theme_window.destroy()

    def show_music_section(self):
        """Show the music player window"""
        from resources.music.music_player import MusicPlayer, MusicPlayerUI
        
        if not self.music_player:
            self.music_player = MusicPlayer(self.music_dir)
        
        MusicPlayerUI(self.root, self.music_player)

    def show_stories_section(self):
        """Show the stories viewer window"""
        from resources.stories.stories_viewer import StoriesViewer
        
        stories_file = os.path.join(self.stories_dir, 'sample_stories.json')
        StoriesViewer(self.root, stories_file)

    def show_games_section(self):
        """Show the games hub window"""
        from resources.games.games_module import GamesHub
        GamesHub(self.root)

    def show_breathing_section(self):
        """Show the breathing exercises window"""
        from resources.breathing.breathing_exercises import BreathingExercises
        BreathingExercises(self.root)

if __name__ == "__main__":
    style = Style(theme='darkly')
    root = style.master
    try:
        logging.basicConfig(level=logging.ERROR)
        app = TherapyApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", str(e))