import math
from xmlrpc.client import Error
import threading

import tkinter as tk

import numpy as np
from PIL import ImageTk, Image
from formation import AppBuilder
from tkinter import messagebox

from finite_fields.finite_field import FiniteField
from primitive_element_finders.fast_primitive_finder import FastPrimitiveFinder
from utils.is_prime import is_prime_power


class FiniteFieldsApp:
    def __init__(self):
        self.primitive = None
        self.app = AppBuilder(path='resources/finite_fields_app_formation.xml')
        self.__primitive_finder = None
        self.__finite_field = None
        self.__elements = None
        self.init_app()

    def run(self):
        self.app.mainloop()

    def init_app(self):
        scrollbar = tk.Scrollbar(self.app._root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.app.listbox_field_elements.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.app.listbox_field_elements.yview)
        self.app.progressbar['value'] = 0
        self.app.button_find_field['command'] = self.press_find_button

    def press_find_button(self):
        self.app.progressbar['value'] = 0
        threading.Thread(target=self.find_field, daemon=True).start()

    def find_field(self):
        try:
            text: str = self.app.entry_field_size.get()
            if '^' in text:
                num = int(text.split('^')[0]) ** int(text.split('^')[1])
            else:
                num = int(text)
        except Error:
            messagebox.showerror("Ошибка", "Введите в поле степень простого числа")
            return

        p = is_prime_power(num)
        if p == -1:
            messagebox.showerror("Ошибка", f"{num} - это не степень простого числа")
            return
        self.app.button_find_field['state'] = 'disabled'
        self.app.progressbar['value'] = 0
        p, k = int(p), int(math.log(num, p))
        self.__primitive_finder = FastPrimitiveFinder(p, k)
        self.app.label_status['text'] = "Поиск примитивного элемента..."
        primitive = self.__primitive_finder.find_any()
        self.app.progressbar['value'] = 20
        self.__finite_field = FiniteField(p, k, primitive)
        self.app.label_status['text'] = "Построение конечного поля..."
        self.__elements = self.__finite_field.get_elements(view='vector', progressbar=self.app.progressbar)
        self.app.progressbar['value'] = 90
        self.app.label_status['text'] = "Заполнение списка..."
        self.app._root.after(0, self.fill_listbox)
        self.draw_matrix(primitive)
        self.app.button_find_field['state'] = 'normal'

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

        # Отрисовка заголовка
        self._current_canvas.create_text(20, 20, text=title, font=("Arial", 12, "bold"), anchor="nw")

        # Отрисовка скобок
        bracket_width = 10  # Ширина скобок
        top_offset = 40  # Отступ сверху для заголовка
        for i in range(rows):
            y_top = i * cell_size + top_offset + 5  # Верхний край ячейки
            y_bottom = (i + 1) * cell_size + top_offset - 5  # Нижний край ячейки

            # Левая скобка
            self._current_canvas.create_line(10, y_top, 10, y_bottom, width=2)  # Вертикальная линия
            if i == 0:
                self._current_canvas.create_line(10, y_top, 20, y_top, width=2)  # Верхняя горизонтальная
            if i == rows - 1:
                self._current_canvas.create_line(10, y_bottom, 20, y_bottom, width=2)  # Нижняя горизонтальная

            # Правая скобка
            x_right = canvas_width - 10
            self._current_canvas.create_line(x_right, y_top, x_right, y_bottom, width=2)  # Вертикальная линия
            if i == 0:
                self._current_canvas.create_line(x_right - 10, y_top, x_right, y_top, width=2)  # Верхняя горизонтальная
            if i == rows - 1:
                self._current_canvas.create_line(x_right - 10, y_bottom, x_right, y_bottom,
                                                 width=2)  # Нижняя горизонтальная

        # Отрисовка чисел
        for i in range(rows):
            for j in range(cols):
                x = j * cell_size + 30  # Центр ячейки по X (учитываем отступ для левой скобки)
                y = i * cell_size + top_offset + cell_size // 2  # Центр ячейки по Y
                self._current_canvas.create_text(x, y, text=str(array[i, j]), font=("Arial", 10), fill="black")

        # Сохраняем ссылку на текущий Canvas
        self._current_canvas = self._current_canvas