import time

from physities.src.dimension import Dimension
from vision1 import OperationType


class MetaT(type):
    @staticmethod
    def neutral_conversion(x):
        return x

    value: float = None
    from_default: callable = neutral_conversion
    to_default: callable = neutral_conversion
    dimension: Dimension

    def __call__(cls, *args, **kwargs):
        # This method creates an instance of the dynamically generated class
        instance = cls.__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance

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

    def __operate_scalar(self, other: int | float, operation_type: OperationType):
        operations = {
            OperationType.ADDITION: self.__add,
            OperationType.SUBTRACTION: self.__sub,
            OperationType.MULTIPLICATION: self.__mul,
            OperationType.DIVISION: self.__div,
        }
        operations_reverse = {
            OperationType.ADDITION: self.__sub,
            OperationType.SUBTRACTION: self.__add,
            OperationType.MULTIPLICATION: self.__div,
            OperationType.DIVISION: self.__mul,
        }
        self.from_default = self.__compose_function(
            inner_func=self.from_default,
            outer_func=lambda x: operations[operation_type](x, other),
        )
        self.to_default = self.__compose_function(
            inner_func=self.to_default,
            outer_func=lambda x: operations_reverse[operation_type](x, other),
        )

    # def __add__(self, other):
    #     if self.value is None:
    #         raise TypeError("Can't create shifted scales")
    #     return type(self)(self.__name__)
    #
    # def __sub__(self, other):
    #     if self.value is None:
    #         raise TypeError("Can't create shifted scales")
    #     return type(self)(self.__name__)

    def __mul__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                self.__operate_scalar(
                    other=other, operation_type=OperationType.MULTIPLICATION
                )
                result_attrs = {
                    "dimension": self.dimension,
                    "from_default": self.from_default,
                    "to_default": self.to_default,
                    "value": None,
                }
                return type(self)(self.__name__, (T,), result_attrs)
            if isinstance(other, type(self)) or issubclass(other, type(self)):
                dimension = self.dimension + other.dimension
                result_attrs = {
                    "dimension": dimension,
                    "from_default": self.from_default,
                    "to_default": self.to_default,
                    "value": None,
                }
                return type(self)(self.__name__, (T,), result_attrs)
        # else:

    def lala(self, x):
        r = time.time()
        a = self.neutral_conversion
        for i in range(500):
            a = self.__compose_function(a, self.neutral_conversion)
        b = time.time()
        print(f"tempo para fazer {b-r}")
        c = time.time()
        self.neutral_conversion(5)
        d = time.time()
        a(x)
        e = time.time()
        print(f"1: {d-c}, 2: {e-d}, diff: {(e-d) - (d-c)}")

    # def __truediv__(self, other):
    #     if self.value is None:
    #         if isinstance(other, (int, float)):
    #             self.xxx(other=other, operation_type=OperationType.DIVISION)
    #     return self
    #
    # def __pow__(self, power, modulo=None):
    #     if self.value is None:
    #         if isinstance(power, (int, float)):
    #             self.xxx(other=power, operation_type=OperationType.POWER)
    #     return self
    #
    # def __radd__(self, other):
    #     self.__add__(other=other)
    #
    # def __rsub__(self, other):
    #     self.__sub__(other=other)

    def __rmul__(self, other):
        self.__mul__(other=other)

    # def __rtruediv__(self, other):
    #     self.__truediv__(other=other)
    #
    # def __rpow__(self, other):
    #     raise TypeError("A dimensional value can't be the power of a exponentiation")


class T(metaclass=MetaT):
    dimension: Dimension = Dimension.new_length(power=1)
    value = None

    def __init__(self, value):
        self.value = value


class J(metaclass=MetaT):
    dimension: Dimension = Dimension.new_time(power=1)
    value = None

    def __init__(self, value):
        self.value = value


if __name__ == "__main__":
    print(T.from_default(2))
    H = T * J
    print(H.from_default(2))
    d = H * 2
    print(d.from_default(2))
    c = d(10)
    # T + 5
    # print(T.from_default(2))
    # T * 2
    print()
