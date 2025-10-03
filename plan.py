# plan.py
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

# 16-hour daily blocks from 06:00–21:00 to cover everything before morning of Oct 9
PLAN = {
    # Oct 3 — Core CS foundations
    "2025-10-04": [
        ("06:00", f"CS — Algorithm: {topics(syllabus_cse, 'Algorithm', slice(0,3))}"),
        ("07:00", f"CS — Algorithm: {topics(syllabus_cse, 'Algorithm', slice(3,6))}"),
        ("08:00", f"CS — Data Structures: {topics(syllabus_cse, 'Data Structures', slice(0,3))}"),
        ("09:00", f"CS — Data Structures: {topics(syllabus_cse, 'Data Structures', slice(3,6))}"),
        ("10:00", f"CS — Operating System: {topics(syllabus_cse, 'Operating System', slice(0,3))}"),
        ("11:00", f"CS — Operating System: {topics(syllabus_cse, 'Operating System', slice(3,6))}"),
        ("12:00", f"CS — DBMS: {topics(syllabus_cse, 'Database Management System', slice(0,4))}"),
        ("13:00", f"CS — DBMS: {topics(syllabus_cse, 'Database Management System', slice(4,8))}"),
        ("14:00", f"General — English language: {topics(syllabus_general, 'English', 0)}"),
        ("15:00", f"General — English clauses/transformations: {topics(syllabus_general, 'English', 2)}"),
        ("16:00", f"General — বাংলা ভাষা/ব্যাকরণ: {topics(syllabus_general, 'বাংলা', 0)}"),
        ("17:00", f"General — বাংলা সাহিত্য: {topics(syllabus_general, 'বাংলা', 1)}"),
        ("18:00", f"General — বাংলাদেশ বিষয়াবলি: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(0,3))}"),
        ("19:00", f"General — আন্তর্জাতিক বিষয়াবলি: {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', slice(0,3))}"),
        ("20:00", f"General — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', slice(0,2))}"),
        ("21:00", f"General — মানসিক দক্ষতা: {topics(syllabus_general, 'মানসিক দক্ষতা', slice(0,3))}"),
    ],

    # Oct 4 — Microprocessor, COA, Compiler, Discrete, Numerical
    "2025-10-05": [
        ("06:00", f"CS — Microprocessor: {topics(syllabus_cse, 'Microprocessor and Interfacing', slice(0,4))}"),
        ("07:00", f"CS — Microprocessor: {topics(syllabus_cse, 'Microprocessor and Interfacing', slice(4,8))}"),
        ("08:00", f"CS — Microprocessor: {topics(syllabus_cse, 'Microprocessor and Interfacing', slice(8,12))}"),
        ("09:00", f"CS — Computer Organization & Architecture: {topics(syllabus_cse, 'Computer Organization and Architecture', slice(0,4))}"),
        ("10:00", f"CS — Computer Organization & Architecture: {topics(syllabus_cse, 'Computer Organization and Architecture', slice(4,7))}"),
        ("11:00", f"CS — Compiler & TOC: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(0,3))}"),
        ("12:00", f"CS — Compiler details: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(3,6))}"),
        ("13:00", f"CS — Discrete Mathematics: {topics(syllabus_cse, 'Discrete Mathematics', slice(0,4))}"),
        ("14:00", f"CS — Discrete Mathematics: {topics(syllabus_cse, 'Discrete Mathematics', slice(4,8))}"),
        ("15:00", f"CS — Numerical Analysis: {topics(syllabus_cse, 'Numerical Analysis', slice(0,3))}"),
        ("16:00", f"CS — Numerical Analysis: {topics(syllabus_cse, 'Numerical Analysis', slice(3,6))}"),
        ("17:00", f"General — English idioms/phrases: {topics(syllabus_general, 'English', 1)}"),
        ("18:00", f"General — English corrections: {topics(syllabus_general, 'English', 3)}"),
        ("19:00", f"General — বাংলাদেশ অর্থনীতি/শিল্প: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(3,5))}"),
        ("20:00", f"General — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', slice(2,4))}"),
        ("21:00", f"General — মানসিক দক্ষতা: {topics(syllabus_general, 'মানসিক দক্ষতা', slice(3,6))}"),
    ],

    # Oct 5 — Networking, Data Communication, AI, Programming, Digital Systems
    "2025-10-06": [
        ("06:00", f"CS — Computer Network: {topics(syllabus_cse, 'Computer Network and the Internet', slice(0,4))}"),
        ("07:00", f"CS — Computer Network: {topics(syllabus_cse, 'Computer Network and the Internet', slice(4,8))}"),
        ("08:00", f"CS — Data Communication: {topics(syllabus_cse, 'Data Communication', slice(0,5))}"),
        ("09:00", f"CS — Data Communication: {topics(syllabus_cse, 'Data Communication', slice(5,10))}"),
        ("10:00", f"CS — Artificial Intelligence: {topics(syllabus_cse, 'Artificial Intelligence', slice(0,5))}"),
        ("11:00", f"CS — Artificial Intelligence: {topics(syllabus_cse, 'Artificial Intelligence', slice(5,10))}"),
        ("12:00", f"CS — Programming (C/C++/Java/OOP): {topics(syllabus_cse, 'Computer Programming', slice(0,6))}"),
        ("13:00", f"CS — Programming deep dive: {topics(syllabus_cse, 'Computer Programming', slice(6,12))}"),
        ("14:00", f"CS — Digital System: {topics(syllabus_cse, 'Digital System', slice(0,5))}"),
        ("15:00", f"CS — Digital System: {topics(syllabus_cse, 'Digital System', slice(5,11))}"),
        ("16:00", f"CS — Digital System devices: {topics(syllabus_cse, 'Digital System', slice(11,14))}"),
        ("17:00", f"General — English sentences/transformations: {topics(syllabus_general, 'English', 2)}"),
        ("18:00", f"General — English words (syn/ant/prefix/suffix): {topics(syllabus_general, 'English', 5)}"),
        ("19:00", f"General — বাংলাদেশ সংবিধান/রাজনীতি/সরকার: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(5,8))}"),
        ("20:00", f"General — আন্তর্জাতিক প্রতিষ্ঠান/নিরাপত্তা: {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', slice(3,5))}"),
        ("21:00", f"General — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', slice(4,5))}"),
    ],

    # Oct 6 — Software Engineering + General drill
    "2025-10-07": [
        ("06:00", f"CS — Software Engineering: {topics(syllabus_cse, 'Software Engineering', slice(0,4))}"),
        ("07:00", f"CS — Software Engineering: {topics(syllabus_cse, 'Software Engineering', slice(4,8))}"),
        ("08:00", f"CS — Software Engineering QA/Reliability: {topics(syllabus_cse, 'Software Engineering', slice(8,13))}"),
        ("09:00", f"CS — OS revisions: {topics(syllabus_cse, 'Operating System', slice(6,10))}"),
        ("10:00", f"CS — DBMS practice: {topics(syllabus_cse, 'Database Management System', slice(8,10))}"),
        ("11:00", f"CS — Compiler practice: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(0,6))}"),
        ("12:00", f"General — English quick pass: {topics(syllabus_general, 'English', slice(0,3))}"),
        ("13:00", f"General — English composition: {topics(syllabus_general, 'English', 6)}"),
        ("14:00", f"General — বাংলা ভাষা/সাহিত্য সমন্বিত পুনরাবৃত্তি: {topics(syllabus_general, 'বাংলা', slice(0,2))}"),
        ("15:00", f"General — বাংলাদেশ: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(0,9))}"),
        ("16:00", f"General — আন্তর্জাতিক: {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', slice(0,6))}"),
        ("17:00", f"General — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', slice(0,5))}"),
        ("18:00", f"General — মানসিক দক্ষতা ফোকাস: {topics(syllabus_general, 'মানসিক দক্ষতা', slice(0,6))}"),
        ("19:00", "Formula sheet consolidation (NA, OS, DBMS, µP)"),
        ("20:00", "Weak spot drills (CS)"),
        ("21:00", "Light recap and wind down"),
    ],

    # Oct 7 — Mixed CS revision + General polish
    "2025-10-08": [
        ("06:00", f"CS — Algorithms mixed set: {topics(syllabus_cse, 'Algorithm', slice(0,8))}"),
        ("07:00", f"CS — Data Structures mixed set: {topics(syllabus_cse, 'Data Structures', slice(0,11))}"),
        ("08:00", f"CS — Networking mixed set: {topics(syllabus_cse, 'Computer Network and the Internet', slice(0,12))}"),
        ("09:00", f"CS — Data Communication mixed set: {topics(syllabus_cse, 'Data Communication', slice(0,12))}"),
        ("10:00", f"CS — Microprocessor mixed set: {topics(syllabus_cse, 'Microprocessor and Interfacing', slice(0,12))}"),
        ("11:00", f"CS — COA mixed set: {topics(syllabus_cse, 'Computer Organization and Architecture', slice(0,8))}"),
        ("12:00", f"CS — Compiler & TOC refresh: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(0,6))}"),
        ("13:00", f"CS — AI refresh: {topics(syllabus_cse, 'Artificial Intelligence', slice(0,10))}"),
        ("14:00", f"General — English polish: {topics(syllabus_general, 'English', slice(0,6))}"),
        ("15:00", f"General — বাংলা polish: {topics(syllabus_general, 'বাংলা', slice(0,2))}"),
        ("16:00", f"General — বাংলাদেশ quick pass: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(0,9))}"),
        ("17:00", f"General — আন্তর্জাতিক quick pass: {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', slice(0,6))}"),
        ("18:00", f"General — গাণিতিক যুক্তি mixed: {topics(syllabus_general, 'গাণিতিক যুক্তি', slice(0,5))}"),
        ("19:00", f"General — মানসিক দক্ষতা mixed: {topics(syllabus_general, 'মানসিক দক্ষতা', slice(0,6))}"),
        ("20:00", "Cheat sheet pass (CS + General)"),
        ("21:00", "Wind down"),
    ],

    # Oct 8 — Final structured revision (no heavy new topics)
    "2025-10-09": [
        ("06:00", f"CS rapid-fire — Data Structures: {topics(syllabus_cse, 'Data Structures', slice(0,6))}"),
        ("07:00", f"CS rapid-fire — Algorithms: {topics(syllabus_cse, 'Algorithm', slice(0,6))}"),
        ("08:00", f"CS rapid-fire — OS & DBMS: {topics(syllabus_cse, 'Operating System', slice(0,6))}; {topics(syllabus_cse, 'Database Management System', slice(0,6))}"),
        ("09:00", f"CS rapid-fire — Microprocessor & COA: {topics(syllabus_cse, 'Microprocessor and Interfacing', slice(0,8))}; {topics(syllabus_cse, 'Computer Organization and Architecture', slice(0,6))}"),
        ("10:00", f"CS rapid-fire — Networking & DataComm: {topics(syllabus_cse, 'Computer Network and the Internet', slice(0,10))}; {topics(syllabus_cse, 'Data Communication', slice(0,10))}"),
        ("11:00", f"CS rapid-fire — Compiler/TOC & AI: {topics(syllabus_cse, 'Compiler and Theory of Computation', slice(0,6))}; {topics(syllabus_cse, 'Artificial Intelligence', slice(0,8))}"),
        ("12:00", f"General pass — English: {topics(syllabus_general, 'English', slice(0,6))}"),
        ("13:00", f"General pass — বাংলা: {topics(syllabus_general, 'বাংলা', slice(0,2))}"),
        ("14:00", f"General pass — বাংলাদেশ: {topics(syllabus_general, 'বাংলাদেশ বিষয়াবলি', slice(0,9))}"),
        ("15:00", f"General pass — আন্তর্জাতিক: {topics(syllabus_general, 'আন্তর্জাতিক বিষয়াবলি', slice(0,6))}"),
        ("16:00", f"General pass — গাণিতিক যুক্তি: {topics(syllabus_general, 'গাণিতিক যুক্তি', slice(0,5))}"),
        ("17:00", f"General pass — মানসিক দক্ষতা: {topics(syllabus_general, 'মানসিক দক্ষতা', slice(0,6))}"),
        ("18:00", "Light walk, hydration, calm breathing"),
        ("19:00", "Cheat sheet glance (only key formulas/rules)"),
        ("20:00", "Pack essentials; early wind down"),
        ("21:00", "Sleep prep; no screens"),
    ],

    # Oct 9 — Morning wrap (final recall only)
    "2025-10-10": [
        ("06:00", "Final recall — top 20 CS formulas/concepts"),
        ("07:00", "Final recall — General quick hits (Bangla/English/Math)"),
        ("08:00", "Center logistics & documents check"),
        ("09:00", "Hydration, calm mind, no new learning"),
        ("10:00", f"Arrive at center; reporting window (planned {EXAM_REPORTING})"),
    ],
}
