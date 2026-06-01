# ==========================================
# SYNOPTIMESH — DESKTOP NODE
# ==========================================

import os
import time
import subprocess
import webbrowser
from email_feature import push_mail
import pyautogui
import cv2

from ai_engine     import ask_ai, start_ai_session
from search_engine import suggest_commands, normalize
from rapidfuzz     import fuzz
import win32com.client
import pytesseract
import pyttsx3
# ==========================================
# APP PATHS
# ==========================================

APPS = {
    "chrome":        ("exe", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
    "vscode":        ("exe", "code"),
    "spotify":       ("uri", "spotify:"),
    "discord":       ("uri", "discord:"),
    "notepad":       ("exe", "notepad.exe"),
    "calculator":    ("exe", "calc.exe"),
    "file explorer": ("exe", "explorer.exe"),
    "task manager":  ("exe", "taskmgr.exe"),
    "settings":      ("uri", "ms-settings:"),
    "paint":         ("exe", "mspaint.exe"),
    "outlook": ("exe", "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE"),
}
def launch_app(app_name):
    if app_name not in APPS:
        print(f"\n[DESKTOP] App '{app_name}' not found.\n")
        return

    kind, target = APPS[app_name]

    try:
        if kind == "uri":
            import os
            os.startfile(target)
        else:
            subprocess.Popen(target)
        print(f"\n[DESKTOP] Launched '{app_name}'.\n")

    except FileNotFoundError:
        print(f"\n[DESKTOP] Could not find '{app_name}'. Is it installed?\n")
    except OSError as e:
        print(f"\n[DESKTOP] Failed to launch '{app_name}': {e}\n")
# ==========================================
# FUZZY COMMAND MATCHER
# ==========================================

COMMAND_KEYWORDS = {
    "web search":      ["search", "google", "look up", "find"],
    "youtube search":  ["youtube", "play", "video", "watch"],
    "write notepad":   ["write", "notepad", "type", "note"],
    "calculator":      ["calculator", "calc", "calculate", "math", "compute"],
    "camera":          ["camera", "photo", "selfie", "video", "webcam", "record", "picture"],
    "ai assistant":    ["ai", "ask", "chat", "groq", "assistant", "synoptimesh"],
    "screenshot":      ["screenshot", "capture", "screen"],
    "open app":        ["open", "launch", "start", "run"],
    "lock screen":     ["lock", "lock screen"],
    "shutdown":        ["shutdown", "shut down", "power off", "turn off"],
    "restart":         ["restart", "reboot"],
}

def find_best_match(user_input):

    best_score   = 0
    best_command = None
    user_input   = normalize(user_input)

    for command, keywords in COMMAND_KEYWORDS.items():
        for keyword in keywords:
            score = max(
                fuzz.partial_ratio(user_input, keyword),
                fuzz.token_sort_ratio(user_input, keyword)
            )
            if score > best_score:
                best_score   = score
                best_command = command

    if best_score > 85:
        return best_command, best_score

    return None, 0

# ==========================================
# WEB SEARCH
# ==========================================

def web_search(query=None):

    if not query:
        query = input("\nSearch query: ").strip()

    print(f"\n[DESKTOP] Searching Google: {query}\n")

    # AI answers first
    ask_ai(query)

    time.sleep(2)

    # Then open browser fullscreen
    webbrowser.open(f"https://www.google.com/search?q={query}")
    time.sleep(2)
    pyautogui.press("f11")

# ==========================================
# YOUTUBE SEARCH
# ==========================================

def youtube_search(query=None):

    if not query:
        query = input("\nYouTube search: ").strip()

    print(f"\n[DESKTOP] Searching YouTube: {query}\n")

    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    time.sleep(2)
    pyautogui.press("f11")

# ==========================================
# WRITE IN NOTEPAD
# ==========================================

def write_in_notepad(text=None):

    if not text:
        text = input("\nWhat to write: ").strip()

    print(f"\n[DESKTOP] Writing in Notepad...\n")

    subprocess.Popen(["notepad.exe"])
    time.sleep(1.5)
    pyautogui.write(text, interval=0.03)

# ==========================================
# CALCULATOR
# ==========================================

def open_calculator(expression=None):

    print("\n[DESKTOP] Opening Calculator...\n")
    subprocess.Popen(["calc.exe"])
    time.sleep(1.5)

    if expression:
        # Type the expression into calculator
        pyautogui.write(expression, interval=0.05)
        print(f"[DESKTOP] Typed: {expression}\n")
    else:
        expr = input("\nEnter expression to calculate (or press Enter to skip): ").strip()
        if expr:
            pyautogui.write(expr, interval=0.05)

# =========================================
# OCR SCREEN READ AND SUMMARY FUNCTION
# =========================================

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\User.DESKTOP-53UC8KT\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
engine = pyttsx3.init()

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    speaker.Speak(str(text))

def speak_long_text(text):

    chunk_size = 300

    for i in range(0, len(text), chunk_size):

        speak(text[i:i+chunk_size])


def ocr_reading():

    print("\n[SYNOPTIMESH OCR NODE]")
    print("Capturing screen...\n")

    try:

        screenshot = pyautogui.screenshot()

        text = pytesseract.image_to_string(
            screenshot,
            config="--oem 3 --psm 6"
        )
        summary_prompt = f"""
           Summarize the following screen content in 3 concise sentences.

        TEXT:
        {text}
         """

        summary = ask_ai( f"Summarize this screen content:\n\n{text}")

        print("\nSUMMARY:")
        print(summary)
        speak(summary)
        if text.strip():

            print("\n" + "=" * 60)
            print("DETECTED TEXT")
            print("=" * 60)
            print(text)
            print("=" * 60)

            speak("Text detected on screen.")

        else:

            speak("No readable text detected.")

    except Exception as e:

        print("\nERROR:")
        print(e)
        traceback.print_exc()
        speak("OCR operation failed.")

# ==========================================
# CAMERA FUNCTIONS
# ==========================================

def get_camera():
    for index in [0, 1, 2]:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"[CAMERA] Found camera at index {index}")
            return cap
    return None

