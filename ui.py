import tkinter as tk
from timer import Timer
from utils import format_time

class clockwyrmApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ClockWyrm")

        # Timer Setup
        self.timer = Timer(
            root=self.root,
            work_duration=1 * 60, 
            break_duration=1 * 60,
            update_callback=self.update_ui
        )

        # Session Label
        self.label = tk.Label(root, text="Work Session", font=("Helvetica", 24))
        self.label.pack(pady=10)

        # Progression Bar
        self.canvas = tk.Canvas(root, width=300, height=300, bg="lightgrey")
        self.canvas.pack(pady=10)

        # Background Arc
        self.canvas.create_arc(50, 50, 250, 250, start=0, extent=359.9, outline='lightgray', style= tk.ARC, width=20)

        # Prgression Arc
        self.progress_arc = self.canvas.create_arc(50, 50, 250, 250, start=0, extent=359.9, outline='purple', style=tk.ARC, width=20)

        # Time Label
        self.time_label = self.canvas.create_text(150, 150, text=format_time(self.timer.remaining_time), font=("Helvetica", 24), fill="black")

        # Start Button
        self.start_button = tk.Button(root, text="Start", command=self.timer.start)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Pause Button
        self.pause_button = tk.Button(root, text="Pause", command=self.timer.pause)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Reset Button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_ui(self, time_str, session_type):
        self.label.config(text=session_type)
        self.canvas.itemconfig(self.time_label, text=time_str)

        total_time = self.timer.work_duration if session_type == "Work Session" else self.timer.break_duration
        progress = 360 * (1 - self.timer.remaining_time / total_time)
        self.canvas.itemconfig(self.progress_arc, extent=progress)

    def reset(self):
        self.timer.reset()
        self.update_ui(format_time(self.timer.remaining_time), "Work Session")



