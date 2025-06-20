# import tkinter as tk
# from tkinter import ttk, messagebox #This is for the teacher dropdown box
# import csv
# import os
#
# # 1. Create the main window (“root”)
# root = tk.Tk()
# root.title("Teacher Form")
#
# # 2. Put a label that says “Teacher:”
# label_teacher = tk.Label(root, text="Teacher:")
# label_teacher.grid(row=0, column=0, padx=10, pady=10, sticky="e")  # right-align in its cell
#
# # 3. Place an entry widget so the user can type the teacher’s name
# entry_teacher = tk.Entry(root, width=30)
# entry_teacher.grid(row=0, column=1, padx=10, pady=10)
#
# # 4. Start the GUI event loop
# root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

CSV_FILE = "teachers.csv"

def load_previous():
    """Read existing names from the CSV file (if it exists)."""
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="") as f:
            reader = csv.reader(f)
            return [row[0] for row in reader if row]   # one name per row
    return []

def save_name():
    name = teacher_var.get().strip()
    if not name:
        messagebox.showwarning("Missing name", "Please enter or select a teacher name.")
        return

    # 1️⃣  append to list-box
    teacher_listbox.insert(tk.END, name)

    # 2️⃣  append to CSV
    with open(CSV_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name])

    # 3️⃣  clear entry / combobox
    teacher_var.set("")

    # 4️⃣  little confirmation (optional)
    status_var.set(f"Saved: {name}")

# ---------- GUI ---------- #
root = tk.Tk()
root.title("Teacher Recorder")

# ―― input ―― #
teacher_var = tk.StringVar()
teacher_label = tk.Label(root, text="Teacher:")
teacher_label.grid(row=0, column=0, padx=8, pady=8, sticky="e")

# If you’d rather have a free-text Entry, swap ttk.Combobox for tk.Entry
teacher_combo = ttk.Combobox(root, textvariable=teacher_var, width=30)
teacher_combo.grid(row=0, column=1, padx=8, pady=8)
teacher_combo["values"] = sorted(set(load_previous()))  # preload known names
teacher_combo["state"] = "normal"  # allow typing new names

save_btn = ttk.Button(root, text="Save", command=save_name)
save_btn.grid(row=0, column=2, padx=8, pady=8)

# ―― saved list ―― #
tk.Label(root, text="Recorded teachers:").grid(row=1, column=0, columnspan=3, sticky="w", padx=8)
frame = tk.Frame(root)
frame.grid(row=2, column=0, columnspan=3, padx=8, pady=(0,8), sticky="nsew")

teacher_listbox = tk.Listbox(frame, height=8, width=45)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=teacher_listbox.yview)
teacher_listbox.configure(yscrollcommand=scrollbar.set)
teacher_listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# populate listbox with previous names
for n in load_previous():
    teacher_listbox.insert(tk.END, n)

# ―― status bar ―― #
status_var = tk.StringVar()
tk.Label(root, textvariable=status_var, anchor="w").grid(row=3, column=0, columnspan=3, sticky="we", padx=8, pady=(0,8))

# make the listbox stretch if window is resized
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

