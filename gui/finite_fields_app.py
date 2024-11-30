import math
import threading
import tkinter as tk
import numpy as np
# noinspection PyPackageRequirements
from formation import AppBuilder
from tkinter import messagebox

from finite_fields.finite_field import FiniteField
from primitive_element_finders.fast_primitive_finder import FastPrimitiveFinder
from utils.is_prime import is_prime_power


class FiniteFieldsApp:
    def __init__(self):
        self._current_canvas = None
        self.primitive = None
        self.app = AppBuilder(path='resources/finite_fields_app_formation.xml')
        self.__primitive_finder = None
        self.__finite_field = None
        self.__elements = None
        self.__p = None
        self.__n = None
        self.init_app()

    def run(self):
        self.app.mainloop()

    def init_app(self):
        self.__change_lang_to_russian()
        scrollbar = tk.Scrollbar(self.app._root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.app.listbox_field_elements.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.app.listbox_field_elements.yview)
        self.app.progressbar['value'] = 0
        self.app.button_find_field['command'] = self.press_find_button
        self.app.button_use_another_primitive['command'] = self.pres_find_with_another_primitive_button

    def press_find_button(self):
        self.app.progressbar['value'] = 0
        threading.Thread(target=self.find_primitive_and_build_field, daemon=True).start()

    def pres_find_with_another_primitive_button(self):
        self.app.progressbar['value'] = 0
        threading.Thread(target=self.find_with_another_primitve, daemon=True).start()

    def find_primitive_and_build_field(self):
        text: str = self.app.entry_field_size.get()
        if not len(text.split('^')) == 2 and not text.isdecimal():
            messagebox.showerror("Ошибка", "Введите в поле степень простого числа")
            return
        if '^' in text:
            try:
                num = int(text.split('^')[0]) ** int(text.split('^')[1])
            except ValueError:
                messagebox.showerror("Ошибка", "Введите в поле степень простого числа")
                return
        else:
            num = int(text)

        self.__p = is_prime_power(num)
        if self.__p == -1:
            messagebox.showerror("Ошибка", f"{num} - это не степень простого числа")
            return
        self.app.button_find_field['state'] = 'disabled'
        self.app.progressbar['value'] = 0
        self.__p, self.__n = round(self.__p), round(math.log(num, self.__p))
        self.__primitive_finder = FastPrimitiveFinder(self.__p, self.__n)
        self.app.label_status['text'] = "Поиск примитивного элемента..."
        primitive = self.__primitive_finder.find_first()
        self.app.progressbar['value'] = 20
        self.__finite_field = FiniteField(self.__p, self.__n, primitive)
        self.app.label_status['text'] = "Построение конечного поля..."
        self.__elements = self.__finite_field.get_elements(view='vector', progressbar=self.app.progressbar)
        self.app.progressbar['value'] = 90
        self.app.label_status['text'] = "Заполнение списка..."
        self.app._root.after(0, self.fill_listbox)
        self.draw_matrix(primitive)
        self.app.button_find_field['state'] = 'normal'
        self.app.button_use_another_primitive['state'] = 'normal'

    def find_with_another_primitve(self):
        if self.__primitive_finder is not None:
            self.app.entry_field_size.delete(0, tk.END)
            self.app.entry_field_size.insert(0, f"{self.__p}^{self.__n}")

            self.app.button_find_field['state'] = 'disabled'
            self.app.button_use_another_primitive['state'] = 'disabled'
            self.app.label_status['text'] = "Поиск примитивного элемента..."
            primitive = self.__primitive_finder.find_next()
            self.app.progressbar['value'] = 20
            self.__finite_field = FiniteField(self.__p, self.__n, primitive)
            self.app.label_status['text'] = "Построение конечного поля..."
            self.__elements = self.__finite_field.get_elements(view='vector', progressbar=self.app.progressbar)
            self.app.progressbar['value'] = 90
            self.app.label_status['text'] = "Заполнение списка..."
            self.app._root.after(0, self.fill_listbox)
            self.draw_matrix(primitive)
            self.app.button_find_field['state'] = 'normal'
            self.app.button_use_another_primitive['state'] = 'normal'

    def fill_listbox(self):
        self.app.listbox_field_elements.delete(0, tk.END)
        self.app.listbox_field_elements.insert("end", *[f"A^{i+1} = {self.__elements[i]}" for i in range(0, min(1000, len(self.__elements)))])
        self.app.progressbar['value'] = 100
        self.app.label_status['text'] = "Поле построено!"

    def draw_matrix(self, array: np.ndarray, title: str = "A^1 ="):
        if hasattr(self, "_current_canvas") and self._current_canvas is not None:
            self._current_canvas.destroy()

        rows, cols = array.shape
        cell_size = 25

        canvas_width = cols * cell_size + 40
        canvas_height = rows * cell_size + 40

        self._current_canvas = tk.Canvas(self.app._root, width=canvas_width, height=canvas_height)
        self._current_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self._current_canvas.create_text(20, 20, text=title, font=("Arial", 12, "bold"), anchor="nw")

        top_offset = 40
        for i in range(rows):
            y_top = i * cell_size + top_offset + 5
            y_bottom = (i + 1) * cell_size + top_offset - 5

            self._current_canvas.create_line(10, y_top, 10, y_bottom, width=2)
            if i == 0:
                self._current_canvas.create_line(10, y_top, 20, y_top, width=2)
            if i == rows - 1:
                self._current_canvas.create_line(10, y_bottom, 20, y_bottom, width=2)
            x_right = canvas_width - 10
            self._current_canvas.create_line(x_right, y_top, x_right, y_bottom, width=2)
            if i == 0:
                self._current_canvas.create_line(x_right - 10, y_top, x_right, y_top, width=2)
            if i == rows - 1:
                self._current_canvas.create_line(x_right - 10, y_bottom, x_right, y_bottom,
                                                 width=2)

        for i in range(rows):
            for j in range(cols):
                x = j * cell_size + 30
                y = i * cell_size + top_offset + cell_size // 2
                self._current_canvas.create_text(x, y, text=str(array[i, j]), font=("Arial", 10), fill="black")

        self._current_canvas = self._current_canvas

    def __change_lang_to_russian(self):
        self.app.label_field_size['text'] = 'Размер поля'
        self.app.button_find_field['text'] = 'Найти'
        self.app.button_use_another_primitive['text'] = 'Использовать другой\nпримитивный элемент'