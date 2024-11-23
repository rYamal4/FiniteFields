import unittest

from primitive_element_finders.dumb_primitive_pow_functions import DumbPrimitivePowFunctions
from wrappers.disable_logging import disable_logging


class TestDumbPrimitivePowFunctions(unittest.TestCase):

    @disable_logging
    def test_raises_exception_if_n_not_prime(self):
        with self.assertRaises(ValueError):
            DumbPrimitivePowFunctions(6, 2)

    @disable_logging
    def test_get_functions_with_n_3_and_p_2(self):
        coefficients = [[1, 0], [1, 1], [2, 1], [0, 2], [2, 0], [2, 2], [1, 2], [0, 1]]
        a1, a2 = 1, 1

        functions = DumbPrimitivePowFunctions(3, 2).get()

        for function, coefficient in zip(functions, coefficients):
            self.assertEqual(coefficient, function(a1, a2))

    @disable_logging
    def test_get_functions_with_n_2_and_p_3(self):
        coefficients = [[1, 0], [1, 1], [0, 1], [0, 1], [0, 1], [1, 1], [1, 0]]
        a1, a2, a3 = 1, 1, 0

        functions = DumbPrimitivePowFunctions(2, 3).get()

        for function, coefficient in zip(functions, coefficients):
            self.assertEqual(coefficient, function(a1, a2, a3))

    @disable_logging
    def test_get_functions_with_n_3_and_p_3(self):
        coefficients = [[2, 1], [2, 2], [0, 2], [2, 2], [0, 2], [2, 0], [1, 2], [1, 1], [0, 1], [1, 0], [2, 1],
                        [2, 2], [0, 2], [2, 0], [1, 2], [1, 1], [0, 1], [1, 0], [2, 1], [2, 2], [0, 2], [2, 0],
                        [1, 2], [1, 1], [0, 1]]
        a1, a2, a3 = 2, 1, 0

        functions = DumbPrimitivePowFunctions(3, 3).get()

        for function, coefficient in zip(functions, coefficients):
            self.assertEqual(coefficient, function(a1, a2, a3))
