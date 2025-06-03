import tkinter as tk
import time
from utils import format_time, play_sound
import json
import os

class Timer():
    
    def __init__(self, root, work_duration, break_duration, update_callback):
        self.root = root
        self.default_work_duration = work_duration
        self.default_break_duration = break_duration
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.update_callback = update_callback
        self.remaining_time = work_duration
        
        self.is_running = False
        self.is_work_session = True
        self.timer_id = None

        self.task_time_log = {}
        self.current_task = None
        self.load_logs()

    def _tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_callback(format_time(self.remaining_time), "Work Session" if self.is_work_session else "Break")
            self.timer_id = self.root.after(1000, self._tick)
        else:

            play_sound("work" if self.is_work_session else "break")

            if self.is_work_session and hasattr(self, 'current_task'):
                if self.current_task in self.task_time_log:
                    self.task_time_log[self.current_task] += self.work_duration
            
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
    
    def save_logs(self, filename="task_time_log.json"):
        with open(filename, 'w') as f:
            json.dump(self.task_time_log, f, indent=4)
        
    def set_current_task(self, task_name):
        self.current_task = task_name
        if task_name not in self.task_time_log:
            self.task_time_log[task_name] = 0

    def load_logs(self, filename="task_time_log.json"):
        try:
            with open(filename, 'r') as f:
                self.task_time_log = json.load(f)
        except FileNotFoundError:
            self.task_time_log = {}          

    def set_duration(self, work_mins, break_mins):
        self.work_duration = work_mins * 60
        self.break_duration = break_mins * 60
        self.reset()