import math
from xmlrpc.client import Error
import threading

import tkinter as tk
from formation import AppBuilder
from tkinter import messagebox

from finite_fields.finite_field import FiniteField
from primitive_element_finders.fast_primitive_finder import FastPrimitiveFinder
from utils.is_prime import is_prime_power


class FiniteFieldsApp:
    def __init__(self):
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

    def fill_listbox(self):
        self.app.listbox_field_elements.delete(0, tk.END)
        self.app.listbox_field_elements.insert("end", *[f"A^{i+1} = {self.__elements[i]}" for i in range(0, min(1000, len(self.__elements)))])
        self.app.progressbar['value'] = 100
        self.app.label_status['text'] = "Поле построено!"