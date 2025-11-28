import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import json
import os
from datetime import datetime
import winsound


class TimerStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер-Секундомер")
        self.root.geometry("600x650")
        self.root.minsize(550, 600)

        self.setup_styles()

        self.timer_running = False
        self.stopwatch_running = False
        self.timer_time = 0
        self.stopwatch_time = 0
        self.timer_thread = None
        self.stopwatch_thread = None
        self.laps = []
        self.presets = self.load_presets()
        self.dark_mode = False

        self.stopwatch_history = []
        self.timer_start_time = 0

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

    def create_widgets(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Приложение", menu=app_menu)
        app_menu.add_command(label="Темная тема", command=self.toggle_dark_mode)
        app_menu.add_separator()
        app_menu.add_command(label="Выход", command=self.on_closing)

        action_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Действия", menu=action_menu)
        action_menu.add_command(label="Сохранить результаты", command=self.save_results)
        action_menu.add_command(label="Быстрый таймер 5 мин", command=lambda: self.quick_timer(300))
        action_menu.add_command(label="Быстрый таймер 10 мин", command=lambda: self.quick_timer(600))

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.time_label = ttk.Label(main_frame, text="", font=("Arial", 16, "bold"))
        self.time_label.pack(pady=(0, 20))
        self.update_current_time()

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        self.create_stopwatch_tab(notebook)
        self.create_timer_tab(notebook)
        self.create_presets_tab(notebook)
        self.create_stats_tab(notebook)

    def create_stopwatch_tab(self, notebook):
        stopwatch_frame = ttk.Frame(notebook, padding="20")
        notebook.add(stopwatch_frame, text="Секундомер")

        self.stopwatch_display = ttk.Label(stopwatch_frame, text="00:00:00.0",
                                           font=("Arial", 32, "bold"))
        self.stopwatch_display.pack(pady=20)

        self.stopwatch_progress = ttk.Progressbar(stopwatch_frame, orient='horizontal',
                                                  length=400, mode='determinate')
        self.stopwatch_progress.pack(pady=10)

        button_frame = ttk.Frame(stopwatch_frame)
        button_frame.pack(pady=20)

        self.start_stopwatch_btn = ttk.Button(button_frame, text="Старт",
                                              command=self.start_stopwatch, width=12)
        self.start_stopwatch_btn.pack(side=tk.LEFT, padx=5)

        self.stop_stopwatch_btn = ttk.Button(button_frame, text="Стоп",
                                             command=self.stop_stopwatch,
                                             state=tk.DISABLED, width=12)
        self.stop_stopwatch_btn.pack(side=tk.LEFT, padx=5)

        self.reset_stopwatch_btn = ttk.Button(button_frame, text="Сброс",
                                              command=self.reset_stopwatch, width=12)
        self.reset_stopwatch_btn.pack(side=tk.LEFT, padx=5)

    def create_timer_tab(self, notebook):
        timer_frame = ttk.Frame(notebook, padding="20")
        notebook.add(timer_frame, text="Таймер")

        presets_frame = ttk.LabelFrame(timer_frame, text="Быстрый запуск", padding="10")
        presets_frame.pack(fill=tk.X, pady=(0, 20))

        presets_buttons = [
            ("1 мин", 60), ("5 мин", 300), ("10 мин", 600),
            ("15 мин", 900), ("25 мин", 1500), ("30 мин", 1800)
        ]

        for text, seconds in presets_buttons:
            btn = ttk.Button(presets_frame, text=text,
                             command=lambda s=seconds: self.set_preset_time(s))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        input_frame = ttk.Frame(timer_frame)
        input_frame.pack(pady=20)

        time_units = [("Часы", "hours", 0, 23),
                      ("Минуты", "minutes", 0, 59),
                      ("Секунды", "seconds", 0, 59)]

        self.time_vars = {}
        for label_text, name, from_, to in time_units:
            unit_frame = ttk.Frame(input_frame)
            unit_frame.pack(side=tk.LEFT, padx=15)

            ttk.Label(unit_frame, text=label_text, font=("Arial", 12)).pack(pady=5)
            var = tk.StringVar(value="0")
            self.time_vars[name] = var

            spinbox = ttk.Spinbox(unit_frame, from_=from_, to=to, width=8,
                                  textvariable=var, font=("Arial", 12))
            spinbox.pack(pady=5)

        self.timer_display = ttk.Label(timer_frame, text="00:00:00",
                                       font=("Arial", 32, "bold"))
        self.timer_display.pack(pady=20)

        self.timer_progress = ttk.Progressbar(timer_frame, orient='horizontal',
                                              length=400, mode='determinate')
        self.timer_progress.pack(pady=10)

        timer_button_frame = ttk.Frame(timer_frame)
        timer_button_frame.pack(pady=20)

        self.start_timer_btn = ttk.Button(timer_button_frame, text="Запуск",
                                          command=self.start_timer, width=12)
        self.start_timer_btn.pack(side=tk.LEFT, padx=5)

        self.stop_timer_btn = ttk.Button(timer_button_frame, text="Пауза",
                                         command=self.stop_timer,
                                         state=tk.DISABLED, width=12)
        self.stop_timer_btn.pack(side=tk.LEFT, padx=5)

        self.reset_timer_btn = ttk.Button(timer_button_frame, text="Сброс",
                                          command=self.reset_timer, width=12)
        self.reset_timer_btn.pack(side=tk.LEFT, padx=5)

    def create_presets_tab(self, notebook):
        presets_frame = ttk.Frame(notebook, padding="20")
        notebook.add(presets_frame, text="Предустановки")

        add_frame = ttk.LabelFrame(presets_frame, text="Добавить предустановку", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.preset_name_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.preset_name_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Время (секунды):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.preset_time_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.preset_time_var, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить",
                   command=self.add_preset).grid(row=0, column=4, padx=5, pady=5)

        ttk.Label(presets_frame, text="Сохраненные предустановки:",
                  font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        self.presets_listbox = tk.Listbox(presets_frame, height=8, font=("Arial", 10))
        self.presets_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.update_presets_listbox()

        presets_buttons_frame = ttk.Frame(presets_frame)
        presets_buttons_frame.pack(pady=10)

        ttk.Button(presets_buttons_frame, text="Установить время",
                   command=self.load_selected_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(presets_buttons_frame, text="Удалить",
                   command=self.delete_preset).pack(side=tk.LEFT, padx=5)

    def create_stats_tab(self, notebook):
        stats_frame = ttk.Frame(notebook, padding="20")
        notebook.add(stats_frame, text="Статистика")

        stats_text = f"""
        Статистика приложения:

        Всего использовано секундомер: {self.get_usage_stats().get('stopwatch_uses', 0)} раз
        Всего использовано таймер: {self.get_usage_stats().get('timer_uses', 0)} раз
        Сохранено предустановок: {len(self.presets)}

        Последний запуск: {self.get_usage_stats().get('last_used', 'Никогда')}
        """

        self.stats_label = ttk.Label(stats_frame, text=stats_text, font=("Arial", 11),
                                     justify=tk.LEFT)
        self.stats_label.pack(anchor="w", pady=10)

        stats_buttons_frame = ttk.Frame(stats_frame)
        stats_buttons_frame.pack(pady=20)

        ttk.Button(stats_buttons_frame, text="Обновить статистику",
                   command=self.update_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(stats_buttons_frame, text="Сбросить статистику",
                   command=self.reset_stats).pack(side=tk.LEFT, padx=5)

    def update_current_time(self):
        current_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
        self.time_label.config(text=f"{current_time}")
        self.root.after(1000, self.update_current_time)

    def format_time(self, total_seconds, milliseconds=False):
        try:
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)

            if milliseconds:
                ms = int((total_seconds - int(total_seconds)) * 10)
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms}"
            else:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except:
            return "00:00:00.0" if milliseconds else "00:00:00"

    def start_stopwatch(self):
        try:
            if not self.stopwatch_running:
                self.stopwatch_running = True
                self.start_stopwatch_btn.config(state=tk.DISABLED)
                self.stop_stopwatch_btn.config(state=tk.NORMAL)

                self.stopwatch_thread = threading.Thread(target=self.update_stopwatch, daemon=True)
                self.stopwatch_thread.start()
                self.record_usage('stopwatch_uses')
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
            self.stopwatch_display.config(text="00:00:00.0")
            self.stopwatch_progress['value'] = 0
            self.start_stopwatch_btn.config(state=tk.NORMAL)
            self.stop_stopwatch_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сбросить секундомер: {e}")

    def update_stopwatch(self):
        start_time = time.time() - self.stopwatch_time
        while self.stopwatch_running:
            try:
                self.stopwatch_time = time.time() - start_time
                formatted_time = self.format_time(self.stopwatch_time, milliseconds=True)
                self.stopwatch_display.config(text=formatted_time)

                progress_value = (self.stopwatch_time % 60) / 60 * 100
                self.stopwatch_progress['value'] = progress_value

                time.sleep(0.1)
            except:
                break

    def start_timer(self):
        try:
            if not self.timer_running:
                hours = int(self.time_vars['hours'].get() or 0)
                minutes = int(self.time_vars['minutes'].get() or 0)
                seconds = int(self.time_vars['seconds'].get() or 0)

                self.timer_time = hours * 3600 + minutes * 60 + seconds
                self.timer_start_time = self.timer_time

                if self.timer_time > 0:
                    self.timer_running = True
                    self.start_timer_btn.config(state=tk.DISABLED)
                    self.stop_timer_btn.config(state=tk.NORMAL)

                    self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
                    self.timer_thread.start()
                    self.record_usage('timer_uses')
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
            self.timer_progress['value'] = 0
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

                progress_value = (1 - remaining_time / self.timer_start_time) * 100
                self.timer_progress['value'] = progress_value

                if remaining_time <= 10:
                    self.timer_display.config(foreground='red')
                elif remaining_time <= 30:
                    self.timer_display.config(foreground='orange')
                else:
                    self.timer_display.config(foreground='black')

                time.sleep(1)
                remaining_time -= 1

            if remaining_time <= 0 and self.timer_running:
                self.timer_running = False
                self.timer_display.config(text="00:00:00", foreground='red')
                self.timer_progress['value'] = 100
                self.start_timer_btn.config(state=tk.NORMAL)
                self.stop_timer_btn.config(state=tk.DISABLED)
                self.play_alarm()
                messagebox.showinfo("Таймер", "Время вышло!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка в работе таймера: {e}")

    def play_alarm(self):
        try:
            for _ in range(3):
                winsound.Beep(1000, 500)
                time.sleep(0.5)
        except:
            pass

    def set_preset_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        self.time_vars['hours'].set(str(hours))
        self.time_vars['minutes'].set(str(minutes))
        self.time_vars['seconds'].set(str(secs))

        self.timer_display.config(text=self.format_time(seconds))

    def add_preset(self):
        name = self.preset_name_var.get().strip()
        time_str = self.preset_time_var.get().strip()

        if not name or not time_str:
            messagebox.showwarning("Предупреждение", "Введите название и время")
            return

        try:
            time_seconds = int(time_str)
            if time_seconds <= 0:
                raise ValueError("Время должно быть положительным")

            self.presets[name] = time_seconds
            self.save_presets()
            self.update_presets_listbox()

            self.preset_name_var.set("")
            self.preset_time_var.set("")
            messagebox.showinfo("Успех", f"Предустановка '{name}' добавлена!")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное время в секундах")

    def update_presets_listbox(self):
        self.presets_listbox.delete(0, tk.END)
        for name, seconds in self.presets.items():
            time_str = self.format_time(seconds)
            self.presets_listbox.insert(tk.END, f"{name} - {time_str}")

    def load_selected_preset(self):
        selection = self.presets_listbox.curselection()
        if selection:
            index = selection[0]
            name = list(self.presets.keys())[index]
            seconds = self.presets[name]
            self.set_preset_time(seconds)

    def delete_preset(self):
        selection = self.presets_listbox.curselection()
        if selection:
            index = selection[0]
            name = list(self.presets.keys())[index]
            del self.presets[name]
            self.save_presets()
            self.update_presets_listbox()

    def quick_timer(self, seconds):
        self.set_preset_time(seconds)
        self.start_timer()

    def get_usage_stats(self):
        try:
            with open('timer_stats.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'stopwatch_uses': 0,
                'timer_uses': 0,
                'last_used': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    def record_usage(self, stat_type):
        stats = self.get_usage_stats()
        stats[stat_type] = stats.get(stat_type, 0) + 1
        stats['last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open('timer_stats.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except:
            pass

    def update_stats(self):
        stats = self.get_usage_stats()
        stats_text = f"""
        Статистика приложения:

        Всего использовано секундомер: {stats.get('stopwatch_uses', 0)} раз
        Всего использовано таймер: {stats.get('timer_uses', 0)} раз
        Сохранено предустановок: {len(self.presets)}

        Последний запуск: {stats.get('last_used', 'Никогда')}
        """
        self.stats_label.config(text=stats_text)

    def reset_stats(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить статистику?"):
            try:
                os.remove('timer_stats.json')
                self.update_stats()
                messagebox.showinfo("Успех", "Статистика сброшена!")
            except:
                pass

    def save_presets(self):
        try:
            with open('timer_presets.json', 'w', encoding='utf-8') as f:
                json.dump(self.presets, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_presets(self):
        try:
            with open('timer_presets.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "Кофе": 300,
                "Отдых": 600,
                "Помидорка": 1500,
                "Перерыв": 900
            }

    def save_results(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Результаты работы Таймер-Секундомера\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(f"Время экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                    f.write(f"Сохраниенные предустановки: {len(self.presets)}\n")
                    for name, seconds in self.presets.items():
                        f.write(f"  - {name}: {self.format_time(seconds)}\n")

                messagebox.showinfo("Успех", f"Результаты сохранены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить результаты: {e}")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.configure(bg='#2C3E50')
            style = ttk.Style()
            style.configure('TFrame', background='#2C3E50')
            style.configure('TLabel', background='#2C3E50', foreground='white')
            style.configure('TButton', background='#34495E', foreground='white')
            style.configure('TLabelframe', background='#2C3E50', foreground='white')
            style.configure('TLabelframe.Label', background='#2C3E50', foreground='white')
        else:
            self.root.configure(bg='SystemButtonFace')
            style = ttk.Style()
            style.theme_use('clam')

    def on_closing(self):
        try:
            self.timer_running = False
            self.stopwatch_running = False
            self.save_presets()
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