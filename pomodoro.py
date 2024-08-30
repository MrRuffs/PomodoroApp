import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

# Set the default timers
WORK_TIME = 25 * 60  # 25 minutes
SHORT_BREAK_TIME = 5 * 60  # 5 minutes
LONG_BREAK_TIME = 15 * 60  # 15 minutes

class PomodoroTimer:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("400x250")  # Increased size for additional input field
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="darkly")  # Updated theme for better design
        self.style.theme_use()

        # Create a main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Task Input Field
        self.task_entry = ttk.Entry(self.main_frame, width=40)
        self.task_entry.pack(pady=(0, 10))
        self.task_entry.insert(0, "Enter your task here...")

        # Timer Type Label
        self.type_label = ttk.Label(self.main_frame, text="Work Time", font=("Helvetica", 18))
        self.type_label.pack(pady=(0, 10))

        # Timer Display Label
        self.timer_label = ttk.Label(self.main_frame, text="25:00", font=("Helvetica", 48))  # Default to work time
        self.timer_label.pack(pady=(0, 20))

        # Buttons Frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=(10, 0))

        # Start, Stop, and Skip Buttons
        self.start_button = ttk.Button(self.buttons_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(self.buttons_frame, text="Stop", command=self.stop_timer, state="DISABLED")
        self.stop_button.grid(row=0, column=1, padx=10)

        self.skip_button = ttk.Button(self.buttons_frame, text="Skip", command=self.skip_timer)
        self.skip_button.grid(row=0, column=2, padx=10)

        # Timer and State Variables
        self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False
        self.current_time = WORK_TIME  # Initialize current time to work time
        self.current_task = ""  # Initialize current task as an empty string

        self.update_type_label()
        self.update_timer_display()  # Initialize the timer display with the correct time
        self.root.mainloop()
    
    def start_timer(self):
        task = self.task_entry.get().strip()
        if not task or task == "Enter your task here...":
            messagebox.showwarning("Warning", "Please enter a task before starting the timer.")
            return

        self.current_task = task
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.skip_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()
    
    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        self.is_running = False
    
    def skip_timer(self):
        if self.is_running:
            self.stop_timer()  # Stop the timer

        if self.is_work_time:
            # Skip to break time
            self.current_time = 0  # Set work time to 0 to show as ended
            self.is_work_time = False
            self.pomodoros_completed += 1
            if self.pomodoros_completed % 4 == 0:
                self.break_time = LONG_BREAK_TIME
                messagebox.showinfo("Break Time", "You've completed 4 pomodoros! Enjoy a long break.")
            else:
                self.break_time = SHORT_BREAK_TIME
                messagebox.showinfo("Break Time", "You've skipped to a short break time.")
            self.current_time = self.break_time
        else:
            # Skip to the next work session
            self.current_time = 0  # Set break time to 0 to show as ended
            self.is_work_time = True
            self.work_time = WORK_TIME
            self.current_time = self.work_time
            messagebox.showinfo("Work Time", "You've skipped to the next work session.")

        # Update the display immediately
        self.update_type_label()
        self.update_timer_display()
    
    def update_timer(self):
        if self.is_running:
            self.current_time -= 1
            if self.current_time == 0:
                if self.is_work_time:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                    messagebox.showinfo("Great job!" if self.pomodoros_completed % 4 == 0 
                                        else "Good job!", "Take a long break and rest!"
                                        if self.pomodoros_completed % 4 == 0 
                                        else "Take a short break!"
                                        )
                    self.current_time = self.break_time
                else:
                    self.is_work_time = True
                    self.work_time = WORK_TIME
                    self.current_time = self.work_time
                    messagebox.showinfo("Work time", "Get back to work!")

            self.update_timer_display()
            self.root.after(1000, self.update_timer)  # Continue updating every second
    
    def update_timer_display(self):
        minutes, seconds = divmod(self.current_time, 60)
        self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
    
    def update_type_label(self):
        if self.is_work_time:
            self.type_label.config(text=f"Work Time: {self.current_task}")
        elif self.pomodoros_completed % 4 == 0:
            self.type_label.config(text="Long Break")
        else:
            self.type_label.config(text="Short Break")

PomodoroTimer()
