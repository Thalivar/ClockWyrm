import tkinter as tk
from timer import Timer
from utils import format_time

class clockwyrmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ClockWyrm")
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.config(bg="#3B3939")

        # Timer Setup
        self.timer = Timer(
            root=self.root,
            work_duration=1 * 30, 
            break_duration=1 * 30,
            update_callback=self.update_ui
        )

        # Session Label
        self.label = tk.Label(root, text="Work Session", font=("Helvetica", 24,), bg="#3B3939")
        self.label.pack(pady=10)

        # Progression Bar
        self.canvas = tk.Canvas(root, width=300, height=300, bg="#3B3939")
        self.canvas.pack(pady=10)

        # Background Arc
        self.canvas.create_arc(50, 50, 250, 250, start=0, extent=359.9, outline='#3B3939', style=tk.ARC, width=20)

        # Progress Arc
        self.progress_arc = self.canvas.create_arc(50, 50, 250, 250, start=0, extent=0, outline="#D17DE6", style=tk.ARC, width=20)

        # Time Label
        self.time_label = self.canvas.create_text(150, 150, text=format_time(self.timer.remaining_time), font=("Helvetica", 24), fill="white")

        # Start Timer Button
        self.start_button = tk.Button(root, text="Start", command=self.timer.start, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Pause Timer Button
        self.pause_button = tk.Button(root, text="Pause", command=self.timer.pause, bg="yellow", fg="black")
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Reset Timer Button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset, bg="red", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        # === Task UI ===
        self.tasks_frame = tk.Frame(root, bg="#3B3939")
        self.tasks_frame.pack(pady=20, fill=tk.X, padx=20, )

        # Task Entry
        self.task_entry = tk.Entry(self.tasks_frame, font=("Helvetica", 14), width=20, bg="#3B3939")
        self.task_entry.pack(side=tk.LEFT, padx=10)
        
        # Add Task Button
        self.add_task_button = tk.Button(self.tasks_frame, text="Add Task", command=self.add_task, bg="blue", fg="white")
        self.add_task_button.pack(side=tk.LEFT, padx=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(self.tasks_frame, font=("Helvetica", 14), height=5, bg="#696666")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Task Control Buttons
        self.delete_task_button = tk.Button(self.tasks_frame, text="Delete Task", command=self.delete_task, bg="red", fg="white", state=tk.DISABLED)
        self.delete_task_button.pack(side=tk.LEFT, padx=10)

        self.start_task_button = tk.Button(self.tasks_frame, text="Start Task", command=self.start_selected_task, bg="green", fg="white", state=tk.DISABLED)
        self.start_task_button.pack(side=tk.LEFT, padx=10)

        # === Task Data ===
        self.tasks = []
        self.current_task = None
        self.task_time_log = {}

        # Bind selection event
        self.task_listbox.bind("<<ListboxSelect>>", lambda e: self.enable_task_buttons())

        self.timer_frame = tk.Frame(root, bg="#3B3939")
        self.timer_frame.pack(pady=10)

        tk.Label(self.timer_frame, text="Work (mins)", bg="#3B3939", fg="white").pack(side=tk.LEFT)
        self.work_entry = tk.Entry(self.timer_frame, width=5)
        self.work_entry.pack(side=tk.LEFT, padx=5)
        self.work_entry.insert(0, 25)

        tk.Label(self.timer_frame, text="Break (mins)", bg="#3B3939", fg="white").pack(side=tk.LEFT)
        self.break_entry = tk.Entry(self.timer_frame, width=5)
        self.break_entry.pack(side=tk.LEFT, padx=5)
        self.break_entry.insert(0, 5)

        tk.Button(self.timer_frame, text="Set Timer", command=self.set_custom_time, bg="purple", fg="white").pack(side=tk.LEFT, padx=10)

    def update_ui(self, time_str, session_type):
        self.canvas.itemconfig(self.time_label, text=time_str)
        
        total_time = self.timer.work_duration if session_type == "Work Session" else self.timer.break_duration
        progress = 360 * (1 - self.timer.remaining_time / total_time)
        self.canvas.itemconfig(self.progress_arc, extent=-progress)  # Negative for clockwise

        if self.current_task:
            time_spent = self.timer.task_time_log.get(self.current_task, 0)
            self.label.config(text=f"{session_type}\nTask: {self.current_task} (Time: {format_time(time_spent)})")

    def reset(self):
        self.timer.reset()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task and task not in self.tasks:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_time_log[task] = 0
            self.task_entry.delete(0, tk.END)
    
    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task = self.task_listbox.get(selected)
            self.task_listbox.delete(selected)
            self.tasks.remove(task)
            del self.task_time_log[task]
            self.enable_task_buttons()
    
    def start_selected_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task_name = self.task_listbox.get(selected)
            self.current_task = task_name
            self.timer.set_current_task(task_name)
            self.timer.reset()
    
    def enable_task_buttons(self):
        if self.task_listbox.curselection():
            self.start_task_button.config(state=tk.NORMAL)
            self.delete_task_button.config(state=tk.NORMAL)
        else:
            self.start_task_button.config(state=tk.DISABLED)
            self.delete_task_button.config(state=tk.DISABLED)
    
    def on_close(self):
        self.timer.save_logs()
        self.root.destroy()      

    def set_custom_time(self):
        try:
            work_mins = int(self.work_entry.get())
            break_mins = int(self.break_entry.get())
            if work_mins > 0 and break_mins > 0:
                self.timer.set_duration(work_mins, break_mins)
        except ValueError:
            pass
