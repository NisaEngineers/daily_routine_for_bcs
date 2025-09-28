# filename: voice_notifier.py
import os
import time
import hashlib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from gtts import gTTS
import pygame

# --------- CONFIG ---------
TZ = ZoneInfo("Asia/Dhaka")
AUDIO_DIR = "notifier_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Gentle prefix/suffix to make reminders feel kind and light
GENTLE_PREFIX = "Gentle reminder. "
GENTLE_SUFFIX = " Stay steady and kind to yourself."

# Your daily routine blocks mapped per date (YYYY-MM-DD)
# Time format: "HH:MM" 24-hour. Messages kept short and actionable.
PLAN = {
    # Sept 29
    "2025-09-29": [
        ("01:13", "C programming and pointers. Deep focus 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Data structures: arrays, stacks, queues. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "Bangla literature: Tagore, Nazrul. 2 hours."),
        ("15:30", "Coding or mental ability practice. 1 hour."),
        ("16:30", "Algorithms: complexity, divide and conquer. 90 minutes."),
        ("19:00", "Quick recall: Bangla grammar rules and key formulas. 1 hour."),
        ("20:00", "Numerical Analysis lecture / notes review. 1 hour."),
        ("21:30", "Wind down. Prepare tomorrow’s plan. 30 minutes."),
    ],

    # Sept 30
    "2025-09-30": [
        ("05:30", "Trees and heaps; Huffman coding. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Algorithms: sorting and hashing. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "English literature: Shakespeare and Romantics. 2 hours."),
        ("15:30", "Mental ability: series, analogy drills. 1 hour."),
        ("16:30", "Digital systems: Boolean algebra and K-map. 90 minutes."),
        ("19:00", "English grammar: voice, narration, error spotting. 1 hour."),
        ("20:00", "Digital Logic lecture / revisions. 1 hour."),
        ("21:30", "Wind down. Light review. 30 minutes."),
    ],

    # Oct 1
    "2025-10-01": [
        ("05:30", "Graphs: BFS, DFS, shortest paths. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Microprocessor: 8086 architecture and addressing modes. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "Bangladesh Affairs: constitution and liberation war. 2 hours."),
        ("15:30", "Math practice: algebra, probability. 1 hour."),
        ("16:30", "Batch MCQ: Numerical Analysis. Warm-up and attempt. 90 minutes."),
        ("19:00", "Quick recall: math formulas and key concepts. 1 hour."),
        ("20:00", "Review NA mistakes and notes. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 2
    "2025-10-02": [
        ("05:30", "Microprocessor: interrupts and memory management. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Operating Systems: processes, scheduling, deadlocks. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "English literature: Victorians and Moderns. 2 hours."),
        ("15:30", "Mental ability: puzzles and arrangements. 1 hour."),
        ("16:30", "Batch MCQ: Compiler Design. Attempt and review. 90 minutes."),
        ("19:00", "English grammar recap. 1 hour."),
        ("20:00", "Compiler notes quick pass. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 3
    "2025-10-03": [
        ("05:30", "Operating Systems: memory, paging, file systems. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "DBMS: ER, normalization, SQL basics. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "Bangladesh Affairs: economy and ICT policy. 2 hours."),
        ("15:30", "Math geometry and shortcuts. 1 hour."),
        ("16:30", "Final Model Test 01 (CSE 971). Attempt. 90 minutes."),
        ("19:00", "Review model test mistakes. 1 hour."),
        ("20:00", "Soft pass over weak CS topics. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 4
    "2025-10-04": [
        ("05:30", "DBMS: transactions, concurrency, indexing, B+ trees. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Software Engineering: SDLC, testing, COCOMO. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "English grammar: articles, prepositions, transformations. 2 hours."),
        ("15:30", "Bangla grammar: samas, sandhi, alankar. 1 hour."),
        ("16:30", "Final Model Test 01 (ICT 281). Attempt. 90 minutes."),
        ("19:00", "Review model test mistakes. 1 hour."),
        ("20:00", "Quick recall: grammar rules. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 5
    "2025-10-05": [
        ("05:30", "Compiler & TOC: lexical, syntax, semantic analysis. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Compiler: code gen, optimization; automata basics. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "International Affairs: UN, Nobel, geopolitics. 2 hours."),
        ("15:30", "English vocab: high-frequency academic words. 1 hour."),
        ("16:30", "Final Model Test 02 (CSE 971). Attempt. 90 minutes."),
        ("19:00", "Review mistakes + flashcards. 1 hour."),
        ("20:00", "Focused fix on weak areas. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 6
    "2025-10-06": [
        ("05:30", "Numerical Analysis: Gauss elimination, interpolation. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Numerical Analysis: differentiation, integration, Newton–Raphson. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "General mix: Bangla literature quick pass; English grammar drills. 2 hours."),
        ("15:30", "Mental ability mixed sets. 1 hour."),
        ("16:30", "Final Model Test 02 (ICT 281). Attempt. 90 minutes."),
        ("19:00", "Review mistakes. 1 hour."),
        ("20:00", "Formula sheet consolidation. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 7
    "2025-10-07": [
        ("05:30", "Data Communication: OSI, TCP/IP, encoding, modulation. 75 minutes."),
        ("07:00", "Gym and commute. 2 hours."),
        ("09:15", "Networking: IP, routing, TCP/UDP, security, DNS/HTTP. 2 hours."),
        ("11:15", "Coding or system design. 1 hour."),
        ("13:00", "Bangladesh & International Affairs: current events. 2 hours."),
        ("15:30", "Bangla grammar and English vocab quick drills. 1 hour."),
        ("16:30", "Final Model Test 03 (CSE 971). Attempt. 90 minutes."),
        ("19:00", "Review mistakes. 1 hour."),
        ("20:00", "Light recap of tough CS topics. 1 hour."),
        ("21:30", "Wind down. 30 minutes."),
    ],

    # Oct 8
    "2025-10-08": [
        ("05:30", "CS rapid-fire: DS, algorithms, OS, DBMS, microprocessor, networking. 2 hours."),
        ("07:30", "Short walk, calm prep. 30 minutes."),
        ("09:15", "CS rapid-fire continues. 2 hours."),
        ("11:15", "Coding pause: light note tidying. 1 hour."),
        ("13:00", "General subjects quick recall: grammar, math formulas, affairs headlines. 2 hours."),
        ("16:30", "Final Model Test 03 (ICT 281). Attempt. 90 minutes."),
        ("19:00", "Cheat sheet pass. Confidence build. 1 hour."),
        ("20:00", "Early wind down and sleep prep. 1 hour."),
    ],
}

# --------- TTS + PLAYBACK ---------
def msg_to_filename(msg: str) -> str:
    digest = hashlib.sha1(msg.encode("utf-8")).hexdigest()[:12]
    return os.path.join(AUDIO_DIR, f"{digest}.mp3")

def synthesize(msg: str) -> str:
    path = msg_to_filename(msg)
    if not os.path.exists(path):
        # gTTS supports 'bn' for Bangla and 'en' for English.
        # Auto-detect: Bangla if any Bengali characters present, else English.
        lang = "bn" if any("\u0980" <= ch <= "\u09FF" for ch in msg) else "en"
        gTTS(text=msg, lang=lang, slow=True).save(path)
    return path

def play_audio(path: str):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    sound = pygame.mixer.Sound(path)
    sound.play()
    # Wait for playback to finish
    while pygame.mixer.get_busy():
        time.sleep(0.1)

# --------- SCHEDULE LOGIC ---------
def get_today_key(now: datetime) -> str:
    return now.strftime("%Y-%m-%d")

def get_current_block(now: datetime):
    day_key = get_today_key(now)
    blocks = PLAN.get(day_key, [])
    # Find the last block whose start time <= current time
    current_minutes = now.hour * 60 + now.minute
    last_block = None
    for hhmm, msg in blocks:
        h, m = map(int, hhmm.split(":"))
        if h * 60 + m <= current_minutes:
            last_block = (hhmm, msg)
        else:
            break
    return last_block

def make_spoken_message(hhmm: str, msg: str) -> str:
    # Compose a gentle voice line
    return f"{GENTLE_PREFIX}{hhmm}. {msg}{GENTLE_SUFFIX}"

def main_loop():
    print("Voice notifier started. Timezone: Asia/Dhaka.")
    current_day = None
    notified_times = set()

    while True:
        now = datetime.now(TZ)
        day_key = get_today_key(now)

        # New day: reset
        if current_day != day_key:
            current_day = day_key
            notified_times.clear()
            blocks = PLAN.get(day_key, [])
            print(f"\nNew day: {current_day} — {len(blocks)} blocks loaded:")
            for t, _ in blocks:
                print(f"  - {t}")

        # If no plan for today, idle gently
        blocks = PLAN.get(day_key, [])
        if not blocks:
            time.sleep(5)
            continue

        # Check each block; trigger if now >= scheduled time and not fired yet
        for hhmm, msg in blocks:
            if hhmm in notified_times:
                continue

            # Parse scheduled time for today
            h, m = map(int, hhmm.split(":"))
            scheduled = now.replace(hour=h, minute=m, second=0, microsecond=0)

            # If we started late or we're exactly on/after the scheduled minute, fire
            if now >= scheduled:
                spoken = make_spoken_message(hhmm, msg)
                audio_path = synthesize(spoken)
                print(f"[{now.strftime('%H:%M:%S')}] Triggering: {hhmm} -> {msg}")
                play_audio(audio_path)
                notified_times.add(hhmm)

        # Sleep briefly; 5s makes it responsive without busy-waiting
        time.sleep(5)
  # check every 20 seconds


if __name__ == "__main__":
    main_loop()
