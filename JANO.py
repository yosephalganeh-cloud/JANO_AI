import subprocess
import requests
import time
import urllib.parse
import json
import os

CONFIG_FILE = "jano_config.json"

def speak(text):
    print(f"\n[JANO_AI]: {text}")
    subprocess.run(["termux-tts-speak", text])

def listen():
    print("\n[JANO_AI is listening...] (Speak now)")
    try:
        process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        user_text = stdout.strip()
        if user_text and "ERROR" not in user_text:
            print(f"[You]: {user_text}")
            return user_text
        return None
    except:
        return None

def get_input(mode):
    """የመጣበትን የግብዓት አይነት (ድምፅ ወይም ጽሑፍ) መቆጣጠሪያ"""
    if mode == "voice":
        return listen()
    else:
        return input("\n[You - Type here]: ").strip()

def ask_ai(question, gender, language):
    prompt = f"You are JANO_AI, a highly intelligent voice assistant. The user is {gender}. The user's preferred language is {language}. CRITICAL RULE: If the user asks in Amharic, you MUST reply in Amharic. If the user asks in English, you MUST reply in English. Keep your responses short, natural, and highly accurate. User says: {question}"
    
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{safe_prompt}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "Sorry, my network brain is currently offline."
    except:
        return "Network connection failed."

def get_battery_info():
    try:
        output = subprocess.check_output(["termux-battery-status"], text=True)
        data = json.loads(output)
        return f"Your battery is at {data['percentage']} percent, and it is {data['status']}."
    except:
        return "I couldn't read the battery status."

def get_wifi_info():
    try:
        output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        data = json.loads(output)
        if data.get("supplicant_state") == "COMPLETED":
            return f"You are connected to Wi-Fi. The network name is {data.get('ssid', 'unknown')}."
        return "You are not connected to Wi-Fi."
    except:
        return "I couldn't get the Wi-Fi information."

def setup_user(input_mode):
    # መረጃው ቀድሞ የተቀመጠ ከሆነ ማንበብ
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config["gender"], config["language"]
        except:
            pass

    # መረጃው ከሌለ በአዲሱ መንገድ ጠይቆ ማስቀመጥ
    speak("Please specify your gender. Say or type Male or Female.")
    user_gender = "Unknown"
    while True:
        ans = get_input(input_mode)
        if ans:
            ans_lower = ans.lower()
            if "female" in ans_lower or "ሴት" in ans_lower:
                user_gender = "Female"
                break
            elif "male" in ans_lower or "ወንድ" in ans_lower:
                user_gender = "Male"
                break
            else:
                speak("Please specify Male or Female.")
    
    speak("Which language do you prefer? Say or type English or Amharic.")
    user_lang = "English"
    while True:
        ans = get_input(input_mode)
        if ans:
            ans_lower = ans.lower()
            if "amharic" in ans_lower or "አማርኛ" in ans_lower:
                user_lang = "Amharic"
                break
            elif "english" in ans_lower or "እንግሊዝኛ" in ans_lower:
                user_lang = "English"
                break
            else:
                speak("Please specify English or Amharic.")
                
    # መረጃውን ፋይል ውስጥ መቅረጽ
    config = {"gender": user_gender, "language": user_lang}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
        
    speak("Setup complete. Memory saved.")
    return user_gender, user_lang

if __name__ == "__main__":
    # ሁልጊዜ ሲነሳ መጀመሪያ የግብዓት አይነት ይጠይቃል
    print("\nSelect Mode / ሁነታ ይምረጡ:")
    print("1. For Voice mode, type 'voice' or 'v'")
    print("2. For Typing mode, type 'typing' or 't'")
    
    input_mode = "voice"
    while True:
        mode_choice = input("Choose mode: ").strip().lower()
        if "voice" in mode_choice or mode_choice == "v":
            input_mode = "voice"
            speak("Voice mode activated.")
            break
        elif "typing" in mode_choice or mode_choice == "t":
            input_mode = "typing"
            speak("Typing mode activated.")
            break
        else:
            print("Invalid option. Enter 'typing' or 'voice'.")

    # የተጠቃሚ መረጃ ማረጋገጫ (ከአንዴ በላይ አይጠይቅም)
    gender, language = setup_user(input_mode)
    speak(f"Welcome back. JANO_AI is ready in {input_mode} mode.")
    
    # ዋናው የስራ ክፍል
    while True:
        cmd_raw = get_input(input_mode)
        
        if not cmd_raw: 
            continue
            
        cmd = cmd_raw.lower()

        # ==========================================
        # TERMUX API SYSTEM CONTROLS
        # ==========================================
        if "battery" in cmd or "ባትሪ" in cmd:
            speak(get_battery_info())
            
        elif "wifi" in cmd or "ዋይፋይ" in cmd:
            speak(get_wifi_info())
        
        elif "torch on" in cmd or "flashlight on" in cmd or "መብራት አብራ" in cmd:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight turned on.")
            
        elif "torch off" in cmd or "flashlight off" in cmd or "መብራት አጥፋ" in cmd:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight turned off.")

        elif "clipboard" in cmd:
            try:
                text = subprocess.check_output(["termux-clipboard-get"], text=True)
                speak(f"Clipboard content is: {text}")
            except:
                speak("Clipboard is empty.")
                
        elif "vibrate" in cmd or "ንዘር" in cmd:
            speak("Vibrating now.")
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif "stop" in cmd or "exit" in cmd or "አቁም" in cmd:
            speak("Shutting down JANO_AI. Goodbye!")
            break

        # ==========================================
        # ASK AI
        # ==========================================
        else:
            ai_reply = ask_ai(cmd_raw, gender, language)
            speak(ai_reply)
        
        time.sleep(1)
