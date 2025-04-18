import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import pyperclip

is_dark_mode = True
history = []

# ------------------ Theme Definitions ------------------
dark_theme = {
    "bg": "#121212",
    "fg": "#ffffff",
    "btn_bg": "#1f1f1f",
    "btn_active": "#2c2c2c",
    "entry_bg": "#1e1e1e",
    "entry_fg": "#ffffff",
    "accent": "#bb86fc",
    "history_bg": "#1a1a1a",
}

light_theme = {
    "bg": "#f5f5f5",
    "fg": "#000000",
    "btn_bg": "#ffffff",
    "btn_active": "#e0e0e0",
    "entry_bg": "#ffffff",
    "entry_fg": "#000000",
    "accent": "#6200ee",
    "history_bg": "#eaeaea",
}

# ------------------ Core Functions ------------------
def click(event):
    text = event.widget.cget("text")
    if text == "=":
        calculate()
    elif text == "C":
        entry.delete(0, tk.END)
    elif text == "⌫":
        entry.delete(len(entry.get()) - 1)
    else:
        entry.insert(tk.END, text)

def calculate():
    try:
        expression = entry.get()
        result = str(eval(expression))
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        timestamp = datetime.now().strftime("%H:%M:%S")
        history.append(f"[{timestamp}] {expression} = {result}")
        update_history()
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()
    toggle_btn.config(text="🌞 Light Mode" if is_dark_mode else "🌙 Dark Mode")

def toggle_history():
    if history_frame.winfo_viewable():
        history_frame.pack_forget()
    else:
        history_frame.pack(fill=tk.BOTH, expand=False, padx=15, pady=(0, 10))

def update_history():
    history_text.config(state=tk.NORMAL)
    history_text.delete("1.0", tk.END)
    for item in history[-12:][::-1]:
        history_text.insert(tk.END, item + "\n")
    history_text.config(state=tk.DISABLED)

def clear_history():
    history.clear()
    update_history()

def copy_result(event):
    pyperclip.copy(entry.get())

def key_handler(event):
    if event.keysym == "Return":
        calculate()
    elif event.keysym == "Escape":
        entry.delete(0, tk.END)
    elif event.keysym == "BackSpace":
        entry.delete(len(entry.get()) - 1)

# ------------------ Theme Application ------------------
def apply_theme():
    theme = dark_theme if is_dark_mode else light_theme
    root.config(bg=theme["bg"])
    entry.config(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    toggle_btn.config(bg=theme["accent"], fg="#fff")
    history_btn.config(bg=theme["accent"], fg="#fff")
    clear_history_btn.config(bg=theme["accent"], fg="#fff")
    history_frame.config(bg=theme["history_bg"])
    history_text.config(bg=theme["history_bg"], fg=theme["fg"])
    button_frame.config(bg=theme["bg"])
    for btn in buttons_list:
        btn.config(bg=theme["btn_bg"], fg=theme["fg"], activebackground=theme["btn_active"])

# ------------------ GUI Layout ------------------
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("400x750")
root.resizable(True, True)
root.bind("<Key>", key_handler)

entry = tk.Entry(root, font="Helvetica 26", justify='right', bd=0, relief=tk.FLAT)
entry.pack(fill=tk.BOTH, ipadx=8, ipady=18, pady=(25, 12), padx=20)
entry.bind("<Button-1>", copy_result)

toggle_btn = tk.Button(root, text="🌞 Light Mode", font="Helvetica 12 bold", bd=0, command=toggle_theme)
toggle_btn.pack(fill=tk.X, padx=20, pady=(0, 5))

history_btn = tk.Button(root, text="📜 Show/Hide History", font="Helvetica 12 bold", bd=0, command=toggle_history)
history_btn.pack(fill=tk.X, padx=20, pady=(0, 5))

clear_history_btn = tk.Button(root, text="🗑️ Clear History", font="Helvetica 12 bold", bd=0, command=clear_history)
clear_history_btn.pack(fill=tk.X, padx=20, pady=(0, 10))

history_frame = tk.Frame(root, height=110)
history_text = scrolledtext.ScrolledText(history_frame, font="Helvetica 11", height=6, state=tk.DISABLED, wrap=tk.WORD, bd=0)
history_text.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(expand=True, fill="both", padx=15, pady=10)

button_texts = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
    ["⌫", ".", "(", ")"]
]

buttons_list = []

for i, row in enumerate(button_texts):
    for j, txt in enumerate(row):
        btn = tk.Button(button_frame, text=txt, font="Helvetica 18 bold", bd=0, relief=tk.FLAT)
        btn.grid(row=i, column=j, sticky="nsew", padx=6, pady=6, ipadx=8, ipady=10)
        btn.bind("<Button-1>", click)
        buttons_list.append(btn)

for i in range(5):
    button_frame.rowconfigure(i, weight=1)
for j in range(4):
    button_frame.columnconfigure(j, weight=1)

apply_theme()
root.mainloop()
