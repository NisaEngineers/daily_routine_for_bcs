# filename: voice_notifier.py
import os
import time
import importlib
from datetime import datetime
from zoneinfo import ZoneInfo

from gtts import gTTS
import pygame

# --------- CONFIG ---------
TZ = ZoneInfo("Asia/Dhaka")
AUDIO_DIR = "notifier_audio"
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
import plan   # initial import
PLAN = plan.PLAN
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
            print(f"[{datetime.now(TZ).strftime('%H:%M:%S')}] plan.py reloaded.")
    except Exception as e:
        print("Error reloading plan:", e)

# --------- MAIN LOOP ---------
def main_loop():
    print("Voice notifier started. Timezone: Asia/Dhaka.")
    current_day = None
    notified_times = set()
    last_reload_check = time.time()

    while True:
        now = datetime.now(TZ)

        # Check for plan updates every 60s
        if time.time() - last_reload_check >= 60:
            reload_plan_if_updated()
            last_reload_check = time.time()

        day_key = get_today_key(now)

        # Reset daily tracker at midnight
        if current_day != day_key:
            current_day = day_key
            notified_times.clear()
            blocks = PLAN.get(day_key, [])
            print(f"\nNew day: {current_day} — {len(blocks)} blocks loaded:")
            for t, _ in blocks:
                print(f"  - {t}")

        blocks = PLAN.get(day_key, [])
        if not blocks:
            time.sleep(5)
            continue

        for hhmm, msg in blocks:
            if hhmm in notified_times:
                continue

            h, m = map(int, hhmm.split(":"))
            scheduled = now.replace(hour=h, minute=m, second=0, microsecond=0)

            if now >= scheduled:
                spoken = make_spoken_message(hhmm, msg)
                audio_path = synthesize(spoken)
                print(f"[{now.strftime('%H:%M:%S')}] Triggering: {hhmm} -> {msg}")
                play_audio(audio_path)
                notified_times.add(hhmm)

        time.sleep(5)

if __name__ == "__main__":
    main_loop()
