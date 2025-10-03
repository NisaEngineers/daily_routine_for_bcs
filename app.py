# app.py
import os
import time
import importlib
import threading
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

from gtts import gTTS
import pygame

# --------- CONFIG ---------
TZ = ZoneInfo("Asia/Dhaka")
AUDIO_DIR = "notifier_audio"
DB_FILE = "study_progress.db"
os.makedirs(AUDIO_DIR, exist_ok=True)

GENTLE_PREFIX = "Gentle reminder. "
GENTLE_SUFFIX = " Stay steady and kind to yourself."

# --------- PLAN LOADER ---------
import plan_v2
PLAN = plan_v2.PLAN
PLAN_PATH = plan_v2.__file__
last_mtime = os.path.getmtime(PLAN_PATH)

def reload_plan_if_updated():
    global PLAN, last_mtime
    try:
        mtime = os.path.getmtime(PLAN_PATH)
        if mtime != last_mtime:
            importlib.reload(plan_v2)
            PLAN = plan_v2.PLAN
            last_mtime = mtime
            log_message(f"plan.py reloaded at {datetime.now(TZ).strftime('%H:%M:%S')}")
            refresh_schedule()
            update_progress()
    except Exception as e:
        log_message(f"Error reloading plan: {e}")

# --------- DB ---------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS progress (
        date TEXT,
        time TEXT,
        msg TEXT,
        completed INTEGER,
        ts TEXT
    )""")
    conn.commit()
    conn.close()

def set_completion(date_key: str, hhmm: str, msg: str, completed: int):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Upsert-like behavior: delete old row and insert new
    cur.execute("DELETE FROM progress WHERE date=? AND time=? AND msg=?", (date_key, hhmm, msg))
    cur.execute(
        "INSERT INTO progress (date, time, msg, completed, ts) VALUES (?, ?, ?, ?, ?)",
        (date_key, hhmm, msg, completed, datetime.now(TZ).isoformat())
    )
    conn.commit()
    conn.close()

def get_completion_map(date_key: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT time, msg, completed FROM progress WHERE date=?", (date_key,))
    rows = cur.fetchall()
    conn.close()
    # key by (time, msg) to avoid collisions if messages repeat at different times
    return {(t, m): c for (t, m, c) in rows}

def get_overall_stats():
    """Compute overall progress across all planned days."""
    total_blocks = 0
    completed_blocks = 0
    for day, blocks in PLAN.items():
        total_blocks += len(blocks)
        cm = get_completion_map(day)
        for hhmm, msg in blocks:
            if cm.get((hhmm, msg), 0) == 1:
                completed_blocks += 1
    return completed_blocks, total_blocks

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

# --------- GUI + NOTIFIER THREAD ---------
running = False
notified_times = set()
current_day = None
exam_name = "BCS Special Preli"
exam_marks = 200

checkbox_vars = {}  # {(hhmm, msg): tk.BooleanVar}

def log_message(msg: str):
    gui_log.config(state="normal")
    gui_log.insert(tk.END, msg + "\n")
    gui_log.see(tk.END)
    gui_log.config(state="disabled")

def notifier_loop():
    global current_day, notified_times, running
    log_message("Voice notifier started. Timezone: Asia/Dhaka.")
    last_reload_check = time.time()

    while running:
        now = datetime.now(TZ)

        # Hot-reload plan once per minute
        if time.time() - last_reload_check >= 60:
            reload_plan_if_updated()
            last_reload_check = time.time()

        day_key = get_today_key(now)

        # New day setup
        if current_day != day_key:
            current_day = day_key
            notified_times.clear()
            refresh_schedule()
            update_progress()
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

def on_checkbox_toggle(day_key: str, hhmm: str, msg: str, var: tk.BooleanVar):
    set_completion(day_key, hhmm, msg, int(var.get()))
    update_progress()
    log_message(f"Marked: [{day_key}] {hhmm} — {msg} -> {'Done' if var.get() else 'Undone'}")

def refresh_schedule():
    # Clear previous widgets
    for widget in schedule_inner.winfo_children():
        widget.destroy()
    checkbox_vars.clear()

    today = get_today_key(datetime.now(TZ))
    blocks = PLAN.get(today, [])
    completion_map = get_completion_map(today)

    # Build list with checkboxes
    for hhmm, msg in blocks:
        var = tk.BooleanVar(value=bool(completion_map.get((hhmm, msg), 0)))
        checkbox_vars[(hhmm, msg)] = var

        row = tk.Frame(schedule_inner)
        row.pack(fill="x", padx=5, pady=2)

        chk = tk.Checkbutton(
            row, text=f"{hhmm} — {msg}", variable=var,
            command=lambda d=today, t=hhmm, m=msg, v=var: on_checkbox_toggle(d, t, m, v)
        )
        chk.pack(side="left", anchor="w")

def update_progress():
    completed, total = get_overall_stats()
    pct = (completed / total * 100) if total else 0.0
    progress_bar['value'] = pct
    progress_label.config(text=f"Progress: {completed}/{total} blocks ({pct:.1f}%)")

def manual_reload():
    reload_plan_if_updated()
    refresh_schedule()
    update_progress()

# --------- GUI ---------
root = tk.Tk()
root.title("📚 Study Voice Notifier")
root.geometry("900x650")

# Top controls
top_frame = tk.Frame(root)
top_frame.pack(pady=5, fill="x")

start_btn = tk.Button(top_frame, text="▶ Start", command=start_notifier, bg="green", fg="white", width=10)
start_btn.pack(side="left", padx=5)

stop_btn = tk.Button(top_frame, text="■ Stop", command=stop_notifier, bg="red", fg="white", width=10)
stop_btn.pack(side="left", padx=5)

reload_btn = tk.Button(top_frame, text="⟳ Reload Plan", command=manual_reload, width=12)
reload_btn.pack(side="left", padx=5)

exam_label = tk.Label(top_frame, text=f"Exam: {exam_name} ({exam_marks} marks)", font=("Arial", 10, "bold"))
exam_label.pack(side="right", padx=10)

# Progress panel
progress_frame = tk.LabelFrame(root, text="Overall Progress", font=("Arial", 10, "bold"))
progress_frame.pack(fill="x", padx=10, pady=5)

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(side="left", padx=10, pady=8)

progress_label = tk.Label(progress_frame, text="Progress: 0/0 blocks (0.0%)", font=("Arial", 10))
progress_label.pack(side="left", padx=10)

# Schedule panel
schedule_frame = tk.LabelFrame(root, text="Today's Schedule", font=("Arial", 10, "bold"))
schedule_frame.pack(fill="both", expand=False, padx=10, pady=5)

# A scrollable inner frame for checkboxes
schedule_canvas = tk.Canvas(schedule_frame, height=250)
schedule_scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", command=schedule_canvas.yview)
schedule_inner = tk.Frame(schedule_canvas)

schedule_inner.bind(
    "<Configure>",
    lambda e: schedule_canvas.configure(scrollregion=schedule_canvas.bbox("all"))
)
schedule_canvas.create_window((0, 0), window=schedule_inner, anchor="nw")
schedule_canvas.configure(yscrollcommand= schedule_scrollbar.set)

schedule_canvas.pack(side="left", fill="both", expand=True)
schedule_scrollbar.pack(side="right", fill="y")

# Log panel
log_frame = tk.LabelFrame(root, text="Notifier Log", font=("Arial", 10, "bold"))
log_frame.pack(fill="both", expand=True, padx=10, pady=5)
gui_log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled")
gui_log.pack(fill="both", expand=True, padx=5, pady=5)

# --------- INIT & RUN ---------
init_db()
refresh_schedule()
update_progress()

root.mainloop()
