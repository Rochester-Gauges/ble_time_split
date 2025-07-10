import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import traceback

class TimeRangePopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Enter Start and End Times")
        self.grab_set()  # Make this window modal

        self.start_entries = {}
        self.end_entries = {}
        self.result = None  # Stores the result after submission

        self._build_ui()

    def _build_ui(self):
        # Common labels
        labels = ['Month', 'Day', 'Year', 'Hour', 'Minute', 'Second']

        # Numeric-only validation
        vcmd = (self.register(self._validate_digit), '%P')

        # Start time
        tk.Label(self, text="Start Time").grid(row=0, column=0, columnspan=6, pady=(10, 0))
        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=1, column=i)
            entry = tk.Entry(self, width=4, validate="key", validatecommand=vcmd)
            entry.grid(row=2, column=i)
            self.start_entries[label.lower()] = entry

        # End time
        tk.Label(self, text="End Time").grid(row=3, column=0, columnspan=6, pady=(10, 0))
        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=4, column=i)
            entry = tk.Entry(self, width=4, validate="key", validatecommand=vcmd)
            entry.grid(row=5, column=i)
            self.end_entries[label.lower()] = entry

        # Submit button
        submit_btn = tk.Button(self, text="Submit", command=self._on_submit)
        submit_btn.grid(row=6, column=0, columnspan=6, pady=10)

    def _validate_digit(self, P):
        return P.isdigit() or P == ""

    def _get_datetime_from_entries(self, entries_dict):
        try:
            parts = [int(entries_dict[k].get()) for k in ['year', 'month', 'day', 'hour', 'minute', 'second']]
            return datetime(*parts)
        except Exception:
            traceback.print_exc()
            return None

    def _on_submit(self):
        start = self._get_datetime_from_entries(self.start_entries)
        end = self._get_datetime_from_entries(self.end_entries)

        if not start or not end:
            messagebox.showerror("Invalid Input", "Please enter valid numeric date/time values.")
            return

        if start >= end:
            messagebox.showwarning("Invalid Range", "Start time must be before end time.")
            return

        self.result = (start, end)
        self.destroy()
        
        
def open_popup(root):
    popup = TimeRangePopup(root)
    root.wait_window(popup)

    if popup.result:
        start, end = popup.result
        if not start or not end:
            return None, None
        return start, end