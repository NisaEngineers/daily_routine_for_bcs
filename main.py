import os, time, importlib, threading
from datetime import datetime
from zoneinfo import ZoneInfo
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from gtts import gTTS
import pygame

# --------- CONFIG ---------
TZ = ZoneInfo("Asia/Dhaka")
AUDIO_DIR = "notifier_audio"
LOG_FILE = "study_log.txt"
os.makedirs(AUDIO_DIR, exist_ok=True)

GENTLE_PREFIX = "Gentle reminder. "
GENTLE_SUFFIX = " Stay steady and kind to yourself."

# --------- TTS + PLAYBACK ---------
def msg_to_filename(msg: str) -> str:
    import hashlib
    digest = hashlib.sha1(msg.encode("utf-8")).hexdigest()[:12]
    return os.path.join(AUDIO_DIR, f"{digest}.mp3")

def synthesize(msg: str) -> str:
    path = msg_to_filename(msg)
    if not os.path.exists(path):
        lang = "bn" if any("\u0980" <= ch <= "\u09FF" for ch in msg) else "en"
        gTTS(text=msg, lang=lang, slow=False).save(path)
    return path

def play_audio(path: str):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    sound = pygame.mixer.Sound(path)
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)

# --------- HELPERS ---------
def get_today_key(now: datetime) -> str:
    return now.strftime("%Y-%m-%d")

def make_spoken_message(hhmm: str, msg: str) -> str:
    return f"{GENTLE_PREFIX}{hhmm}. {msg}{GENTLE_SUFFIX}"

# --------- PLAN LOADER ---------
from plan import PLAN
import plan
PLAN = PLAN
PLAN_PATH = plan.__file__
last_mtime = os.path.getmtime(PLAN_PATH)

def reload_plan_if_updated():
    global PLAN, last_mtime
    try:
        mtime = os.path.getmtime(PLAN_PATH)
        if mtime != last_mtime:
            importlib.reload(plan)
            PLAN = plan.PLAN
            last_mtime = mtime
            log_message(f"plan.py reloaded at {datetime.now(TZ).strftime('%H:%M:%S')}")
            refresh_schedule()
    except Exception as e:
        log_message(f"Error reloading plan: {e}")

# --------- GUI + NOTIFIER THREAD ---------
running = False
notified_times = set()
current_day = None
exam_name = "BCS Special Preli"
exam_marks = 200

def log_message(msg: str):
    gui_log.config(state="normal")
    gui_log.insert(tk.END, msg + "\n")
    gui_log.see(tk.END)
    gui_log.config(state="disabled")

def save_study_log(subject: str, duration: int, marks: int):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(TZ)} | {subject} | {duration} min | {marks} marks\n")

def prompt_study_feedback(subject: str):
    duration = simpledialog.askinteger("Study Duration", f"How many minutes did you actually study for {subject}?", minvalue=0)
    marks = simpledialog.askinteger("Self-Assessment", f"Marks for {subject} (0–{exam_marks}):", minvalue=0, maxvalue=exam_marks)
    if duration is not None and marks is not None:
        save_study_log(subject, duration, marks)
        log_message(f"Logged: {subject} | {duration} min | {marks} marks")

def notifier_loop():
    global current_day, notified_times, running
    log_message("Voice notifier started. Timezone: Asia/Dhaka.")
    last_reload_check = time.time()

    while running:
        now = datetime.now(TZ)

        if time.time() - last_reload_check >= 60:
            reload_plan_if_updated()
            last_reload_check = time.time()

        day_key = get_today_key(now)

        if current_day != day_key:
            current_day = day_key
            notified_times.clear()
            refresh_schedule()
            blocks = PLAN.get(day_key, [])
            log_message(f"\nNew day: {current_day} — {len(blocks)} blocks loaded.")

        blocks = PLAN.get(day_key, [])
        for hhmm, msg in blocks:
            if hhmm in notified_times:
                continue
            h, m = map(int, hhmm.split(":"))
            scheduled = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if now >= scheduled:
                spoken = make_spoken_message(hhmm, msg)
                audio_path = synthesize(spoken)
                log_message(f"[{now.strftime('%H:%M:%S')}] Triggering: {hhmm} -> {msg}")
                play_audio(audio_path)
                notified_times.add(hhmm)
                # After block, prompt for feedback
                root.after(2000, lambda subj=msg: prompt_study_feedback(subj))

        time.sleep(5)

def start_notifier():
    global running
    if not running:
        running = True
        threading.Thread(target=notifier_loop, daemon=True).start()
        log_message("Notifier started.")

def stop_notifier():
    global running
    running = False
    log_message("Notifier stopped.")

def refresh_schedule():
    schedule_box.config(state="normal")
    schedule_box.delete("1.0", tk.END)
    today = get_today_key(datetime.now(TZ))
    blocks = PLAN.get(today, [])
    for hhmm, msg in blocks:
        schedule_box.insert(tk.END, f"{hhmm} — {msg}\n")
    schedule_box.config(state="disabled")

def set_exam_info():
    global exam_name, exam_marks
    name = simpledialog.askstring("Exam Name", "Enter exam name:", initialvalue=exam_name)
    marks = simpledialog.askinteger("Exam Marks", "Enter total marks:", initialvalue=exam_marks)
    if name: exam_name = name
    if marks: exam_marks = marks
    exam_label.config(text=f"Exam: {exam_name} ({exam_marks} marks)")

# --------- GUI ---------
root = tk.Tk()
root.title("📚 Study Voice Notifier")
root.geometry("700x500")

# Top controls
top_frame = tk.Frame(root)
top_frame.pack(pady=5)

start_btn = tk.Button(top_frame, text="▶ Start", command=start_notifier, bg="green", fg="white", width=10)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(top_frame, text="■ Stop", command=stop_notifier, bg="red", fg="white", width=10)
stop_btn.grid(row=0, column=1, padx=5)

exam_btn = tk.Button(top_frame, text="⚙ Exam Info", command=set_exam_info, width=12)
exam_btn.grid(row=0, column=2, padx=5)

exam_label = tk.Label(top_frame, text=f"Exam: {exam_name} ({exam_marks} marks)", font=("Arial", 10, "bold"))
exam_label.grid(row=0, column=3, padx=10)

# Schedule panel
schedule_frame = tk.LabelFrame(root, text="Today's Schedule", font=("Arial", 10, "bold"))
schedule_frame.pack(fill="x", padx=10, pady=5)
schedule_box = scrolledtext.ScrolledText(schedule_frame, height=8, state="disabled")
schedule_box.pack(fill="x", padx=5, pady=5)

# Log panel
log_frame = tk.LabelFrame(root, text="Notifier Log", font=("Arial", 10, "bold"))
log_frame.pack(fill="both", expand=True, padx=10, pady=5)
gui_log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled")
gui_log.pack(fill="both", expand=True, padx=5, pady=5)

refresh_schedule()
root.mainloop()

