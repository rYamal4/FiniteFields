from itertools import product

from custom_collections.list_set import ListSet
from primitive_element_finders.primitive_pow_functions import AbstractPrimitivePowFunctions
from utils.logger import logger


class DumbPrimitiveElementFinder:
    def __init__(self,
                 n: int,
                 p: int,
                 primitive_pow_funcs: AbstractPrimitivePowFunctions):
        self.__n = n
        self.__p = p
        self.__functions = primitive_pow_funcs
        self.__cached_primitives = ListSet()
        self.__primitive_pow_zero = self.__get_primitive_pow_zero()
        self.__is_found_all_primitives = False

    def find_any_primitive(self):
        if len(self.__cached_primitives) > 0:
            return self.__cached_primitives[0]
        logger.info("Finding single primitive element...")
        for args_list in product(range(self.__n), repeat=self.__p):
            if self.__functions.get()[-1](*args_list) == self.__primitive_pow_zero:
                flag = True
                for function in self.__functions.get()[:-1]:
                    if function(*args_list) == self.__primitive_pow_zero:
                        flag = False
                        break
                if flag:
                    self.__cached_primitives.append(args_list)
                    return args_list


    def find_all_primitives(self):
        if self.__is_found_all_primitives:
            return self.__cached_primitives
        logger.info("Finding all primitive elements...")
        for args_list in product(range(self.__n), repeat=self.__p):
            if args_list in self.__cached_primitives:
                continue
            if self.__functions.get()[-1](*args_list) == self.__primitive_pow_zero:
                flag = True
                for function in self.__functions.get()[:-1]:
                    if function(*args_list) == self.__primitive_pow_zero:
                        flag = False
                        break
                if flag:
                    self.__cached_primitives.append(args_list)
        self.__is_found_all_primitives = True
        return self.__cached_primitives

    def __get_primitive_pow_zero(self):
        a = [0] * self.__p
        a[-1] = 1
        return a