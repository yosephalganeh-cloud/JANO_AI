import subprocess
import requests
import time
import urllib.parse
import os

def speak(text):
    print(f"\n[Jarvis]: {text}")
    subprocess.run(["termux-tts-speak", text])

def listen():
    print("\n[Listening...]")
    try:
        process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        user_text = stdout.strip()
        if user_text and "ERROR" not in user_text:
            print(f"[You]: {user_text}")
            return user_text
        return None
    except Exception:
        return None

def ask_ai(question):
    prompt = f"Jarvis: {question}"
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{safe_prompt}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "I'm offline."
    except:
        return "Connection failed."

if __name__ == "__main__":
    speak("System online. I am YOSEPH_JA, your voice assistant.")
    
    while True:
        user_speech = listen()
        if not user_speech: continue
        
        cmd = user_speech.lower()
        
        # System control
        if "open" in cmd:
            app_name = cmd.replace("open ", "")
            speak(f"Opening {app_name}")
            subprocess.run(["termux-open", f"app://{app_name}"])
            
        elif "close" in cmd or "exit" in cmd:
            speak("Returning to home screen.")
            subprocess.run(["am", "force-stop", "com.android.chrome"]) # ምሳሌ
            subprocess.run(["input", "keyevent", "3"]) # Home button
            
        elif "stop" in cmd:
            speak("Shutting down.")
            break
            
        else:
            speak(ask_ai(user_speech))
        
        # ቀጣዩን እንዳይቀጥል መጠበቂያ
        time.sleep(2)
