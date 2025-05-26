import tkinter as tk
from timer import Timer
from utils import format_time

class clockwyrmApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ClockWyrm")

        self.timer = Timer(
            root=self.root,
            work_duration=25 * 60, 
            break_duration=5 * 60,
            update_callback=self.update_ui
        )

        self.label = tk.Label(root, text="Work Session", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.time_label = tk.Label(root, text=format_time(self.timer.remaining_time), font=("Helvetica", 48))
        self.time_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.timer.start)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.timer.pause)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_ui(self, time_str, session_type):
        self.time_label.config(text=time_str)
        self.label.config(text=session_type)

    def reset(self):
        self.timer.reset()
        self.update_ui(format_time(self.timer.remaining_time), "Work Session")



