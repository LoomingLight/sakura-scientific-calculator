# Sakura Calculator - A Themed Scientific Calculator with Voice Input #
# Developed by Looming Light #
# This code creates a scientific calculator GUI with a cherry blossom theme #
# Supporting both manual and voice inputs for calculations. #

# ---------------------------- IMPORTS --------------------------- #

import tkinter as tk
import math
import speech_recognition as sr
import pyttsx3
import threading

# --------------------------- THEME CONFIGURATION ---------------------------
# A "Pop" Cherry Blossom theme with high contrast and varied elements
THEME = {
    'bg_main': '#FFB7C5',      # Main body: Cherry Blossom Pink
    'bg_screen': '#2E1A25',    # Display background: Dark cherry/brown
    'fg_screen': '#FFF0F5',    # Display text: Lavender blush
    'btn_num_bg': '#FFF0F5',   # Numbers: Very pale pink/white
    'btn_num_fg': '#C71585',   # Numbers text: Medium Violet Red
    'btn_op_bg': '#FF69B4',    # Basic Ops (+, -, *): Hot Pink
    'btn_op_fg': '#FFFFFF',    # Basic Ops text: White
    'btn_sci_bg': '#DDA0DD',   # Sci Ops (sin, cos): Plum/Lavender
    'btn_sci_fg': '#4B0082',   # Sci Ops text: Indigo
    'btn_call_bg': '#FF1493',  # Call to action (Equals, Mic): Deep Pink
    'btn_active': '#FFC0CB',   # Hover/Active state
}

# Update these paths if needed
LOGO_PATH = 'logo.png'
MIC_PATH = 'microphone.png'

# Initialize Text-to-Speech
try:
    engine = pyttsx3.init()
except:
    engine = None

# --------------------------- HELPER FUNCTIONS ---------------------------
def load_safe_img(path):
    """Safely loads an image, returning None if it fails."""
    try:
        return tk.PhotoImage(file=path)
    except Exception:
        return None

def speak(text):
    """Non-blocking TTS."""
    if not engine: return
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except: pass
    threading.Thread(target=run, daemon=True).start()

def update_display(value):
    """Updates the main calculator screen."""
    entryField.delete(0, tk.END)
    entryField.insert(0, str(value))

# --------------------------- CORE LOGIC ---------------------------
BINARY_OPS = {
    'ADD': lambda a, b: a + b, 'PLUS': lambda a, b: a + b,
    'SUBTRACT': lambda a, b: a - b, 'MINUS': lambda a, b: a - b,
    'MULTIPLY': lambda a, b: a * b, 'TIMES': lambda a, b: a * b,
    'DIVIDE': lambda a, b: a / b, 'BY': lambda a, b: a / b,
    'MOD': lambda a, b: a % b, 'POWER': lambda a, b: a ** b,
}
UNARY_OPS = {
    'ROOT': math.sqrt, 'SQRT': math.sqrt,
    'SIN': lambda a: math.sin(math.radians(a)),
    'COS': lambda a: math.cos(math.radians(a)),
    'TAN': lambda a: math.tan(math.radians(a)),
    'LOG': math.log10, 'LN': math.log,
    'SQUARE': lambda a: a**2, 'CUBE': lambda a: a**3,
    'FACTORIAL': lambda a: math.factorial(int(a))
}

def process_input(value):
    current_text = entryField.get()
    try:
        if value == 'C':
            entryField.delete(len(current_text) - 1, tk.END)
        elif value == 'CE':
            entryField.delete(0, tk.END)
        elif value == '=':
            expr = current_text.replace(chr(247), '/').replace('x\u02b8', '**')
            update_display(eval(expr))
        elif value in ['sinθ', 'cosθ', 'tanθ']:
            update_display(getattr(math, value[:-1])(math.radians(eval(current_text))))
        elif value in ['sinh', 'cosh', 'tanh']:
             update_display(getattr(math, value)(eval(current_text)))
        elif value == '√': update_display(math.sqrt(eval(current_text)))
        elif value == 'ln': update_display(math.log(eval(current_text)))
        elif value == 'log₁₀': update_display(math.log10(eval(current_text)))
        elif value == 'x!': update_display(math.factorial(int(eval(current_text))))
        elif value == chr(8731): update_display(eval(current_text) ** (1/3))
        elif value == 'x\u00B2': update_display(eval(current_text) ** 2)
        elif value == 'x\u00B3': update_display(eval(current_text) ** 3)
        elif value == 'x\u02b8': entryField.insert(tk.END, '**')
        elif value == 'π': entryField.insert(tk.END, math.pi)
        elif value == 'e': entryField.insert(tk.END, math.e)
        elif value == chr(247): entryField.insert(tk.END, '/')
        else: entryField.insert(tk.END, value)
    except:
        update_display("Error")