def camera_menu():

    while True:

        print("""
========== CAMERA ==========
1. SELFIE    -> Take a photo
2. VIDEO     -> Record video
3. STREAM    -> Live preview
4. BACK      -> Return
""")

        cmd = input("Camera Command: ").strip().upper()

        if cmd in ["1", "SELFIE", "PHOTO", "TAKE PHOTO", "TAKE SELFIE"]:
            take_photo()

        elif cmd in ["2", "VIDEO", "RECORD", "RECORD VIDEO"]:
            record_video()

        elif cmd in ["3", "STREAM", "PREVIEW", "LIVE"]:
            live_preview()

        elif cmd in ["4", "BACK", "RETURN", "EXIT"]:
            print("\n[CAMERA] Returning...\n")
            break

        else:
            print("\n[!] Unknown camera command.\n")

def take_photo():

    print("\n[CAMERA] Opening camera...\n")

    cap = get_camera()
    if cap is None:
        print("[CAMERA] No camera found.\n")
        return

    print("[CAMERA] Press SPACE to take photo, ESC to cancel.\n")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Synoptimesh Camera — SPACE to capture", frame)

        key = cv2.waitKey(1)

        if key == 32:   # SPACE
            path = os.path.join(
    os.path.expanduser("~"),
    "OneDrive", "Desktop",
    f"synoptimesh_photo_{int(time.time())}.png"
)
            cv2.imwrite(path, frame)
            print(f"\n[CAMERA] Photo saved: {path}\n")
            break

        elif key == 27:  # ESC
            print("\n[CAMERA] Cancelled.\n")
            break

    cap.release()
    cv2.destroyAllWindows()

def record_video():

    try:
        duration = input("\nRecord duration in seconds (default 10): ").strip()
        duration = int(duration) if duration.isdigit() and duration != "" else 10
    except:
        duration = 10

    print(f"\n[CAMERA] Recording {duration}s video...\n")

    cap = get_camera()
    if cap is None:
        print("[CAMERA] No camera found.\n")
        return

    path   = os.path.join(
        os.path.expanduser("~"),
        "OneDrive", "Desktop",
        f"synoptimesh_video_{int(time.time())}.avi"
    )
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out    = cv2.VideoWriter(path, fourcc, 20.0, (640, 480))
    start  = time.time()

    print("[CAMERA] Recording... Press ESC to stop early.\n")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        out.write(frame)
        cv2.imshow("Synoptimesh — Recording", frame)

        elapsed   = time.time() - start
        remaining = duration - int(elapsed)
        print(f"\r[CAMERA] Time remaining: {remaining}s   ", end="")

        if cv2.waitKey(1) == 27 or elapsed >= duration:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\n\n[CAMERA] Video saved: {path}\n")
    
