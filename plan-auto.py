# plan.py
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import math

from general import syllabus_49_bcs_special_2025 as GENERAL
from cse import computer_science_syllabus_49_bcs_special_2025 as CSE

TZ = ZoneInfo("Asia/Dhaka")

ALL_SYLLABUS = {
    "General": GENERAL,
    "CSE": CSE
}

def flatten_syllabus():
    """Flatten syllabus dict into (subject, topic) pairs."""
    tasks = []
    for section, content in ALL_SYLLABUS.items():
        for subject, details in content.items():
            if isinstance(details, dict):
                # Part-based subjects
                for part, sub in details.items():
                    if isinstance(sub, dict) and "Topics" in sub:
                        for topic in sub["Topics"]:
                            tasks.append((subject, topic))
                    elif isinstance(sub, dict):
                        for subtopic, items in sub.items():
                            if isinstance(items, list):
                                for t in items:
                                    tasks.append((subject, f"{subtopic}: {t}"))
            elif isinstance(details, list):
                for t in details:
                    tasks.append((subject, t))
    return tasks

def generate_plan(start_date, end_date, hours_per_day=16):
    tasks = flatten_syllabus()
    total_days = (end_date - start_date).days
    total_blocks = total_days * hours_per_day
    chunk_size = max(1, math.ceil(len(tasks) / total_blocks))

    PLAN = {}
    current = start_date
    idx = 0
    while current < end_date:
        blocks = []
        for h in range(6, 22):  # 6 AM – 10 PM
            if idx >= len(tasks):
                break
            subject, topic = tasks[idx]
            blocks.append((f"{h:02d}:00", f"{subject} — {topic}"))
            idx += chunk_size
        PLAN[current.strftime("%Y-%m-%d")] = blocks
        current += timedelta(days=1)
    return PLAN

# Generate plan until morning of 9th Oct
PLAN = generate_plan(
    start_date=datetime(2025, 10, 3, tzinfo=TZ),
    end_date=datetime(2025, 10, 9, tzinfo=TZ)
)

