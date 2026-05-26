import os
import sys
import subprocess
import requests
import time
import urllib.parse
import json
import random

# Core ANSI Terminal Color Matrix
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
CONFIG_FILE = "config.json"
selected_mode = "typing"  # Global variable to track input mode

def display_dynamic_banner():
    """Generates and displays stylized, randomized terminal arts inspired by msfconsole."""
    os.system("clear")
    primary_color = random.choice(COLORS)
    accent_color = random.choice([c for c in COLORS if c != primary_color])
    
    banner_block = f"""
{primary_color}    ████████╗ █████╗ ███╗   ██╗ ██████╗       █████╗ ██╗
    ╚══██╔══╝██╔══██╗████╗  ██║██╔═══██╗     ██╔══██╗██║
       ██║   ███████║██╔██╗ ██║██║   ██║     ███████║██║
       ██║   ██╔══██║██║╚██╗██║██║   ██║     ██╔══██║██║
       ██║   ██║  ██║██║ ╚████║╚██████╔╝     ██║  ██║██║
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═╝  ╚═╝╚═╝{RESET}"""

    banner_snake = f"""
{primary_color}       _  _____ _   _  ___      _     ___ 
    _ | |/ _   | \ | |/ _ \    /_\   |_ _|
   | || | |_|  |  \| | |_| |  / _ \   | | 
    \__/ \_____|_| \_|\___/  /_/ \_\ |___|{RESET}"""

    banner_mouse = f"""
{accent_color}       (q\-/-/)  {primary_color}   ___   _   _  _  ___        _   ___ 
{accent_color}        _ 4 4    {primary_color}  |_ _| /_\ | \| |/ _ \      /_\ |_ _|
{accent_color}       (_v  _)   {primary_color}   | | / _ \| .  | |_| |    / _ \ | | 
{accent_color}       (( _ )_   {primary_color}  |___/_/ \_\_|\_|\___/    /_/ \_\___|
{accent_color}       (     )_) {RESET}"""

    selected_art = random.choice([banner_block, banner_snake, banner_mouse])
    print(selected_art)
    print(f"{accent_color}========================================================")
    print(f"                ENGINE DEVELOPED BY YOSEPH ALGANEH     ")
    print(f"========================================================{RESET}\n")

def speak(text):
    """Displays text, and executes TTS only if input mode is voice."""
    print(f"\n{CYAN}[JANO_AI]: {text}{RESET}")
    if selected_mode == "voice":
        subprocess.run(["termux-tts-speak", text])

def listen_voice():
    """Captures environmental speech audio and normalizes it to raw text."""
    try:
        process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate()
        parsed_text = stdout.strip()
        if parsed_text and "ERROR" not in parsed_text:
            print(f"{GREEN}[You (Voice)]: {parsed_text}{RESET}")
            return parsed_text
        return None
    except:
        return None

def get_user_input(input_mode):
    """Consolidates inputs across system terminals dynamically depending on mode."""
    if input_mode == "voice":
        return listen_voice()
    else:
        try:
            typed_input = input(f"{GREEN}[You (Type)]: {RESET}").strip()
            return typed_input if typed_input else None
        except (KeyboardInterrupt, EOFError):
            return "exit"

def query_optimized_ai(question, language):
    """Highly stable AI GET Request using Pollinations correct format."""
    # Custom system instructions (Gender removed)
    system_prompt = f"You are JANO_AI, a highly smart assistant developed by Yoseph Alganeh. The Language is {language}. Crucial Rule: Always reply in the exact language the user used. Keep answers direct, accurate, and fast."
    
    # URL Encoding for safety
    safe_question = urllib.parse.quote(question)
    safe_system = urllib.parse.quote(system_prompt)
    
    # The officially supported Pollinations GET endpoint
    url = f"https://text.pollinations.ai/{safe_question}?system={safe_system}"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"{RED}[Debug Error]: API returned status {response.status_code}{RESET}")
            return "sorry sever errori can not help you right now. please try again later."
    except Exception as e:
        print(f"{RED}[Network Error]: {e}{RESET}")
        return "No Internet. please check your internet connection. "

def get_battery_metrics():
    """Pulls current charging, voltage, and health attributes via Termux JSON blocks."""
    try:
        raw_output = subprocess.check_output(["termux-battery-status"], text=True)
        json_data = json.loads(raw_output)
        return f"Battery capacity is at {json_data['percentage']}% and status is {json_data['status']}."
    except:
        return "Unable to parse device battery attributes."

