import subprocess
import requests
import time
import urllib.parse
import json

def speak(text):
    print(f"\n[JANO_AI]: {text}")
    subprocess.run(["termux-tts-speak", text])

def listen():
    print("\n[JANO_AI is listening...]")
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

def ask_ai(question):
    url = f"https://text.pollinations.ai/{urllib.parse.quote(question)}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "I am having trouble connecting to the network."
    except:
        return "Network error occurred."

# --- Smart Termux API Functions ---
def get_battery():
    try:
        out = subprocess.check_output(["termux-battery-status"], text=True)
        data = json.loads(out)
        perc = data.get('percentage', 'unknown')
        stat = data.get('status', 'unknown').lower()
        return f"Sir, your battery is at {perc} percent and is currently {stat}."
    except:
        return "I could not read the battery status."

def get_wifi():
    try:
        out = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        data = json.loads(out)
        if data.get("supplicant_state") == "COMPLETED":
            ssid = data.get('ssid', 'unknown').replace('"', '')
            return f"You are connected to a WiFi network named {ssid}."
        return "WiFi is not connected."
    except:
        return "I could not check the WiFi status."

if __name__ == "__main__":
    speak("System online. I am JANO_AI, ready for all commands.")
    
    while True:
        speech = listen()
        if not speech: continue
        cmd = speech.lower()

        # 1. Hardware & Sensors Commands
        if "battery" in cmd:
            speak(get_battery())
            
        elif "wifi" in cmd or "network" in cmd:
            speak(get_wifi())
            
        elif "torch on" in cmd or "flashlight on" in cmd:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight is activated.")
            
        elif "torch off" in cmd or "flashlight off" in cmd:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight is deactivated.")
            
        elif "take photo" in cmd or "take a picture" in cmd:
            speak("Taking a photo now.")
            # ፎቶ አንስቶ photo.jpg በሚል ስም ያስቀምጠዋል
            subprocess.run(["termux-camera-photo", "photo.jpg"])
            speak("Photo saved as photo.jpg in your current directory.")
            
        elif "vibrate" in cmd:
            speak("Vibrating the device.")
            # ስልኩን ለ 1000 ሚሊ ሰከንድ (1 ሰከንድ) ያንቀጠቅጠዋል
            subprocess.run(["termux-vibrate", "-f", "-d", "1000"])

        elif "read clipboard" in cmd or "what did i copy" in cmd:
            try:
                text = subprocess.check_output(["termux-clipboard-get"], text=True)
                speak(f"Your clipboard says: {text}")
            except:
                speak("Your clipboard is empty.")

        # 2. System Exit Command
        elif "stop" in cmd or "sleep" in cmd:
            speak("Shutting down JANO_AI. Have a good day!")
            break

        # 3. AI Assistant Logic (ከላይ ያሉት ትዕዛዞች ካልሆኑ ወደ AI ይላካል)
        else:
            ai_response = ask_ai(speech)
            speak(ai_response)
        
        time.sleep(1.5)
