from syl_cse import syllabus_cse
from syl_gen import syllabus_general

# Helper to render subtopics from a syllabus dict
def topics(syl: dict, subject: str, indices):
    items = syl[subject]["subtopics"]
    if isinstance(indices, slice):
        picked = items[indices]
    elif isinstance(indices, (list, tuple)):
        picked = [items[i] for i in indices]
    else:
        picked = [items[indices]]
    return "; ".join(picked)

# If your exam time differs, update these:
EXAM_REPORTING = "08:30"      # Reporting window (confirm on admit card)
EXAM_START = "10:00"          # Exam start (placeholder)
EXAM_END = "12:00"            # Exam end (placeholder)

PLAN = {
    # Oct 1 — starts 02:30 today
    "2025-10-01": [
        ("02:30", "Monaarch work sprint until 04:30"),
        ("04:35", "Calisthenics: pull-ups, forward/back bend, side twist"),
        ("04:50", "Light bath"),
        ("05:30", f"CS — Data Structures: {topics(syllabus_cse, 'Data Structures', slice(0,3))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — Algorithm: {topics(syllabus_cse, 'Algorithm', slice(0,2))}"),
        ("11:15", "Coding/system design (1h)"),
        ("13:00", f"General — বাংলাদেশ বিষয়াবলি: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', 6)}"),
        ("15:30", f"General — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', 1)}"),
        ("16:30", f"CS — Numerical Analysis MCQ: {topics(syllabus_cse, 'Numerical Analysis', 0)}"),
        ("19:00", "Quick recall — core math formulas"),
        ("20:00", f"CS — Numerical Analysis review: {topics(syllabus_cse, 'Numerical Analysis', 2)}"),
        ("21:30", "Wind down, set priorities for tomorrow"),
    ],

    # Oct 2
    "2025-10-02": [
        ("05:30", f"CS — Microprocessor: {topics(syllabus_cse, 'Microprocessor and Interfacing', slice(3,6))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — Operating System: {topics(syllabus_cse, 'Operating System', slice(1,4))}"),
        ("11:15", "Coding/system design (1h)"),
        ("13:00", f"General — English literature: {topics(syllabus_general, 'English', -1)}"),
        ("15:30", f"General — মানসিক দক্ষতা: {topics(syllabus_general, 'মানসিক দক্ষতা', 1)}"),
        ("16:30", f"CS — Compiler & TOC MCQ: {topics(syllabus_cse, 'Compiler and Theory of Computation', 0)}"),
        ("19:00", f"General — English grammar: {topics(syllabus_general, 'English', 3)}"),
        ("20:00", f"CS — Compiler pass: {topics(syllabus_cse, 'Compiler and Theory of Computation', 3)}"),
        ("21:30", "Wind down"),
    ],

    # Oct 3
    "2025-10-03": [
        ("05:30", f"CS — Operating System: {topics(syllabus_cse, 'Operating System', slice(4,6))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — DBMS: {topics(syllabus_cse, 'Database Management System', slice(1,4))}"),
        ("11:15", "Coding/system design (1h)"),
        ("13:00", f"General — বাংলাদেশ বিষয়াবলি: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', 3)}"),
        ("15:30", f"General — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', 3)}"),
        ("16:30", "Final Model Test 01 (CSE 971)"),
        ("19:00", "Review model test mistakes"),
        ("20:00", "Soft pass over weak CS topics"),
        ("21:30", "Wind down"),
    ],

    # Oct 4
    "2025-10-04": [
        ("05:30", f"CS — DBMS: {topics(syllabus_cse, 'Database Management System', slice(5,7))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — Software Engineering: {topics(syllabus_cse, 'Software Engineering', slice(0,3))}"),
        ("11:15", "Coding/system design (1h)"),
        ("13:00", f"General — English grammar: {topics(syllabus_general, 'English', 4)}"),
        ("15:30", f"General — বাংলা ভাষা/ব্যাকরণ: {topics(syllabus_general, 'বাংলা', 0)}"),
        ("16:30", "Final Model Test 01 (ICT 281)"),
        ("19:00", "Review mistakes"),
        ("20:00", "Quick recall: grammar rules"),
        ("21:30", "Wind down"),
    ],

    # Oct 5
    "2025-10-05": [
        ("05:30", f"CS — Compiler & TOC: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(0,3))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — Compiler: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(3,5))}"),
        ("11:15", "Coding/system design (1h)"),
        ("13:00", f"General — আন্তর্জাতিক বিষয়াবলি: {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', slice(0,3))}"),
        ("15:30", "General — English vocabulary (HF words, transformations)"),
        ("16:30", "Final Model Test 02 (CSE 971)"),
        ("19:00", "Review mistakes and refresh flashcards"),
        ("20:00", "Fix weak CS areas (targeted drills)"),
        ("21:30", "Wind down"),
    ],

    # Oct 6
    "2025-10-06": [
        ("05:30", f"CS — Numerical Analysis: {topics(syllabus_cse, 'Numerical Analysis', slice(0,2))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — Numerical Analysis: {topics(syllabus_cse, 'Numerical Analysis', slice(2,4))}"),
        ("11:15", "Coding/system design (1h)"),
        ("13:00", f"General — বাংলা ও English quick revision: {topics(syllabus_general, 'বাংলা', 1)}; {topics(syllabus_general, 'English', slice(0,2))}"),
        ("15:30", f"General — মানসিক দক্ষতা: mixed sets ({topics(syllabus_general, 'মানসিক দক্ষতা', slice(0,6))})"),
        ("16:30", "Final Model Test 02 (ICT 281)"),
        ("19:00", "Review mistakes thoroughly"),
        ("20:00", "Formula sheet consolidation (math, NA, OS)"),
        ("21:30", "Wind down"),
    ],

    # Oct 7
    "2025-10-07": [
        ("05:30", f"CS — Data Communication: {topics(syllabus_cse, 'Data Communication', slice(0,4))}"),
        ("07:00", "Gym and commute"),
        ("09:15", f"CS — Networking: {topics(syllabus_cse, 'Computer Network and the Internet', slice(0,5))}"),
        ("11:15", "Coding/system design (light)"),
        ("13:00", f"General — বাংলাদেশ/আন্তর্জাতিক: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(8,9))}; {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', 2)}"),
        ("15:30", "General — Bangla grammar + English vocab quick drills"),
        ("16:30", "Final Model Test 03 (CSE 971)"),
        ("19:00", "Review mistakes"),
        ("20:00", "Light recap of tough CS topics (OS/DBMS/µP)"),
        ("21:30", "Wind down"),
    ],

    # Oct 8 — Exam day (confirm timings with admit card)
    "2025-10-08": [
        ("05:30", f"CS rapid-fire: {topics(syllabus_cse, 'Data Structures', slice(0,5))}; {topics(syllabus_cse, 'Algorithm', slice(0,4))}"),
        ("07:30", "Short walk, calm prep, hydration"),
        ("08:30", f"Arrive at center; reporting window begins (planned {EXAM_REPORTING})"),
        ("10:00", f"BCS Special Preli — Exam start (planned {EXAM_START})"),
        ("12:00", f"Exam end (planned {EXAM_END})"),
        ("13:30", "Decompress; light meal; brief reflection (no post-mortem yet)"),
        ("16:30", "If ICT paper later in day, quick grammar/math scan; else rest"),
        ("19:00", "Cheat sheet pass (only if next paper remains)"),
        ("20:00", "Early wind down and sleep prep"),
    ],
}
