import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading


class TimerStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер-секундомер")
        self.root.geometry("450x500")
        self.root.minsize(400, 450)

        self.timer_running = False
        self.stopwatch_running = False
        self.timer_time = 0
        self.stopwatch_time = 0
        self.timer_thread = None
        self.stopwatch_thread = None

        self.create_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        title_label = ttk.Label(main_frame, text="Таймер-секундомер", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        self.create_stopwatch_tab(notebook)
        self.create_timer_tab(notebook)

    def create_stopwatch_tab(self, notebook):
        stopwatch_frame = ttk.Frame(notebook, padding="20")
        notebook.add(stopwatch_frame, text="Секундомер")
        self.stopwatch_display = ttk.Label(stopwatch_frame, text="00:00:00", font=("Arial", 28, "bold"))
        self.stopwatch_display.pack(pady=30)

        button_frame = ttk.Frame(stopwatch_frame)
        button_frame.pack(pady=30)

        self.start_stopwatch_btn = ttk.Button(button_frame, text="Старт",command=self.start_stopwatch,width=10)
        self.start_stopwatch_btn.pack(side=tk.LEFT, padx=10)

        self.stop_stopwatch_btn = ttk.Button(button_frame, text="Стоп",command=self.stop_stopwatch,state=tk.DISABLED,width=10)
        self.stop_stopwatch_btn.pack(side=tk.LEFT, padx=10)

        self.reset_stopwatch_btn = ttk.Button(button_frame, text="Сброс",command=self.reset_stopwatch,width=20)
        self.reset_stopwatch_btn.pack(side=tk.LEFT, padx=10)

    def create_timer_tab(self, notebook):
        timer_frame = ttk.Frame(notebook, padding="20")
        notebook.add(timer_frame, text="Таймер")
        input_frame = ttk.Frame(timer_frame)
        input_frame.pack(pady=20)
        hours_frame = ttk.Frame(input_frame)
        hours_frame.pack(side=tk.LEFT, padx=15)
        ttk.Label(hours_frame, text="Часы", font=("Arial", 12)).pack(pady=5)
        self.hours_var = tk.StringVar(value="0")
        hours_spinbox = ttk.Spinbox(hours_frame, from_=0, to=23, width=8,
                                    textvariable=self.hours_var, font=("Arial", 12))
        hours_spinbox.pack(pady=5)

        minutes_frame = ttk.Frame(input_frame)
        minutes_frame.pack(side=tk.LEFT, padx=15)
        ttk.Label(minutes_frame, text="Минуты", font=("Arial", 12)).pack(pady=5)
        self.minutes_var = tk.StringVar(value="0")
        minutes_spinbox = ttk.Spinbox(minutes_frame, from_=0, to=59, width=8,
                                      textvariable=self.minutes_var, font=("Arial", 12))
        minutes_spinbox.pack(pady=5)

        seconds_frame = ttk.Frame(input_frame)
        seconds_frame.pack(side=tk.LEFT, padx=15)
        ttk.Label(seconds_frame, text="Секунды", font=("Arial", 12)).pack(pady=5)
        self.seconds_var = tk.StringVar(value="0")
        seconds_spinbox = ttk.Spinbox(seconds_frame, from_=0, to=59, width=8,
                                      textvariable=self.seconds_var, font=("Arial", 12))
        seconds_spinbox.pack(pady=5)

        self.timer_display = ttk.Label(timer_frame, text="00:00:00", font=("Arial", 28, "bold"))
        self.timer_display.pack(pady=30)

        timer_button_frame = ttk.Frame(timer_frame)
        timer_button_frame.pack(pady=30)

        self.start_timer_btn = ttk.Button(timer_button_frame, text="Запуск",
                                          command=self.start_timer,
                                          width=10)
        self.start_timer_btn.pack(side=tk.LEFT, padx=10)

        self.stop_timer_btn = ttk.Button(timer_button_frame, text="Пауза",
                                         command=self.stop_timer,
                                         state=tk.DISABLED,
                                         width=10)
        self.stop_timer_btn.pack(side=tk.LEFT, padx=10)

        self.reset_timer_btn = ttk.Button(timer_button_frame, text="Сброс",
                                          command=self.reset_timer,
                                          width=10)
        self.reset_timer_btn.pack(side=tk.LEFT, padx=10)

    def format_time(self, total_seconds):
        try:
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except:
            return "00:00:00"

    def start_stopwatch(self):
        try:
            if not self.stopwatch_running:
                self.stopwatch_running = True
                self.start_stopwatch_btn.config(state=tk.DISABLED)
                self.stop_stopwatch_btn.config(state=tk.NORMAL)

                self.stopwatch_thread = threading.Thread(target=self.update_stopwatch, daemon=True)
                self.stopwatch_thread.start()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить секундомер: {e}")

    def stop_stopwatch(self):
        try:
            self.stopwatch_running = False
            self.start_stopwatch_btn.config(state=tk.NORMAL)
            self.stop_stopwatch_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось остановить секундомер: {e}")

    def reset_stopwatch(self):
        try:
            self.stopwatch_running = False
            self.stopwatch_time = 0
            self.stopwatch_display.config(text="00:00:00")
            self.start_stopwatch_btn.config(state=tk.NORMAL)
            self.stop_stopwatch_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сбросить секундомер: {e}")

    def update_stopwatch(self):
        start_time = time.time() - self.stopwatch_time
        while self.stopwatch_running:
            try:
                self.stopwatch_time = time.time() - start_time
                formatted_time = self.format_time(self.stopwatch_time)
                self.stopwatch_display.config(text=formatted_time)
                time.sleep(0.1)
            except:
                break

    def start_timer(self):
        try:
            if not self.timer_running:
                hours = int(self.hours_var.get() or 0)
                minutes = int(self.minutes_var.get() or 0)
                seconds = int(self.seconds_var.get() or 0)

                self.timer_time = hours * 3600 + minutes * 60 + seconds

                if self.timer_time > 0:
                    self.timer_running = True
                    self.start_timer_btn.config(state=tk.DISABLED)
                    self.stop_timer_btn.config(state=tk.NORMAL)

                    self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
                    self.timer_thread.start()
                else:
                    messagebox.showwarning("Предупреждение", "Установите время для таймера")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить таймер: {e}")

    def stop_timer(self):
        try:
            self.timer_running = False
            self.start_timer_btn.config(state=tk.NORMAL)
            self.stop_timer_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось остановить таймер: {e}")

    def reset_timer(self):

        try:
            self.timer_running = False
            self.timer_time = 0
            self.timer_display.config(text="00:00:00")
            self.start_timer_btn.config(state=tk.NORMAL)
            self.stop_timer_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сбросить таймер: {e}")

    def update_timer(self):
        try:
            remaining_time = self.timer_time
            while self.timer_running and remaining_time > 0:
                formatted_time = self.format_time(remaining_time)
                self.timer_display.config(text=formatted_time)
                time.sleep(1)
                remaining_time -= 1

            if remaining_time <= 0 and self.timer_running:
                self.timer_running = False
                self.timer_display.config(text="00:00:00")
                self.start_timer_btn.config(state=tk.NORMAL)
                self.stop_timer_btn.config(state=tk.DISABLED)
                messagebox.showinfo("Таймер", "Время вышло!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка в работе таймера: {e}")

    def on_closing(self):
        try:
            self.timer_running = False
            self.stopwatch_running = False
            self.root.destroy()
        except:
            self.root.destroy()

def main():
    try:
        root = tk.Tk()
        app = TimerStopwatchApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка",
                             f"Приложение не может быть запущено: {e}")

if __name__ == "__main__":
    main()