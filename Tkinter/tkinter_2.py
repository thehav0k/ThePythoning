## Mini Scientific Calculator

import tkinter as tk
from tkinter import ttk
import math

# Colors and fonts
BG_COLOR = "#1e1e2f"
BTN_COLOR = "#2563eb"
BTN_HOVER_COLOR = "#1e40af"
BTN_TEXT_COLOR = "#ffffff"
ENTRY_BG = "#2d2d3c"
ENTRY_FG = "#ffffff"
TEXT_COLOR = "#e5e7eb"

FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 14, "bold")
TITLE_COLOR = "#ffffff"

# Calculator logic
def on_click(text):
    if text == "C":
        entry_var.set("")
    elif text == "⌫":
        entry_var.set(entry_var.get()[:-1])
    elif text == "=":
        try:
            expr = entry_var.get().replace("^", "**")
            result = str(eval(expr, {"__builtins__": None}, math.__dict__))
            entry_var.set(result)
        except Exception:
            entry_var.set("Error")
    elif text in ("sin", "cos", "tan", "log"):
        entry_var.set(entry_var.get() + text + "(")
    else:
        entry_var.set(entry_var.get() + text)

root = tk.Tk()
root.title("Scientific Calculator")
root.configure(bg=BG_COLOR)
root.minsize(400, 560)

# Style for ttk buttons
style = ttk.Style(root)
style.theme_use("clam")

style.configure("Calc.TButton",
                font=FONT,
                foreground=BTN_TEXT_COLOR,
                background=BTN_COLOR,
                padding=8,
                borderwidth=0)
style.map("Calc.TButton",
          background=[('active', BTN_HOVER_COLOR)],
          foreground=[('disabled', '#888'), ('!disabled', BTN_TEXT_COLOR)])

# Title
tk.Label(root, text="Scientific Calculator", font=TITLE_FONT, bg=BG_COLOR, fg=TITLE_COLOR) \
    .pack(pady=(15, 5))

# Entry
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG,
                 insertbackground=ENTRY_FG, relief=tk.FLAT, justify='right')
entry.pack(fill=tk.X, padx=20, pady=10, ipady=10)

# Button layout
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(padx=12, pady=10, fill=tk.BOTH, expand=True)

buttons = [
    ["7", "8", "9", "/", "sin"],
    ["4", "5", "6", "*", "cos"],
    ["1", "2", "3", "-", "tan"],
    ["0", ".", "^", "+", "log"],
    ["(", ")", "C", "=", "⌫"]
]

for r, row in enumerate(buttons):
    btn_frame.grid_rowconfigure(r, weight=1)
    for c, text in enumerate(row):
        btn_frame.grid_columnconfigure(c, weight=1)
        b = ttk.Button(
            btn_frame, text=text, style="Calc.TButton",
            command=lambda t=text: on_click(t)
        )
        b.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

# Keyboard bindings
for func in ["sin", "cos", "tan", "log"]:
    root.bind(f'<Alt-{func[0]}>', lambda e, f=func: entry_var.set(entry_var.get() + f + "("))

root.mainloop()