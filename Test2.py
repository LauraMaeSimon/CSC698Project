"""
Incident Recorder v1.0
---------------------------------
• Choose a teacher (pulled from teachers.csv)
• Choose/enter a student (pulled from laura_students.csv, auto-creates file)
• Pick one of 5 common behaviours (good + bad)
• Optional notes box
• Click Submit → incident saved with timestamp to incidents.csv
• Bottom of the window always shows the two most-recent incidents
Everything is stored under  ~/Documents/TeachersData/
"""

from pathlib import Path
import csv, os, datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ── 1.  DATA LOCATIONS ─────────────────────────────────────────────────────────
DATA_DIR = Path.home() / "Documents" / "TeachersData"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TEACHERS_CSV = DATA_DIR / "teachers.csv"
STUDENTS_CSV = DATA_DIR / "laura_students.csv"
INCIDENTS_CSV = DATA_DIR / "incidents.csv"

# ── 2.  HELPER FUNCTIONS ───────────────────────────────────────────────────────
def read_column(csv_path):
    """Return first-column entries from a CSV, or [] if file missing/empty."""
    if csv_path.exists():
        with open(csv_path, newline="") as f:
            return [row[0] for row in csv.reader(f) if row]
    return []

def append_row(csv_path, row):
    """Append one row (iterable) to a CSV, creating the file if needed."""
    new_file = not csv_path.exists()
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:                      # add header on very first write
            w.writerow(["timestamp", "teacher", "student", "behaviour", "notes"])
        w.writerow(row)

def load_recent_incidents(n=2):
    """Return last *n* incidents as list of strings (most recent first)."""
    if not INCIDENTS_CSV.exists():
        return []
    with open(INCIDENTS_CSV, newline="") as f:
        rows = list(csv.reader(f))
        header, data = rows[0], rows[1:]
    latest = data[-n:][::-1]             # last n, reversed
    return [
        f"{r[0][:16]} | {r[2]} | {r[3]} | {r[4]}"
        for r in latest
    ]

# ── 3.  INITIAL LOADS ──────────────────────────────────────────────────────────
teacher_list  = read_column(TEACHERS_CSV)
student_list  = read_column(STUDENTS_CSV)
behaviours    = [
    "On-Task / Participating",
    "Prepared & Helping Others",
    "Excellent Effort",
    "Off-Task / Distracted",
    "Disruptive / Calling Out"
]

# ── 4.  GUI  ────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Classroom Incident Recorder")

# --- Teacher ------------------------------------------------------------------
tk.Label(root, text="Teacher:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
teacher_var = tk.StringVar()
teacher_cb  = ttk.Combobox(root, textvariable=teacher_var, values=teacher_list,
                           width=28, state="normal")
teacher_cb.grid(row=0, column=1, columnspan=2, sticky="we", padx=6, pady=6)

# --- Student ------------------------------------------------------------------
tk.Label(root, text="Student:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
student_var = tk.StringVar()
student_cb  = ttk.Combobox(root, textvariable=student_var, values=student_list,
                           width=28, state="normal")
student_cb.grid(row=1, column=1, columnspan=2, sticky="we", padx=6, pady=6)

# --- Behaviour ----------------------------------------------------------------
tk.Label(root, text="Behaviour:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
behaviour_var = tk.StringVar()
behaviour_cb  = ttk.Combobox(root, textvariable=behaviour_var, values=behaviours,
                             width=28, state="readonly")
behaviour_cb.grid(row=2, column=1, columnspan=2, sticky="we", padx=6, pady=6)

# --- Notes --------------------------------------------------------------------
tk.Label(root, text="Notes:").grid(row=3, column=0, sticky="ne", padx=6, pady=6)
notes_txt = tk.Text(root, height=3, width=30)
notes_txt.grid(row=3, column=1, columnspan=2, sticky="we", padx=6, pady=6)

# --- Status / recent incidents ------------------------------------------------
tk.Label(root, text="Most-recent two incidents:").grid(row=5, column=0,
                                                       columnspan=3, sticky="w",
                                                       padx=6, pady=(12,0))
recent_var = tk.StringVar()
recent_lbl = tk.Label(root, textvariable=recent_var, justify="left",
                      anchor="w", bg="#f1f1f1", relief="sunken")
recent_lbl.grid(row=6, column=0, columnspan=3, sticky="we", padx=6, pady=(0,12))

def refresh_recent():
    lines = load_recent_incidents(2)
    recent_var.set("\n".join(lines) if lines else "— no incidents yet —")

refresh_recent()

# --- Submit -------------------------------------------------------------------
def submit():
    teacher   = teacher_var.get().strip()
    student   = student_var.get().strip()
    behaviour = behaviour_var.get().strip()
    notes     = notes_txt.get("1.0", "end").strip()

    # basic validation
    if not teacher or not student or not behaviour:
        messagebox.showwarning("Missing info",
                               "Teacher, student, and behaviour are required.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1️⃣  save incident
    append_row(INCIDENTS_CSV, [timestamp, teacher, student, behaviour, notes])

    # 2️⃣  extend student list if new
    if student not in student_list:
        student_list.append(student)
        append_row(STUDENTS_CSV, [student])        # 1-column CSV
        student_cb["values"] = student_list

    # 3️⃣  clear note box & behaviour
    behaviour_var.set("")
    notes_txt.delete("1.0", "end")

    # 4️⃣  update recent display
    refresh_recent()

    # 5️⃣  feedback
    messagebox.showinfo("Recorded", f"Incident recorded for {student}.")

submit_btn = ttk.Button(root, text="Submit Incident", command=submit)
submit_btn.grid(row=4, column=0, columnspan=3, pady=8)

# make columns stretch
root.grid_columnconfigure(1, weight=1)
root.mainloop()