def live_preview():

    print("\n[CAMERA] Live preview. Press ESC to close.\n")

    cap = get_camera()
    if cap is None:
        print("[CAMERA] No camera found.\n")
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Synoptimesh — Live Preview", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ==========================================
# HELP FUNCTION
# ==========================================
def help_fn():

    engine = pyttsx3.init()

    engine.say("HELP ME")
    engine.runAndWait()

# ==========================================
# SCREENSHOT
# ==========================================

def take_screenshot():

    # Works for both normal and OneDrive Desktop
    path = os.path.join(
        os.path.expanduser("~"),
        "OneDrive",
        "Desktop",
        f"synoptimesh_screenshot_{int(time.time())}.png"
    )

    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    print(f"\n[DESKTOP] Screenshot saved: {path}\n")
"""
# ==========================================
# LOCK / SHUTDOWN / RESTART
# ==========================================

def lock_screen():
    print("\n[DESKTOP] Locking screen...\n")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def shutdown():
    confirm = input("\nShutdown? (yes/no): ").strip().lower()
    if confirm == "yes":
        os.system("shutdown /s /t 10")
    else:
        print("Cancelled.\n")

def restart():
    confirm = input("\nRestart? (yes/no): ").strip().lower()
    if confirm == "yes":
        os.system("shutdown /r /t 10")
    else:
        print("Cancelled.\n")
"""
# ==========================================
# DESKTOP NODE MAIN LOOP
# ==========================================

def desktop_node():

    while True:

        print("""
========================================
           DESKTOP NODE
========================================
SEARCH         -> Web Search
YOUTUBE        -> YouTube Search
WRITE          -> Write in Notepad
CALC           -> Calculator

AI             -> AI Assistant (Groq)
CAMERA         -> Camera (photo/video/selfie)s
SS             -> Screenshot
OPEN           -> Open App

HELP           -> alert help
MAIL           -> Send mail
SCREENSUM      -> summarizes the screen

[FUTURE TASKS: TASK8, TASK9, TASK10...]
========================================
""")

        user_input = input("Desktop Command: ").strip()

        # Show suggestions
        suggestions = suggest_commands(user_input)
        if suggestions:
            print("\nSuggestions:")
            for s in suggestions:
                print(f"  - {s}")

        cmd = user_input.upper()

        # ----------------------------------------
        # DIRECT COMMANDS
        # ----------------------------------------

        '''if cmd == "RETURN":
            print("\n[DESKTOP] Returning to Master Hub...\n")
            break'''

        if cmd == "SEARCH":
            web_search()

        elif cmd == "YOUTUBE":
            youtube_search()

        elif cmd == "WRITE":
            write_in_notepad()

        elif cmd == "CALC":
            open_calculator()

        elif cmd == "AI":
            start_ai_session()

        elif cmd == "CAMERA":
            camera_menu()

        elif cmd == "SS":
            take_screenshot()

        elif cmd == "OPEN":
            app = input("\nApp to open: ").strip().lower()
            if app in APPS:
                launch_app(app)
            else:
                print(f"\n[DESKTOP] App '{app}' not found in list.\n")
                print("Available:", ", ".join(APPS.keys()))

        elif cmd == "HELP":
            help_fn()

        elif cmd == "MAIL":
            push_mail()

        elif cmd == "SCREENSUM":
            ocr_reading()

        # ----------------------------------------
        # FUTURE TASKS — add below as needed
        # ----------------------------------------

        elif cmd == "TASK8":
            print("\n[DESKTOP] TASK8 — Not assigned yet.\n")

        elif cmd == "TASK9":
            print("\n[DESKTOP] TASK9 — Not assigned yet.\n")

        elif cmd == "TASK10":
            print("\n[DESKTOP] TASK10 — Not assigned yet.\n")

        # ----------------------------------------
        # NATURAL LANGUAGE FALLBACK
        # ----------------------------------------

        else:

            # Long sentence questions → AI
            if len(user_input.split()) >= 4:
                ask_ai(user_input)
                continue

            # Fuzzy match short inputs
            matched, score = find_best_match(user_input)

            if matched == "web search":
                web_search(user_input)

            elif matched == "youtube search":
                youtube_search(user_input)

            elif matched == "write notepad":
                write_in_notepad()

            elif matched == "calculator":
                open_calculator(user_input)

            elif matched == "camera":
                camera_menu()

            elif matched == "ai assistant":
                start_ai_session()

            elif matched == "screenshot":
                take_screenshot()

            elif matched == "help":
                help_fn()

            elif matched == "mail":
                push_mail()

            elif matched == "summarize screen":
                ocr_reading()

            else:
                # Final fallback — ask AI
                ask_ai(user_input)






