# YOSEPH_JA - Voice AI Assistant
A voice-controlled AI assistant for Termux, powered by Python and Pollinations AI.

## Features
- Voice-to-Text interaction.
- Text-to-Speech responses.
- Open applications via voice commands.
- Lightweight and API-key-free.

## Prerequisites
You need Termux with API access:
```bash
pkg update && pkg upgrade
pkg install termux-api python git -y
git clone https://github.com/yosephalganeh-cloud/YOSEPH_JA
cd YOSEPH_JA
pip install -r requirements.txt
python JANO.py
