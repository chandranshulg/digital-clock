import tkinter as tk
import time

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        self.label = tk.Label(root, font=('Arial', 50), background='black', foreground='white')
        self.label.pack(anchor='center')

        self.format_12hr = True  # Start in 12-hour format

        self.switch_format_button = tk.Button(root, text="Switch to 24-hour format", command=self.switch_format)
        self.switch_format_button.pack(side='left', padx=10)

        self.timer_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.timer_button.pack(side='right', padx=10)

        self.stopwatch_button = tk.Button(root, text="Start Stopwatch", command=self.start_stopwatch)
        self.stopwatch_button.pack(side='right', padx=10)

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime('%I:%M:%S %p' if self.format_12hr else '%H:%M:%S')
        self.label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def switch_format(self):
        self.format_12hr = not self.format_12hr
        new_format = "24-hour" if not self.format_12hr else "12-hour"
        self.switch_format_button.config(text=f"Switch to {new_format} format")

    def start_timer(self):
        self.timer_window = tk.Toplevel(self.root)
        self.timer_window.title("Timer")
        self.timer_label = tk.Label(self.timer_window, font=('Arial', 30), text="00:00:00")
        self.timer_label.pack(anchor='center')

        self.time_entry = tk.Entry(self.timer_window)
        self.time_entry.pack(anchor='center')
        self.time_entry.insert(0, "Enter time in seconds")

        self.start_button = tk.Button(self.timer_window, text="Start", command=self.countdown)
        self.start_button.pack(anchor='center')

    def countdown(self):
        try:
            total_time = int(self.time_entry.get())
            self.timer_label.config(text=self.format_time(total_time))
            self.decrement_time(total_time)
        except ValueError:
            self.timer_label.config(text="Invalid time!")

    def decrement_time(self, remaining_time):
        if remaining_time > 0:
            self.timer_window.after(1000, self.decrement_time, remaining_time - 1)
            self.timer_label.config(text=self.format_time(remaining_time))
        else:
            self.timer_label.config(text="Time's up!")

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"

    def start_stopwatch(self):
        self.stopwatch_window = tk.Toplevel(self.root)
        self.stopwatch_window.title("Stopwatch")
        self.stopwatch_label = tk.Label(self.stopwatch_window, font=('Arial', 30), text="00:00:00")
        self.stopwatch_label.pack(anchor='center')

        self.elapsed_time = 0
        self.running = False

        self.start_stopwatch_button = tk.Button(self.stopwatch_window, text="Start", command=self.start_stopwatch_count)
        self.start_stopwatch_button.pack(anchor='center')

        self.stop_stopwatch_button = tk.Button(self.stopwatch_window, text="Stop", command=self.stop_stopwatch_count)
        self.stop_stopwatch_button.pack(anchor='center')

        self.reset_stopwatch_button = tk.Button(self.stopwatch_window, text="Reset", command=self.reset_stopwatch_count)
        self.reset_stopwatch_button.pack(anchor='center')

    def start_stopwatch_count(self):
        self.running = True
        self.update_stopwatch()

    def update_stopwatch(self):
        if self.running:
            self.elapsed_time += 1
            self.stopwatch_label.config(text=self.format_time(self.elapsed_time))
            self.stopwatch_window.after(1000, self.update_stopwatch)

    def stop_stopwatch_count(self):
        self.running = False

    def reset_stopwatch_count(self):
        self.elapsed_time = 0
        self.stopwatch_label.config(text="00:00:00")


if __name__ == "__main__":
    root = tk.Tk()
    clock = DigitalClock(root)
    root.mainloop()
