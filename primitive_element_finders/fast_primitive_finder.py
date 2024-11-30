import galois
import numpy as np

from custom_collections.list_set import ListSet
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
    find_first():
        Finds and returns first primitive element.
    find_next():
        Finds and returns next primitive element
    find_all():
        Finds and returns all primitive elements.
    """
    def __init__(self, p, n):
        self.__p = p
        self.__n = n
        self.__primitive_iterator = galois.primitive_polys(p, n)
        self.__not_primitives: ListSet[np.ndarray] = ListSet()
        self.__cached_primitives: ListSet[np.ndarray] = ListSet()
        self.__primitive_counter = 0

    def find_first(self):
        """
        Finds and returns first primitive element. After finding,
        it is cached and can be obtained by calling this method again.
        :return: primitive element of type np.ndarray
        """
        if len(self.__cached_primitives) > 0:
            logger.info("First primitive element is cached!")
            return self.__cached_primitives[0]
        logger.info("Finding primitive element...")
        poly = next(self.__primitive_iterator)
        A = self.__get_companion_matrix(poly.coefficients())
        self.__cached_primitives.add(A)
        logger.info("Found primitive element.")
        logger.info(f"Found {len(self.__cached_primitives)} primitives.")
        return A

    def find_next(self):
        logger.info("Finding next primitive element...")
        try:
            poly = next(self.__primitive_iterator)
            self.__cached_primitives.add(self.__get_companion_matrix(poly.coefficients()))
            logger.info("Found next primitive element...")
            logger.info(f"Found {len(self.__cached_primitives)} primitives.")
            return self.__cached_primitives[-1]
        except StopIteration:
            self.__primitive_counter = self.__primitive_counter % len(self.__cached_primitives)
            logger.info(f"Already found all primitives, returning {self.__primitive_counter} element")
            primitive = self.__cached_primitives[self.__primitive_counter]
            self.__primitive_counter += 1
            return primitive

    def find_all(self):
        """
        Finds and returns a list of every primitive element. After finding,
        they are cached and can be obtained by calling this method again.
        :return: list of primitive elements of type np.ndarray
        """
        logger.info("Finding primitive elements...")
        for poly in self.__primitive_iterator:
            try:
                self.__cached_primitives.add(self.__get_companion_matrix(poly.coefficients()))
            except StopIteration:
                logger.info("Primitive elements are cached!")
                return self.__cached_primitives
        logger.info(f"Found all {len(self.__cached_primitives)} primitive elements.")
        return self.__cached_primitives

    def __get_companion_matrix(self, coefficients):
        n = len(coefficients) - 1
        coeffs = list((-np.int32(c)) % self.__p for c in coefficients)
        coeffs.reverse()
        A = np.zeros((n, n), dtype=np.int32)
        A[1:, :-1] = np.eye(n - 1)
        A[:, -1] = np.array(coeffs[:-1])
        return A