import galois
import numpy as np

from primitive_element_finders.abstract_primitive_finder import AbstractPrimitiveFinder
from utils.logger import logger


class FastPrimitiveFinder(AbstractPrimitiveFinder):
    """
    A class for finding primitive elements in finite fields.

    Primitive elements are determined using galois library.
    Primitive elements have form of a companion matrix of a corresponding primitive polynomial.
    After finding primitive elements, they are cached.

    Methods:
    -------
    find_any_primitive():
        Finds and returns any single primitive element.
    find_all_primitives():
        Finds and returns all primitive elements.
    """
    def __init__(self, p, n):
        self.__p = p
        self.__n = n
        self.__cached_primitive: np.ndarray = None
        self.__cached_primitives: list[np.ndarray] = None

    def find_any(self):
        """
        Finds and returns single primitive element. After finding,
        it is cached and can be obtained by calling this method again.
        :return: primitive element of type np.ndarray
        """
        logger.info("Finding primitive element...")
        if self.__cached_primitive is not None:
            logger.info("Primitive element is cached!")
            return self.__cached_primitive
        poly = galois.primitive_poly(self.__p, self.__n)
        A = self.__get_companion_matrix(poly.coefficients())
        self.__cached_primitive = A
        logger.info("Found primitive element.")
        return A

    def find_all(self):
        """
        Finds and returns a list of every primitive element. After finding,
        they are cached and can be obtained by calling this method again.
        :return: list of primitive elements of type np.ndarray
        """
        logger.info("Finding primitive elements...")
        if self.__cached_primitives is not None:
            logger.info("Primitive elements are cached!")
            return self.__cached_primitives
        self.__cached_primitives = []
        for poly in galois.primitive_polys(self.__p, self.__n):
            if self.__cached_primitive is None:
                self.__cached_primitive = self.__get_companion_matrix(poly.coefficients())
            self.__cached_primitives.append(self.__get_companion_matrix(poly.coefficients()))
        logger.info("Found all primitive elements.")
        return self.__cached_primitives

    def __get_companion_matrix(self, coefficients):
        n = len(coefficients) - 1
        coeffs = list((-np.int32(c)) % self.__p for c in coefficients)
        coeffs.reverse()
        A = np.zeros((n, n), dtype=np.int32)
        A[1:, :-1] = np.eye(n - 1)
        A[:, -1] = np.array(coeffs[:-1])
        return A