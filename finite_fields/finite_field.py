import numpy as np

from custom_collections.list_set import ListSet
from utils.logger import logger


class FiniteField:
    """
    Class for building finite field of size p^n with given p, n and Galois matrix.
    Galois matrix is the companion matrix of a primitive polynomial mod p.

    You can obtain elements of the field using get_elements() method in matrix or vector form.
    After obtaining elements in first time, this then object caches them.
    """
    def __init__(self, p, n, primitive_matrix: np.ndarray):
        self.__p = p
        self.__n = n
        self.__built_matrices: ListSet[np.ndarray] = ListSet()
        self.__primitive_matrix = primitive_matrix

    def __build(self, progressbar=None):
        logger.info("Building field...")
        if len(self.__built_matrices) == self.__p**self.__n - 1:
            logger.info("Building is cached!")
            return self.__built_matrices
        elif len(self.__built_matrices) > 0:
            logger.info("Not every element was found for some reason.")
            raise ValueError(f"Invalid state: only {len(self.__built_matrices)} "
                             f"out of {self.__p**self.__n - 1} was found!")

        current = self.__primitive_matrix.copy()
        self.__built_matrices.add(current)
        progress = 20
        for i in range(self.__p**self.__n - 2):
            current = (np.dot(current, self.__primitive_matrix)) % self.__p
            self.__built_matrices.add(current)
            if progressbar is not None and progress != 20 + int((i / (self.__p ** self.__n - 1)) * 70):
                progress = 20 + int((i / (self.__p ** self.__n - 1)) * 70)
                progressbar['value'] = progress

        logger.info("Field successfully built.")
        return self.__built_matrices

    def get_elements(self, view: str = 'matrix', progressbar=None):
        """
        Method for obtaining elements of the finite field in matrix or vector form.
        :param progressbar:
        :param view: 'matrix' | 'vector'.
        :return: list of np.ndarray that represents elements of the finite field.
        """
        if view == 'matrix':
            return self.__build(progressbar)
        if view == 'vector':
            elements = self.__build(progressbar)
            vectors = []
            for element in elements:
                vectors.append(self.__reverse_first_column(element))
            return vectors

    @staticmethod
    def __reverse_first_column(matrix):
        if not isinstance(matrix, np.ndarray):
            raise ValueError("Input must be a numpy array.")
        if matrix.ndim != 2:
            print(matrix)
            raise ValueError("Input must be a 2D matrix.")
        return matrix[:, 0][::-1]