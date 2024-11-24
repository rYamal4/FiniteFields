from itertools import product

from custom_collections.list_set import ListSet
from primitive_element_finders.abstract_primitive_finder import AbstractPrimitiveFinder
from primitive_element_finders.dumb_primitive_pow_functions import DumbPrimitivePowFunctions
from utils.logger import logger


class DumbPrimitiveElementFinder(AbstractPrimitiveFinder):
    """
    A class to find primitive elements in finite fields.

    Primitive elements are determined using provided object of a
    AbstractPrimitivePowerFunctions class. The class supports finding
    either a single primitive element or all primitive elements.
    After finding primitive elements, they are cached.

    Methods:
    -------
    find_any_primitive():
        Finds and returns any single primitive element.
    find_all_primitives():
        Finds and returns all primitive elements.
    """

    def __init__(self, p: int, n: int,):
        self.__p = p
        self.__n = n
        self.__functions = DumbPrimitivePowFunctions(p, n)
        self.__cached_primitives = ListSet()
        self.__primitive_pow_zero = self.__get_primitive_pow_zero()
        self.__is_found_all_primitives = False

    def find_any(self):
        if len(self.__cached_primitives) > 0:
            return self.__cached_primitives[0]
        logger.info("Finding single primitive element...")
        for args_list in product(range(self.__p), repeat=self.__n):
            if self.__functions.get()[-1](*args_list) == self.__primitive_pow_zero:
                flag = True
                for function in self.__functions.get()[:-1]:
                    if function(*args_list) == self.__primitive_pow_zero:
                        flag = False
                        break
                if flag:
                    primitive = self.__create_shifted_matrix(args_list)
                    self.__cached_primitives.append(primitive)
                    return primitive

    def find_all(self):
        if self.__is_found_all_primitives:
            return self.__cached_primitives
        logger.info("Finding all primitive elements...")
        for args_list in product(range(self.__p), repeat=self.__n):
            if self.__create_shifted_matrix(args_list) in self.__cached_primitives:
                continue
            if self.__functions.get()[-1](*args_list) == self.__primitive_pow_zero:
                flag = True
                for function in self.__functions.get()[:-1]:
                    if function(*args_list) == self.__primitive_pow_zero:
                        flag = False
                        break
                if flag:
                    self.__cached_primitives.append(self.__create_shifted_matrix(args_list))
        self.__is_found_all_primitives = True
        return self.__cached_primitives

    def __get_primitive_pow_zero(self):
        a = [0] * self.__n
        a[-1] = 1
        return a

    @staticmethod
    def __create_shifted_matrix(values):
        size = len(values)
        identity_matrix = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        shifted_matrix = [row[1:] + [row[0]] for row in identity_matrix]
        for i in range(size):
            shifted_matrix[i][-1] = values[size - 1 - i]
        return tuple(tuple(row) for row in shifted_matrix)