def get_wifi_metrics():
    """Extracts internal wireless local area network configurations."""
    try:
        raw_output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        json_data = json.loads(raw_output)
        if json_data.get("supplicant_state") == "COMPLETED":
            return f"Connected to Wi-Fi. Network SSID: {json_data.get('ssid', 'Hidden')}."
        return "Your device is not connected to any active Wi-Fi networks."
    except:
        return "Hardware interface failed to read Wi-Fi configurations."

def load_stored_profile():
    """Loads saved profiles directly from persistent disk configuration space."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as file_stream:
                return json.load(file_stream)
        except:
            return None
    return None

def save_profile_to_disk(language):
    """Writes persistent profile configurations to local storage file."""
    profile_data = {"language": language}
    with open(CONFIG_FILE, 'w') as file_stream:
        json.dump(profile_data, file_stream, indent=4)

def run_onboarding_setup(input_mode):
    """Onboarding setup supporting advanced flexible matching dictionary strings."""
    print(f"{YELLOW}[Setup Wizard Initialization]{RESET}")
    
    # Language Selection (Gender Selection is removed)
    speak("Please choose your system language preference. Enter E for English or A for Amharic.")
    language_track = "English"
    while True:
        raw_ans = get_user_input(input_mode)
        if raw_ans:
            val = raw_ans.lower().strip()
            if val in ["e", "english", "inglish", "እንግሊዝኛ"]:
                language_track = "English"
                break
            elif val in ["a", "amharic", "amaric", "አማርኛ"]:
                language_track = "Amharic"
                break
        print(f"{RED}Invalid input. Please enter E or A.{RESET}")

    save_profile_to_disk(language_track)
    speak("User setup configuration saved successfully.")
    return language_track

if __name__ == "__main__":
    display_dynamic_banner()
    
    print(f"{YELLOW}Select Operational Input Interface Mode:{RESET}")
    print(f" [{GREEN}T{RESET}] Typing Keyboard Interface Mode")
    print(f" [{GREEN}V{RESET}] Voice Speech Interface Mode")
    
    while True:
        mode_token = input(f"\n{BLUE}Select Interface Mode [T/V]: {RESET}").lower().strip()
        if mode_token in ["t", "typing"]:
            selected_mode = "typing"
            break
        elif mode_token in ["v", "voice"]:
            selected_mode = "voice"
            break
        print(f"{RED}Error: Code not recognized. Enter 'T' or 'V'.{RESET}")

    stored_profile = load_stored_profile()
    if stored_profile:
        user_language = stored_profile.get("language", "English")
        print(f"{GREEN}[Profile Loaded Memory]: Language={user_language}{RESET}")
    else:
        user_language = run_onboarding_setup(selected_mode)

    speak("JANO AI Online. Ready for your commands.")

    while True:
        cmd_string = get_user_input(selected_mode)
        if not cmd_string:
            continue

        cmd_normalized = cmd_string.lower().strip()

        # ========================================================
        # SYSTEM OPERATIONS INTERFACES (Termux APIs)
        # ========================================================
        if cmd_normalized in ["battery", "ባትሪ"]:
            speak(get_battery_metrics())
            
        elif cmd_normalized in ["wifi", "ዋይፋይ"]:
            speak(get_wifi_metrics())
        
        elif cmd_normalized in ["torch on", "flashlight on", "መብራት አብራ"]:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight turned on.")
            
        elif cmd_normalized in ["torch off", "flashlight off", "መብራት አጥፋ"]:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight turned off.")

        elif cmd_normalized == "clipboard":
            try:
                clipboard_text = subprocess.check_output(["termux-clipboard-get"], text=True).strip()
                speak(f"Clipboard payload context: {clipboard_text if clipboard_text else 'Empty'}")
            except:
                speak("Unable to interface with device clipboard.")
                
        elif cmd_normalized in ["vibrate", "ንዘር"]:
            speak("Vibrating hardware system.")
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif cmd_normalized in ["stop", "exit", "quit", "አቁም"]:
            speak("Shutting down JANO AI. Goodbye!")
            break

        # ========================================================
        # STABLE CORE AI INFERENCE FASTRUN
        # ========================================================
        else:
            ai_inference_response = query_optimized_ai(cmd_string, user_language)
            speak(ai_inference_response)
        
        time.sleep(0.2)
