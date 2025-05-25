import tkinter as tk
import time
from utils import format_time

class TimerApp:
    
    def __init__(self, work_duration, break_duration, update_callback):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.update_callback = update_callback
        self.is_running = False
        self.is_work_session = True