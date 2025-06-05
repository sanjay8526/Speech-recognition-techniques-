import speech_recognition as sr
import pyttsx3

# Simulated state of appliances
appliance_state = {
    "light": False,
    "fan": False
}

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak and print the assistant's response."""
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture and return voice command from microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙 Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("🗣 You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

def process_command(command):
    """Interpret and execute the command."""
    if "light on" in command:
        appliance_state["light"] = True
        speak("Light turned on.")
    elif "light off" in command:
        appliance_state["light"] = False
        speak("Light turned off.")
    elif "fan on" in command:
        appliance_state["fan"] = True
        speak("Fan turned on.")
    elif "fan off" in command:
        appliance_state["fan"] = False
        speak("Fan turned off.")
    elif "status" in command:
        light = "on" if appliance_state["light"] else "off"
        fan = "on" if appliance_state["fan"] else "off"
        speak(f"The light is {light}, and the fan is {fan}.")
    elif "exit" in command or "stop" in command:
        speak("Shutting down.")
        return False
    else:
        speak("Sorry, I did not understand the command.")
    return True

def main():
    speak("Voice control simulation started.")
    running = True
    while running:
        command = listen()
        if command:
            running = process_command(command)

if __name__ == "__main__":
    main()
