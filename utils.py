from playsound import playsound
import os

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def play_sound(sound_type):
    sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    try:
        if sound_type == "work":
            playsound(os.path.join(sound_dir, 'Alarm_sound.mp3'))
        elif sound_type == "break":
            playsound(os.path.join(sound_dir, 'Alarm_sound.mp3'))
    except Exception as e:
        print(f"Error playing {sound_type} sound: {e}")