from dataclasses import dataclass
from enum import IntEnum

from physities.src.entities.dimension import Dimension


class OperationType(IntEnum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    POWER = 5


class T(type):
    value = None
    dimension = Dimension
    from_default = None
    to_default = None

    @staticmethod
    def __compose_function(inner_func, outer_func):
        return lambda x: outer_func(inner_func(x))

    @staticmethod
    def __add(x, y):
        return x + y

    @staticmethod
    def __sub(x, y):
        return x - y

    @staticmethod
    def __mul(x, y):
        return x * y

    @staticmethod
    def __div(x, y):
        return x / y

    @staticmethod
    def __pow(x, y):
        return x**y

    def xxx(self, other: int | float, operation_type: OperationType):
        operations = {
            OperationType.ADDITION: T.__add,
            OperationType.SUBTRACTION: T.__sub,
            OperationType.MULTIPLICATION: T.__mul,
            OperationType.DIVISION: T.__div,
            OperationType.POWER: T.__pow,
        }
        if self.from_default and self.to_default:
            self.from_default = self.__compose_function(
                inner_func=self.from_default,
                outer_func=lambda x: operations[operation_type](x, other),
            )
        else:
            self.from_default = lambda x: operations[operation_type](x, other)

    def __add__(self, other):
        if self.value is None:
            raise TypeError
        return type(self)(self.__name__)

    def __radd__(self, other):
        self.__add__(other=other)

    def __sub__(self, other):
        if self.value is None:
            raise TypeError
        return type(self)(self.__name__)

    def __rsub__(self, other):
        self.__sub__(other=other)

    def __mul__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                self.xxx(other=other, operation_type=OperationType.MULTIPLICATION)
        return self

    def __rmul__(self, other):
        self.__mul__(other=other)

    def __truediv__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                self.xxx(other=other, operation_type=OperationType.DIVISION)
        return self

    def __rmul__(self, other):
        self.__mul__(other=other)

    def __pow__(self, power, modulo=None):
        if self.value is None:
            if isinstance(power, (int, float)):
                self.xxx(other=power, operation_type=OperationType.POWER)
        return self

    def __rpow__(self, other):
        raise TypeError


if __name__ == "__main__":

    class A(metaclass=T):
        pass

    H = A * 3
    print(A.from_default(2))
    d = H * 3
    print(d.from_default(2))
    # A + 5
    print(A.from_default(2))
    # A * 2
    print(A.from_default(2))
    print()
