Helio – The AI Therapy Assistant

Thrilled to announce the launch of Helio, an innovative project that my teammate and I developed to make emotional wellness support more accessible and technologically advanced. We believe the future of wellness lies in combining empathy with cutting-edge technology.

✨ Abstract: Supporting Users in Stress

Helio is a powerful, cross-platform desktop application that utilizes the Gemini API and sophisticated natural language processing to serve as a private, multilingual AI companion. Its core mission is to provide *immediate, confidential support during moments of stress and emotional distress*. It does this by offering real-time health analysis, conversational therapeutic support, and a comprehensive suite of stress-relief modules (music, stories, games) accessible with a single click.

💡 What is Helio?

Helio is an AI Therapy Assistant built using Python and Tkinter for a native desktop experience. It's designed to be a confidential, judgment-free space where users can engage in deep, empathetic conversations with a customizable AI (e.g., Therapist, Life Coach, Friend). Crucially, Helio features an innovative emotional monitoring system that tracks the user's well-being over time and provides access to critical safety resources when high concern is detected.

🔑 Key Features

  - Gemini-Powered Conversation
  - Multilingual Support
  - Real-Time Emotional Health Indicator: A proprietary system that analyzes conversation patterns across multiple languages to calculate a real-time Depression Score, visualized via a *Matplotlib-powered analytics graph* to track emotional trends.
  - Integrated Stress Relief Toolkit: Provides a dedicated, accessible menu with modules for Relaxing Music, Motivational Stories, and Stress Relief Games perfect for immediate de-escalation of stress.
  - Voice Integration: Fully hands-free interaction using Google Cloud Speech Recognition for input and ElevenLabs Text-to-Speech for the AI's spoken responses.
  - Data Privacy Focus: Chat history and emotional data are stored locally on the user's machine, ensuring ultimate confidentiality and privacy.

🛠 Technology Stack

| Category | Technology | Purpose |

| Backend/Core | Python 3+ | Main application logic |
| Large Language Model | Google Gemini API (2.0-Flash-Exp) | Conversational AI and intelligence |
| Frontend/UI | Tkinter, ttkbootstrap | Native desktop application GUI and modern theme styling |
| Voice & Speech | ElevenLabs API, speech_recognition (Google Cloud) | Text-to-Speech synthesis and Voice Input |
| Data & Analytics | Matplotlib, json | Historical data storage and visualization of emotional trends |

🤝 Why Choose Helio?

  - Proactive & Immediate Stress Support: It doesn't just chat; it actively listens, measures distress, and offers instant, structured tools to help manage acute stress.
  - Confidential and Private: As a desktop app with local storage, users can speak freely without worrying about cloud data storage or large tech companies accessing their most sensitive thoughts.
  - Culturally Inclusive: Addresses a major gap in digital wellness by offering support in multiple regional languages.

⬇ Installation and Project Structure

You can get started with Helio by cloning the repository and setting up your environment:

Installation Process

bash
# 1. Clone the repository
git clone https://github.com/your-username/helio-ai-therapy.git

# 2. Navigate into the project directory
cd helio-ai-therapy

# 3. Install required Python packages
pip install -r requirements.txt

# IMPORTANT:
# Add your API keys (GEMINI_API_KEY, ELEVENLABS_API_KEY, etc.) 
# in the config.py file before proceeding.

# 4. Run the application
python main.py


#### *📁 Project Structure*

```
helio-ai-therapy/
│
├── assets/                  # Icons, images, music
├── modules/                 # Functional modules (chat, mood analysis, etc.)
├── config.py                # API keys and settings (Crucial for functionality)
├── main.py                  # App launcher
├── README.md                # Project description
└── requirements.txt         # Python dependencies

