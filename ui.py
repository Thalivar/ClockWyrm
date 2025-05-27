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

        # === Task Function ===

        # Task list setup
        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(pady=20, fill=tk.X, padx=20)

        # Task entry
        self.task_entry = tk.Entry(self.tasks_frame, font=("Helvetica", 14), width=20)
        self.task_entry.pack(side=tk.LEFT, padx=10)
        
        # Add task button
        self.add_task_button = tk.Button(self.tasks_frame, text="Add Task", command=Timer.add_task, bg="blue", fg="white")
        self.add_task_button.pack(side=tk.LEFT, padx=10)

        # Task listbox
        self.task_listbox = tk.Listbox(self.tasks_frame, font=("Helvetica", 14), width=30)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Task delete button
        self.delete_task_button = tk.Button(self.tasks_frame, text="Delete Task", command=Timer.delete_task, bg="red", fg="white")
        self.delete_task_button.pack(side=tk.LEFT, padx=10)

        # Task start button
        self.start_task_button = tk.Button(self.tasks_frame, text="Start Task", command=Timer.start_selected_task, bg="green", fg="white")
        self.start_task_button.pack(side=tk.LEFT, padx=10)

        # Task control frames
        self.take_control = tk.Frame(root)
        self.take_control.pack(pady=20, fill=tk.X, padx=20)

        # === Task Data ===

        self.tasks = []
        self.current_task = None
        self.task_time_log = {}

        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

    def update_ui(self, time_str, session_type):
        self.label.config(text=session_type)
        self.canvas.itemconfig(self.time_label, text=time_str)

        total_time = self.timer.work_duration if session_type == "Work Session" else self.timer.break_duration
        progress = 360 * (1 - self.timer.remaining_time / total_time)
        self.canvas.itemconfig(self.progress_arc, extent=progress)

        if self.current_task:
            time_spent = self.task_time_log.get(self.current_task, 0)
            self.label.config(text=f"Working on: {self.current_task} (Time Spent: {format_time(time_spent)})")

    def reset(self):
        self.timer.reset()
        self.update_ui(format_time(self.timer.remaining_time), "Work Session")

    def add_task(self):
        task = self.task_entry.get().strip()
        if task and task not in self.tasks:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_time_log[task] = 0
            self.task_entry.delete(0, tk.END)
    
    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            task = self.tasks_listbox.get(selected)
            self.tasks_listbox.delete(selected)
            del self.task_time_log[task]
    
    def start_selected_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            self.current_task = self.tasks_listbox.get(selected)
            self.label.config(text=f"Working on: {self.current_task}")
            self.timer_reset()

    def enable_task_buttons(self):
        if self.task_listbox.curselection():
            self.start_task_button.config(state=tk.NORMAL)
            self.delete_task_button.config(state=tk.NORMAL)