def voice_input():
    recognizer = sr.Recognizer()
    update_display("Listening...")
    root.update()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        command = recognizer.recognize_google(audio)
        update_display(command)
        root.update()
        speak(command)
        
        cmd_upper = command.upper()
        nums = []
        for w in cmd_upper.split():
            try: nums.append(float(w.replace(',','').replace('?','')))
            except: continue

        if len(nums) >= 2:
             for op in sorted(BINARY_OPS.keys(), key=len, reverse=True):
                 if op in cmd_upper:
                     res = BINARY_OPS[op](nums[0], nums[1])
                     update_display(res)
                     speak(str(res))
                     return
        if len(nums) >= 1:
             for op in sorted(UNARY_OPS.keys(), key=len, reverse=True):
                 if op in cmd_upper:
                     res = UNARY_OPS[op](nums[0])
                     update_display(res)
                     speak(str(res))
                     return
    except: update_display("Voice Error")

def get_btn_style(text):
    """Generates unique button styles based on their function."""
    base = {'font': ('Verdana', 16, 'bold'), 'bd': 4, 
            'relief': tk.RAISED, 'activebackground': THEME['btn_active']}
    if text.isdigit() or text == '.':
        base.update({'bg': THEME['btn_num_bg'], 'fg': THEME['btn_num_fg']})
    elif text in ['=', 'C', 'CE']:
        base.update({'bg': THEME['btn_call_bg'], 'fg': 'white', 'font': ('Verdana', 18, 'bold')})
    elif text in ['+', '-', '*', chr(247), '%']:
        base.update({'bg': THEME['btn_op_bg'], 'fg': THEME['btn_op_fg'], 'relief': tk.RIDGE})
    else:
        base.update({'bg': THEME['btn_sci_bg'], 'fg': THEME['btn_sci_fg'], 'font': ('Verdana', 14)})
    return base

# --------------------------- GUI SETUP ---------------------------
root = tk.Tk()
root.title('Sakura Calculator - Scientific Calculator with Voice Input')
root.config(bg=THEME['bg_main'])
root.geometry('900x650')
try: root.state('zoomed')
except: pass

for i in range(8): root.grid_columnconfigure(i, weight=1)
for i in range(7): root.grid_rowconfigure(i, weight=1)

# -- Top Section --
logo = load_safe_img(LOGO_PATH)
if logo:
    tk.Label(root, image=logo, bg=THEME['bg_main']).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

entryField = tk.Entry(root, font=('Consolas', 28, 'bold'), bg=THEME['bg_screen'], 
                      fg=THEME['fg_screen'], bd=8, relief=tk.SUNKEN, justify=tk.RIGHT, 
                      insertbackground='white')
entryField.grid(row=0, column=1 if logo else 0, columnspan=6 if logo else 7, sticky="nsew", padx=10, pady=15)

mic_img = load_safe_img(MIC_PATH)
tk.Button(root, image=mic_img, text="MIC" if not mic_img else "", 
          bg=THEME['btn_call_bg'], fg='white', bd=4, relief=tk.RAISED, 
          command=voice_input).grid(row=0, column=7, sticky="nsew", padx=5, pady=15)

# -- Buttons --
buttons = [
    "C", "CE", "√", "+", "π", "cosθ", "tanθ", "sinθ",
    "1", "2", "3", "-", "2π", "cosh", "tanh", "sinh",
    "4", "5", "6", "*", chr(8731), "x\u02b8", "x\u00B3", "x\u00B2",
    "7", "8", "9", chr(247), "ln", "deg", "rad", "e",
    "0", ".", "%", "=", "log₁₀", "(", ")", "x!"
]

r, c = 1, 0
for btn_text in buttons:
    tk.Button(root, text=btn_text, command=lambda b=btn_text: process_input(b), 
              **get_btn_style(btn_text)).grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
    c += 1
    if c > 7: r, c = r + 1, 0

root.mainloop()