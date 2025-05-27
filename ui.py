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
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

        # Background Arc
        self.canvas.create_arc(50, 50, 250, 250, start=0, extent=359.9, outline='white', style= tk.ARC, width=20)

        # Prgression Arc
        self.progress_arc = self.canvas.create_arc(50, 50, 250, 250, start=0, extent=359.9, outline='purple', style=tk.ARC, width=20)

        # Time Label
        self.time_label = self.canvas.create_text(150, 150, text=format_time(self.timer.remaining_time), font=("Helvetica", 24), fill="black")

        # Start Button
        self.start_button = tk.Button(root, text="Start", command=self.timer.start, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Pause Button
        self.pause_button = tk.Button(root, text="Pause", command=self.timer.pause, bg="yellow", fg="black")
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Reset Button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset, bg="red", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        # === Task UI ===

        # Task list setup
        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(pady=20, fill=tk.X, padx=20)

        # Task entry
        self.task_entry = tk.Entry(self.tasks_frame, font=("Helvetica", 14), width=20)
        self.task_entry.pack(side=tk.LEFT, padx=10)

        
        self.add_task_button = tk.Button(self.tasks_frame, text="Add Task", command=Timer.add_task, bg="blue", fg="white")
        self.add_task_button.pack(side=tk.LEFT, padx=10)

        self.task_listbox = tk.Listbox(self.tasks_frame, font=("Helvetica", 14), width=30)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.delete_task_button = tk.Button(self.tasks_frame, text="Delete Task", command=Timer.delete_task, bg="red", fg="white")
        self.delete_task_button.pack(side=tk.LEFT, padx=10)

        self.start_task_button = tk.Button(self.tasks_frame, text="Start Task", command=Timer.start_selected_task, bg="green", fg="white")



    def update_ui(self, time_str, session_type):
        self.label.config(text=session_type)
        self.canvas.itemconfig(self.time_label, text=time_str)

        total_time = self.timer.work_duration if session_type == "Work Session" else self.timer.break_duration
        progress = 360 * (1 - self.timer.remaining_time / total_time)
        self.canvas.itemconfig(self.progress_arc, extent=progress)

    def reset(self):
        self.timer.reset()
        self.update_ui(format_time(self.timer.remaining_time), "Work Session")



