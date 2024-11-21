from sympy import symbols, sympify, expand, lambdify, isprime

from primitive_element_finders.primitive_pow_functions import AbstractPrimitivePowFunctions
from utils.logger import logger


class DumbPrimitivePowFunctions(AbstractPrimitivePowFunctions):

    def __init__(self, n, p):
        if not isprime(n):
            raise ValueError("n must be a prime number")
        self.n = n
        self.p = p
        self.__symbols = self.__generate_symbols()
        self.__base_function = self.__generate_base_function()
        self.__functions = None

    def get_functions(self):
        if self.__functions is None:
            self.__functions = []
            self.__generate_functions()
        return self.__functions

    def __generate_functions(self):
        logger.info("Generating functions for finding coefficients in primitive element...")
        i = self.n ** self.p
        func = self.__base_function
        symbs = list(self.__symbols.values())[1:]
        for j in range(i - 1):
            func = self.__pow_function(func)

            def result_function(*args, function=func):
                lamb = lambdify(symbs, function, "numpy", dummify=True)
                results = []
                for coef, var in lamb(*args).as_coefficients_dict().items():
                    results.append(var % self.n)
                results.reverse()
                return results

            self.__functions.append(result_function)
        self.__functions = self.__functions[-self.p:] + self.__functions[:-self.p]
        logger.info("Functions generated.")

    def __pow_function(self, func):
        func *= self.__symbols["A"]
        func = expand(func)
        func = func.subs(self.__symbols["A"] ** self.p, self.__base_function)
        func = expand(func)
        func = sum((coef % self.n) * var for var, coef in func.as_coefficients_dict().items())
        return func

    def __generate_base_function(self):
        func = sympify("".join(f"a{i}*A**{self.p - i}+" for i in range(1, self.p + 1))[0:-1])
        return func

    def __generate_symbols(self):
        syms: tuple = symbols("A " + " ".join(f"a{i} " for i in range(1, self.p + 1)))
        symbols_dict = {}
        for sym in syms:
            symbols_dict[str(sym)] = sym
        return symbols_dict
