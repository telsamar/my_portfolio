#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, 'input')
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'input', 'forecast_config.json')
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, 'main.py')

DEFAULT_CONFIG = {"exclusions": [], "coefficients": []}

MONTHS = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"exclusions": [], "coefficients": []}


def save_config(data):
    os.makedirs(INPUT_DIR, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class ConfigEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Прогноз заявок — настройка и запуск")
        self.root.minsize(700, 550)
        self.root.geometry("900x620")

        self.config = load_config()
        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text="Исключения (город, месяц, год — необязательно)", font=('', 10, 'bold')).pack(anchor=tk.W)
        ex_frame = ttk.Frame(main)
        ex_frame.pack(fill=tk.BOTH, expand=True)
        ex_cols = ('city', 'month', 'year', 'comment')
        self.ex_tree = ttk.Treeview(ex_frame, columns=ex_cols, show='headings', height=4, selectmode='browse')
        for c in ex_cols:
            self.ex_tree.heading(c, text={'city': 'Город', 'month': 'Месяц', 'year': 'Год', 'comment': 'Комментарий'}[c])
            self.ex_tree.column(c, width=120)
        self.ex_tree.column('comment', width=220)
        ex_scroll = ttk.Scrollbar(ex_frame, orient=tk.VERTICAL, command=self.ex_tree.yview)
        self.ex_tree.configure(yscrollcommand=ex_scroll.set)
        self.ex_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ex_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.ex_tree.bind('<Delete>', lambda e: self._del_exclusion())
        self.ex_tree.bind('<Double-1>', lambda e: self._edit_exclusion())

        ex_btn_frame = ttk.Frame(main)
        ex_btn_frame.pack(fill=tk.X)
        ttk.Button(ex_btn_frame, text="Добавить исключение", command=self._add_exclusion).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(ex_btn_frame, text="Удалить", command=self._del_exclusion).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(ex_btn_frame, text="Изменить", command=self._edit_exclusion).pack(side=tk.LEFT)

        ttk.Label(main, text="Коэффициенты (город, месяц, коэффициент)", font=('', 10, 'bold')).pack(anchor=tk.W, pady=(15, 0))
        coef_frame = ttk.Frame(main)
        coef_frame.pack(fill=tk.BOTH, expand=True)
        coef_cols = ('city', 'month', 'coefficient', 'comment')
        self.coef_tree = ttk.Treeview(coef_frame, columns=coef_cols, show='headings', height=4, selectmode='browse')
        for c in coef_cols:
            self.coef_tree.heading(c, text={'city': 'Город', 'month': 'Месяц', 'coefficient': 'Коэф.', 'comment': 'Комментарий'}[c])
            self.coef_tree.column(c, width=100)
        self.coef_tree.column('comment', width=220)
        coef_scroll = ttk.Scrollbar(coef_frame, orient=tk.VERTICAL, command=self.coef_tree.yview)
        self.coef_tree.configure(yscrollcommand=coef_scroll.set)
        self.coef_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        coef_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.coef_tree.bind('<Delete>', lambda e: self._del_coefficient())
        self.coef_tree.bind('<Double-1>', lambda e: self._edit_coefficient())

        coef_btn_frame = ttk.Frame(main)
        coef_btn_frame.pack(fill=tk.X)
        ttk.Button(coef_btn_frame, text="Добавить коэффициент", command=self._add_coefficient).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(coef_btn_frame, text="Удалить", command=self._del_coefficient).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(coef_btn_frame, text="Изменить", command=self._edit_coefficient).pack(side=tk.LEFT)

        action_frame = ttk.Frame(main)
        action_frame.pack(fill=tk.X, pady=15)
        ttk.Button(action_frame, text="Сохранить конфиг", command=self._save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Запустить расчёт", command=self._run_forecast).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Загрузить из файла", command=self._reload_config).pack(side=tk.LEFT)

        ttk.Label(main, text="Лог", font=('', 9, 'bold')).pack(anchor=tk.W, pady=(5, 0))
        self.log_text = scrolledtext.ScrolledText(main, height=6, state=tk.DISABLED, wrap=tk.WORD, font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self._refresh_trees()

    def _log(self, msg: str):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + '\n')
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _config_from_trees(self):
        exclusions = []
        for iid in self.ex_tree.get_children():
            row = self.ex_tree.item(iid, 'values')
            exclusions.append({
                'city': (row[0] or '').strip(),
                'month': int(row[1]) if row[1] and str(row[1]).strip().isdigit() else None,
                'year': int(row[2]) if row[2] and str(row[2]).strip().isdigit() else None,
                'comment': (row[3] or '').strip()
            })
            if exclusions[-1]['month'] is None:
                del exclusions[-1]['month']
            if exclusions[-1]['year'] is None:
                del exclusions[-1]['year']
        coefficients = []
        for iid in self.coef_tree.get_children():
            row = self.coef_tree.item(iid, 'values')
            try:
                coef = float(str(row[2]).strip().replace(',', '.')) if row[2] else 1.0
            except ValueError:
                coef = 1.0
            coefficients.append({
                'city': (row[0] or '').strip(),
                'month': int(row[1]) if row[1] and str(row[1]).strip().isdigit() else None,
                'coefficient': coef,
                'comment': (row[3] or '').strip()
            })
            if coefficients[-1]['month'] is None:
                coefficients[-1]['month'] = 1
        return {'exclusions': exclusions, 'coefficients': coefficients}

    def _refresh_trees(self):
        for iid in self.ex_tree.get_children():
            self.ex_tree.delete(iid)
        for ex in self.config.get('exclusions', []):
            month = ex.get('month')
            year = ex.get('year')
            self.ex_tree.insert('', tk.END, values=(
                ex.get('city', ''),
                str(month) if month is not None else '',
                str(year) if year is not None else '',
                ex.get('comment', '')
            ))
        for iid in self.coef_tree.get_children():
            self.coef_tree.delete(iid)
        for co in self.config.get('coefficients', []):
            self.coef_tree.insert('', tk.END, values=(
                co.get('city', ''),
                str(co.get('month', '')) if co.get('month') is not None else '',
                str(co.get('coefficient', 1.0)),
                co.get('comment', '')
            ))

    def _add_exclusion(self):
        self._exclusion_dialog(None)

    def _edit_exclusion(self):
        sel = self.ex_tree.selection()
        if not sel:
            return
        iid = sel[0]
        row = self.ex_tree.item(iid, 'values')
        self._exclusion_dialog(iid, (row[0], row[1], row[2], row[3]))

    def _exclusion_dialog(self, iid, initial=None):
        initial = initial or ('', '', '', '')
        d = tk.Toplevel(self.root)
        d.title("Исключение")
        d.transient(self.root)
        d.grab_set()
        f = ttk.Frame(d, padding=10)
        f.pack(fill=tk.BOTH, expand=True)
        ttk.Label(f, text="Город:").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_city = ttk.Entry(f, width=30)
        e_city.grid(row=0, column=1, padx=5, pady=2)
        e_city.insert(0, initial[0])
        ttk.Label(f, text="Месяц (1–12, пусто = вся территория):").grid(row=1, column=0, sticky=tk.W, pady=2)
        e_month = ttk.Combobox(f, width=10, values=MONTHS)
        e_month.grid(row=1, column=1, padx=5, pady=2)
        e_month.set(initial[1] if initial[1] else '')
        ttk.Label(f, text="Год (пусто = все годы):").grid(row=2, column=0, sticky=tk.W, pady=2)
        e_year = ttk.Entry(f, width=10)
        e_year.grid(row=2, column=1, padx=5, pady=2)
        e_year.insert(0, initial[2] if initial[2] else '')
        ttk.Label(f, text="Комментарий:").grid(row=3, column=0, sticky=tk.W, pady=2)
        e_comment = ttk.Entry(f, width=40)
        e_comment.grid(row=3, column=1, padx=5, pady=2)
        e_comment.insert(0, initial[3] if initial[3] else '')

        def ok():
            city = e_city.get().strip()
            if not city:
                messagebox.showwarning("Внимание", "Укажите город.", parent=d)
                return
            month_s = e_month.get().strip()
            month = int(month_s) if month_s and month_s.isdigit() and 1 <= int(month_s) <= 12 else None
            year_s = e_year.get().strip()
            year = int(year_s) if year_s and year_s.isdigit() else None
            rec = {'city': city, 'comment': e_comment.get().strip()}
            if month is not None:
                rec['month'] = month
            if year is not None:
                rec['year'] = year
            if iid is not None:
                self.ex_tree.item(iid, values=(city, month_s or '', year_s or '', rec['comment']))
            else:
                self.ex_tree.insert('', tk.END, values=(city, month_s or '', year_s or '', rec['comment']))
            d.destroy()

        ttk.Button(f, text="OK", command=ok).grid(row=4, column=1, pady=10, sticky=tk.W)
        ttk.Button(f, text="Отмена", command=d.destroy).grid(row=4, column=1, padx=70, pady=10, sticky=tk.W)
        d.wait_window()

    def _del_exclusion(self):
        for iid in self.ex_tree.selection():
            self.ex_tree.delete(iid)

    def _add_coefficient(self):
        self._coefficient_dialog(None)

    def _edit_coefficient(self):
        sel = self.coef_tree.selection()
        if not sel:
            return
        iid = sel[0]
        row = self.coef_tree.item(iid, 'values')
        self._coefficient_dialog(iid, (row[0], row[1], row[2], row[3]))

    def _coefficient_dialog(self, iid, initial=None):
        initial = initial or ('', '1', '1.0', '')
        d = tk.Toplevel(self.root)
        d.title("Коэффициент")
        d.transient(self.root)
        d.grab_set()
        f = ttk.Frame(d, padding=10)
        f.pack(fill=tk.BOTH, expand=True)
        ttk.Label(f, text="Город:").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_city = ttk.Entry(f, width=30)
        e_city.grid(row=0, column=1, padx=5, pady=2)
        e_city.insert(0, initial[0])
        ttk.Label(f, text="Месяц (1–12):").grid(row=1, column=0, sticky=tk.W, pady=2)
        e_month = ttk.Combobox(f, width=10, values=MONTHS[1:])
        e_month.grid(row=1, column=1, padx=5, pady=2)
        e_month.set(initial[1] if initial[1] else '1')
        ttk.Label(f, text="Коэффициент:").grid(row=2, column=0, sticky=tk.W, pady=2)
        e_coef = ttk.Entry(f, width=10)
        e_coef.grid(row=2, column=1, padx=5, pady=2)
        e_coef.insert(0, initial[2] if initial[2] else '1.0')
        ttk.Label(f, text="Комментарий:").grid(row=3, column=0, sticky=tk.W, pady=2)
        e_comment = ttk.Entry(f, width=40)
        e_comment.grid(row=3, column=1, padx=5, pady=2)
        e_comment.insert(0, initial[3] if initial[3] else '')

        def ok():
            city = e_city.get().strip()
            if not city:
                messagebox.showwarning("Внимание", "Укажите город.", parent=d)
                return
            month_s = e_month.get().strip()
            try:
                month = int(month_s) if month_s else 1
                if month < 1 or month > 12:
                    raise ValueError()
            except ValueError:
                messagebox.showwarning("Внимание", "Месяц должен быть от 1 до 12.", parent=d)
                return
            try:
                coef = float(e_coef.get().strip().replace(',', '.'))
            except ValueError:
                messagebox.showwarning("Внимание", "Введите число для коэффициента.", parent=d)
                return
            if iid is not None:
                self.coef_tree.item(iid, values=(city, str(month), str(coef), e_comment.get().strip()))
            else:
                self.coef_tree.insert('', tk.END, values=(city, str(month), str(coef), e_comment.get().strip()))
            d.destroy()

        ttk.Button(f, text="OK", command=ok).grid(row=4, column=1, pady=10, sticky=tk.W)
        ttk.Button(f, text="Отмена", command=d.destroy).grid(row=4, column=1, padx=70, pady=10, sticky=tk.W)
        d.wait_window()

    def _del_coefficient(self):
        for iid in self.coef_tree.selection():
            self.coef_tree.delete(iid)

    def _save_config(self):
        self.config = self._config_from_trees()
        try:
            save_config(self.config)
            self._log(f"Конфиг сохранён: {CONFIG_PATH}")
            messagebox.showinfo("Сохранено", f"Конфигурация сохранена в\n{CONFIG_PATH}", parent=self.root)
        except Exception as e:
            self._log(f"Ошибка сохранения: {e}")
            messagebox.showerror("Ошибка", str(e), parent=self.root)

    def _reload_config(self):
        self.config = load_config()
        self._refresh_trees()
        self._log("Конфиг загружен из файла.")
        messagebox.showinfo("Загружено", "Конфигурация загружена из файла.", parent=self.root)

    def _run_forecast(self):
        self.config = self._config_from_trees()
        try:
            save_config(self.config)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить конфиг: {e}", parent=self.root)
            return
        self._log("Запуск расчёта...")
        self.root.update()
        try:
            proc = subprocess.run(
                [sys.executable, MAIN_SCRIPT],
                cwd=SCRIPT_DIR,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            out = (proc.stdout or '') + (proc.stderr or '')
            if out:
                self._log(out.strip())
            if proc.returncode == 0:
                self._log("Готово.")
                messagebox.showinfo("Готово", "Расчёт завершён успешно.", parent=self.root)
            else:
                self._log(f"Завершено с кодом {proc.returncode}")
                messagebox.showwarning("Завершено", f"Процесс завершился с кодом {proc.returncode}. См. лог.", parent=self.root)
        except Exception as e:
            self._log(f"Ошибка запуска: {e}")
            messagebox.showerror("Ошибка", str(e), parent=self.root)

    def run(self):
        self.root.mainloop()


def main():
    app = ConfigEditorApp()
    app.run()


if __name__ == "__main__":
    main()
