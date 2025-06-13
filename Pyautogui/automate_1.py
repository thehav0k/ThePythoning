import time
from pynput import keyboard
import pyautogui
last_space_time = 0
pressed_keys = set()

def on_press(key):
    try:
        pressed_keys.add(key)
        if keyboard.Key.cmd in pressed_keys and keyboard.Key.alt in pressed_keys:
            time.sleep(1.25)  # eituk delay na dile age agei likha shuru hoye jabe
            pyautogui.write('Absolute Cinema', interval=0.07) # interval controls typing speed
            return False  # Stop listener after typing
    except Exception:
        pass

def on_release(key):
    try:
        pressed_keys.discard(key)
    except Exception:
        pass

if __name__ == "__main__":
    print("Press Cmd+Opt to type the message at the cursor.")
    with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
