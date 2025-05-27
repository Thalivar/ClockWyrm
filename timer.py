import tkinter as tk
import time
from utils import format_time

class Timer():
    
    def __init__(self, root, work_duration, break_duration, update_callback):
        self.root = root
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.update_callback = update_callback
        self.remaining_time = work_duration
        
        self.is_running = False
        self.is_work_session = True
        self.timer_id = None

    def _tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_callback(format_time(self.remaining_time), "Work Session" if self.is_work_session else "Break")
            self.timer_id = self.root.after(1000, self._tick)
        else:
            self.is_work_session = not self.is_work_session
            self.remaining_time = self.work_duration if self.is_work_session else self.break_duration
            self._tick()
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self._tick()
    
    def pause(self):
        if self.is_running:
            self.root.after_cancel(self.timer_id)
            self.is_running = False
    
    def reset(self):
        if self.is_running:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.is_work_session = True
        self.remaining_time = self.work_duration
        self.update_callback(format_time(self.remaining_time), "Work Session")

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