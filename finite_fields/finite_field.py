import numpy as np

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
        self.__built_matrices = []
        self.__primitive_matrix = primitive_matrix

    def __build(self):
        logger.info("Building field...")
        if len(self.__built_matrices) > 0:
            logger.info("Building is cached!")
            return self.__built_matrices
        current = self.__primitive_matrix.copy()
        second_part = [current]
        for i in range(self.__p**self.__n - 1 - self.__n):
            current = (np.dot(current, self.__primitive_matrix)) % self.__p
            second_part.append(current)
        first_part = []
        for i in range(self.__n - 1):
            current = (np.dot(current, self.__primitive_matrix)) % self.__p
            first_part.append(current)
        self.__built_matrices = first_part + second_part
        logger.info("Built the field")
        return self.__built_matrices

    def get_elements(self, view: str = 'matrix'):
        """
        Method for obtaining elements of the finite field in matrix or vector form.
        :param view: 'matrix' | 'vector'.
        :return: list of np.ndarray that represents elements of the finite field.
        """
        if view == 'matrix':
            return self.__build()
        if view == 'vector':
            elements = self.__build()
            vectors = []
            for element in elements:
                vectors.append(self.__reverse_last_column(element))
            return vectors

    @staticmethod
    def __reverse_last_column(matrix):
        if not isinstance(matrix, np.ndarray):
            raise ValueError("Input must be a numpy array.")
        if matrix.ndim != 2:
            raise ValueError("Input must be a 2D matrix.")
        return matrix[:, -1][::-1]