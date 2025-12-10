# main.py
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

from utils import ensure_dirs, now_str, CALC_LOG
from calculator import Calculator
from notes_manager import NotesManager
from timer import TimerStopwatch
from file_organizer import FileOrganizer
from unit_converter import UnitConverter
from backup_manager import BackupManager

APP_NAME = "Personal Productivity Suite"

class PPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        ensure_dirs()
        self.title(APP_NAME)
        self.geometry("900x600")
        self.minsize(800, 500)
        try:
            ttk.Style(self).theme_use("clam")
        except Exception:
            pass
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=16, pady=12)
        ttk.Label(header, text=APP_NAME, font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Label(header, text=now_str(), font=("Segoe UI", 10)).pack(side="right")

        cards = ttk.Frame(self)
        cards.pack(fill="both", expand=True, padx=20, pady=10)

        card_specs = [
            ("Calculator", self.open_calculator, "Quick math & history"),
            ("Notes", self.open_notes_manager, "Write & manage notes"),
            ("Timer", self.open_timer, "Stopwatch & countdown"),
            ("File Organizer", self.open_file_organizer, "Sort files by type"),
            ("Unit Converter", self.open_unit_converter, "Convert units"),
            ("Backup & Restore", self.open_backup_manager, "Create & restore backups"),
        ]

        cols = 3
        for idx, (title, cmd, desc) in enumerate(card_specs):
            r = idx // cols
            c = idx % cols
            card = ttk.Frame(cards, relief="raised", borderwidth=2)
            card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
            cards.grid_rowconfigure(r, weight=1)
            cards.grid_columnconfigure(c, weight=1)
            ttk.Label(card, text=title, font=("Segoe UI", 12, "bold")).pack(padx=12, pady=(12,6))
            ttk.Label(card, text=desc, wraplength=200).pack(padx=12, pady=(0,12))
            ttk.Button(card, text="Open", command=cmd).pack(pady=(0,12))

    # ----------------- Tools windows -----------------
    def open_calculator(self):
        win = tk.Toplevel(self)
        win.title("Calculator")
        win.geometry("400x300")
        calc = Calculator()

        ttk.Label(win, text="Enter expression:").pack(padx=10, pady=(12,4), anchor="w")
        expr_var = tk.StringVar()
        ttk.Entry(win, textvariable=expr_var).pack(fill="x", padx=10)

        result_var = tk.StringVar()
        ttk.Label(win, textvariable=result_var, font=("Segoe UI", 10, "bold")).pack(padx=10, pady=8)

        def do_eval():
            expr = expr_var.get().strip()
            if not expr:
                return
            try:
                res = calc.evaluate(expr)
                result_var.set(str(res))
            except Exception as e:
                messagebox.showerror("Error", f"Invalid expression:\n{e}")

        ttk.Button(win, text="Compute", command=do_eval).pack(pady=6)
        ttk.Button(win, text="Show Log", command=lambda: self.show_file(CALC_LOG)).pack(pady=6)

    def open_notes_manager(self):
        nm = NotesManager()
        win = tk.Toplevel(self)
        win.title("Notes Manager")
        win.geometry("800x500")

        left = ttk.Frame(win)
        left.pack(side="left", fill="y", padx=8, pady=8)
        right = ttk.Frame(win)
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        search_var = tk.StringVar()
        ttk.Entry(left, textvariable=search_var).pack(padx=6, pady=6)
        ttk.Button(left, text="Search", command=lambda: refresh_list()).pack(padx=6, pady=6)
        ttk.Button(left, text="Add New", command=lambda: add_note()).pack(padx=6, pady=6)
        ttk.Button(left, text="Delete", command=lambda: delete_selected()).pack(padx=6, pady=6)
        ttk.Button(left, text="Export", command=lambda: export_notes()).pack(padx=6, pady=6)

        notes_list = tk.Listbox(left, width=30)
        notes_list.pack(padx=6, pady=6, fill="y", expand=True)

        title_var = tk.StringVar()
        ttk.Label(right, text="Title:").pack(anchor="w")
        title_entry = ttk.Entry(right, textvariable=title_var)
        title_entry.pack(fill="x")
        ttk.Label(right, text="Content:").pack(anchor="w", pady=(8,0))
        content_text = tk.Text(right, wrap="word")
        content_text.pack(fill="both", expand=True)

        def refresh_list():
            notes_list.delete(0, "end")
            q = search_var.get().strip()
            items = nm.find(q) if q else nm.list_notes()
            for n in items:
                notes_list.insert("end", f"{n['id']}: {n['title']}")

        def on_select(evt=None):
            sel = notes_list.curselection()
            if not sel:
                return
            val = notes_list.get(sel[0])
            nid = int(val.split(":",1)[0])
            n = nm.get(nid)
            if n:
                title_var.set(n["title"])
                content_text.delete("1.0", "end")
                content_text.insert("1.0", n["content"])

        notes_list.bind("<<ListboxSelect>>", on_select)

        def add_note():
            t = simpledialog.askstring("Title", "Enter note title:", parent=win)
            if not t:
                return
            c = simpledialog.askstring("Content", "Enter note content:", parent=win)
            nm.add_note(t, c or "")
            refresh_list()

        def delete_selected():
            sel = notes_list.curselection()
            if not sel:
                messagebox.showinfo("Info", "Select a note to delete")
                return
            val = notes_list.get(sel[0])
            nid = int(val.split(":",1)[0])
            if messagebox.askyesno("Confirm", "Delete selected note?"):
                nm.delete(nid)
                title_var.set("")
                content_text.delete("1.0", "end")
                refresh_list()

        def export_notes():
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt"), ("JSON", "*.json"), ("CSV", "*.csv")])
            if not path:
                return
            ext = os.path.splitext(path)[1].lstrip(".") or "txt"
            try:
                nm.export(path, ext)
                messagebox.showinfo("Exported", f"Notes exported to {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

        def save_edit():
            sel = notes_list.curselection()
            if not sel:
                messagebox.showinfo("Info", "Select a note to save")
                return
            val = notes_list.get(sel[0])
            nid = int(val.split(":",1)[0])
            t = title_var.get().strip()
            c = content_text.get("1.0", "end").strip()
            nm.edit(nid, title=t, content=c)
            refresh_list()
            messagebox.showinfo("Saved", "Note updated")

        ttk.Button(right, text="Save", command=save_edit).pack(pady=6)
        refresh_list()

    def open_timer(self):
        win = tk.Toplevel(self)
        win.title("Timer & Stopwatch")
        win.geometry("400x300")

        running = {"state": False, "start": None, "elapsed": 0.0}

        lbl = ttk.Label(win, text="Elapsed: 0.00s", font=("Segoe UI", 12, "bold"))
        lbl.pack(pady=12)

        def update_label():
            if running["state"]:
                nowt = time.time()
                elapsed = running["elapsed"] + (nowt - running["start"])
                lbl.config(text=f"Elapsed: {elapsed:.2f}s")
            win.after(100, update_label)

        def start():
            if not running["state"]:
                running["state"] = True
                running["start"] = time.time()

        def stop():
            if running["state"]:
                running["elapsed"] += time.time() - running["start"]
                running["state"] = False

        def reset():
            running["state"] = False
            running["start"] = None
            running["elapsed"] = 0.0
            lbl.config(text="Elapsed: 0.00s")

        def countdown():
            s = simpledialog.askinteger("Countdown", "Enter seconds:", parent=win, minvalue=1)
            if not s:
                return
            def run(cd):
                for i in range(cd, 0, -1):
                    lbl.config(text=f"Countdown: {i}s")
                    time.sleep(1)
                messagebox.showinfo("Timer", "Time is up!")
                lbl.config(text="Elapsed: 0.00s")
            threading.Thread(target=run, args=(s,), daemon=True).start()

        btns = ttk.Frame(win)
        btns.pack(pady=8)
        ttk.Button(btns, text="Start", command=start).grid(row=0,column=0,padx=6)
        ttk.Button(btns, text="Stop", command=stop).grid(row=0,column=1,padx=6)
        ttk.Button(btns, text="Reset", command=reset).grid(row=0,column=2,padx=6)
        ttk.Button(btns, text="Countdown", command=countdown).grid(row=0,column=3,padx=6)

        update_label()

    def open_file_organizer(self):
        fo = FileOrganizer()
        win = tk.Toplevel(self)
        win.title("File Organizer")
        win.geometry("600x400")

        target_var = tk.StringVar(value=os.path.expanduser("~"))
        dry_var = tk.BooleanVar(value=True)

        ttk.Label(win, text="Target dir:").pack(anchor="w", padx=8, pady=(8,0))
        ttk.Entry(win, textvariable=target_var).pack(fill="x", padx=8)
        ttk.Checkbutton(win, text="Dry run (no files will be moved)", variable=dry_var).pack(anchor="w", padx=8, pady=6)
        ttk.Button(win, text="Browse", command=lambda: target_var.set(filedialog.askdirectory())).pack(padx=8)

        out = tk.Text(win, height=12)
        out.pack(fill="both", expand=True, padx=8, pady=8)

        def run_org():
            t = target_var.get().strip()
            if not t:
                messagebox.showerror("Error", "Select a target directory")
                return
            try:
                acts = fo.organize(t, dry_run=dry_var.get())
                out.delete("1.0", "end")
                if not acts:
                    out.insert("end", "No files to organize")
                else:
                    for s,d in acts:
                        out.insert("end", f"{s} -> {d}\n")
                    if not dry_var.get():
                        out.insert("end", "\nOrganization complete.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Run", command=run_org).pack(pady=6)

    def open_unit_converter(self):
        uc = UnitConverter()
        win = tk.Toplevel(self)
        win.title("Unit Converter")
        win.geometry("400x300")

        ttk.Label(win, text="Value:").pack(anchor="w", padx=8, pady=(8,0))
        val_var = tk.StringVar()
        ttk.Entry(win, textvariable=val_var).pack(fill="x", padx=8)

        ttk.Label(win, text="From unit:").pack(anchor="w", padx=8, pady=(8,0))
        from_var = tk.StringVar()
        ttk.Entry(win, textvariable=from_var).pack(fill="x", padx=8)

        ttk.Label(win, text="To unit:").pack(anchor="w", padx=8, pady=(8,0))
        to_var = tk.StringVar()
        ttk.Entry(win, textvariable=to_var).pack(fill="x", padx=8)

        res_var = tk.StringVar()
        ttk.Label(win, textvariable=res_var, font=("Segoe UI", 10, "bold")).pack(pady=10)

        def do_conv(kind):
            try:
                v = float(val_var.get())
            except Exception:
                messagebox.showerror("Error", "Invalid value")
                return
            f = from_var.get().strip()
            t = to_var.get().strip()
            try:
                if kind == "length":
                    r = uc.length(v, f, t)
                elif kind == "weight":
                    r = uc.weight(v, f, t)
                else:
                    r = uc.temp(v, f, t)
                res_var.set(str(r))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        frame = ttk.Frame(win)
        frame.pack()
        ttk.Button(frame, text="Length", command=lambda: do_conv("length")).grid(row=0,column=0,padx=6)
        ttk.Button(frame, text="Weight", command=lambda: do_conv("weight")).grid(row=0,column=1,padx=6)
        ttk.Button(frame, text="Temp", command=lambda: do_conv("temp")).grid(row=0,column=2,padx=6)

    def open_backup_manager(self):
        bm = BackupManager()
        win = tk.Toplevel(self)
        win.title("Backup & Restore")
        win.geometry("600x400")

        out = tk.Text(win)
        out.pack(fill="both", expand=True)

        def refresh():
            out.delete("1.0", "end")
            for f in bm.list_backups():
                out.insert("end", f + "\n")

        def create():
            path = bm.create_backup()
            messagebox.showinfo("Backup created", path)
            refresh()

        def restore():
            files = bm.list_backups()
            if not files:
                messagebox.showinfo("Info", "No backups available")
                return
            sel = simpledialog.askinteger("Restore", f"Select backup number (1-{len(files)}):", parent=win, minvalue=1, maxvalue=len(files))
            if not sel:
                return
            ok = bm.restore(files[sel-1])
            messagebox.showinfo("Restore", "Succeeded" if ok else "Failed")
            refresh()

        btns = ttk.Frame(win)
        btns.pack(pady=6)
        ttk.Button(btns, text="Create Backup", command=create).grid(row=0,column=0,padx=6)
        ttk.Button(btns, text="List Backups", command=refresh).grid(row=0,column=1,padx=6)
        ttk.Button(btns, text="Restore Backup", command=restore).grid(row=0,column=2,padx=6)
        refresh()

    def show_file(self, path):
        if not os.path.exists(path):
            messagebox.showinfo("Info", "File not found")
            return
        win = tk.Toplevel(self)
        win.title(os.path.basename(path))
        txt = tk.Text(win)
        txt.pack(fill="both", expand=True)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt.insert("1.0", f.read())

if __name__ == "__main__":
    app = PPSApp()
    app.mainloop()
