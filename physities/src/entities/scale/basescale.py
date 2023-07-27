from dataclasses import dataclass
from enum import IntEnum
from typing import Self

from physities.src.entities.dimension import Dimension
from physities.src.enums.base_units import BaseUnit
from physities.src.enums.length import LengthType
from physities.src.enums.mass import MassType
from physities.src.enums.quantity import AmountType
from physities.src.enums.temperature import TemperatureType
from physities.src.enums.time import TimeType


default_scale = {
    BaseUnit.LENGTH: LengthType.METER,
    BaseUnit.MASS: MassType.KILOGRAM,
    BaseUnit.TEMPERATURE: TemperatureType.KELVIN,
    BaseUnit.TIME: TimeType.SECONDS,
    BaseUnit.AMOUNT: AmountType.UNITS,
}


class BaseScale(type):
    dimension: Dimension = None
    value: float = None
    resize: float = 1
    conversion_tuple: tuple[
        dict[str:float, str:float],
        dict[str:float, str:float],
        dict[str:float, str:float],
        dict[str:float, str:float],
        dict[str:float, str:float],
    ] = tuple({"from_base": 1, "to_base": 1} for i in BaseUnit)

    def __call__(cls, value, dimension, conversion_tuple, resize):
        # This method creates an instance of the dynamically generated class
        instance = Scale.__new__(Scale)
        instance.__init__(
            dimension=dimension,
            conversion_tuple=conversion_tuple,
            resize=resize,
            value=value,
        )
        return instance

    @classmethod
    def new(cls, value):
        instance = cls.__call__(
            cls,
            dimension=cls.dimension,
            conversion_tuple=cls.conversion_tuple,
            resize=cls.resize,
            value=value,
        )
        return instance

    @staticmethod
    def __form_result_attrs(dimension, conversion_tuple, resize):
        return {
            "dimension": dimension,
            "conversion_tuple": conversion_tuple,
            "resize": resize,
            "value": None,
        }

    def __mul__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                dimensions = self.dimension.get_dimensions()
                if len(dimensions) == 1:
                    index = dimensions.pop().value
                    new_conversion = self.__tuple_number_conversion_operation(
                        tuple_var=self.conversion_tuple,
                        number=other,
                        to_base_callable=lambda t, n: t / n,
                        from_base_callable=lambda t, n: t * n,
                        index=index,
                    )
                    result_attrs = self.__form_result_attrs(
                        dimension=self.dimension,
                        conversion_tuple=new_conversion,
                        resize=self.resize,
                    )
                    return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

                result_attrs = self.__form_result_attrs(
                    dimension=self.dimension,
                    conversion_tuple=self.conversion_tuple,
                    resize=self.resize * other,
                )
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

            elif isinstance(other, type(self)) or issubclass(other, type(self)):
                new_conversion = self.__tuple_tuple_conversion_operation(
                    self.conversion_tuple,
                    other.conversion_tuple,
                    from_base_callable=lambda s, o: s * o,
                    to_base_callable=lambda s, o: s * o,
                )
                result_attrs = self.__form_result_attrs(
                    dimension=self.dimension + other.dimension,
                    conversion_tuple=new_conversion,
                    resize=self.resize * other.resize,
                )
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

            else:
                raise TypeError

    def __rmul__(self, other):
        try:
            to_return = BaseScale.__mul__(self, other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                dimensions = self.dimension.get_dimensions()
                if len(dimensions) == 1:
                    index = dimensions.pop().value
                    new_conversion = self.__tuple_number_conversion_operation(
                        tuple_var=self.conversion_tuple,
                        number=other,
                        to_base_callable=lambda t, n: t * n,
                        from_base_callable=lambda t, n: t / n,
                        index=index,
                    )
                    result_attrs = self.__form_result_attrs(
                        dimension=self.dimension,
                        conversion_tuple=new_conversion,
                        resize=self.resize,
                    )
                    return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

                result_attrs = self.__form_result_attrs(
                    dimension=self.dimension,
                    conversion_tuple=self.conversion_tuple,
                    resize=self.resize / other,
                )
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
            elif isinstance(other, type(self)) or issubclass(other, type(self)):
                new_conversion = self.__tuple_tuple_conversion_operation(
                    self.conversion_tuple,
                    other.conversion_tuple,
                    from_base_callable=lambda s, o: s / o,
                    to_base_callable=lambda s, o: s / o,
                )
                result_attrs = self.__form_result_attrs(
                    dimension=self.dimension - other.dimension,
                    conversion_tuple=new_conversion,
                    resize=self.resize / other.resize,
                )
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
            else:
                raise TypeError

    def __rtruediv__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                dimensions = self.dimension.get_dimensions()
                dimension = self.dimension * -1
                if len(dimensions) == 1:
                    index = dimensions.pop().value
                    new_conversion = self.__tuple_number_conversion_operation(
                        tuple_var=self.conversion_tuple,
                        number=other,
                        from_base_callable=lambda t, n: t / n,
                        to_base_callable=lambda t, n: n / t,
                        index=index,
                    )
                    result_attrs = self.__form_result_attrs(
                        dimension=dimension,
                        conversion_tuple=new_conversion,
                        resize=self.resize,
                    )
                    return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

                new_conversion = self.__tuple_number_conversion_operation(
                    tuple_var=self.conversion_tuple,
                    number=1,
                    from_base_callable=lambda t, n: n / t,
                    to_base_callable=lambda t, n: n / t,
                )
                result_attrs = self.__form_result_attrs(
                    dimension=dimension,
                    conversion_tuple=new_conversion,
                    resize=other / self.resize,
                )
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
        else:
            raise TypeError

    @staticmethod
    def __tuple_tuple_conversion_operation(
        tuple_1, tuple_2, from_base_callable, to_base_callable
    ):
        return tuple(
            {
                "from_base": from_base_callable(
                    tuple_1[base_unit_index].get("from_base"),
                    tuple_2[base_unit_index].get("from_base"),
                ),
                "to_base": to_base_callable(
                    tuple_1[base_unit_index].get("to_base"),
                    tuple_2[base_unit_index].get("to_base"),
                ),
            }
            for base_unit_index in BaseUnit
        )

    @staticmethod
    def __tuple_number_conversion_operation(
        tuple_var, number, from_base_callable, to_base_callable, index=None
    ):
        if index is None:
            return tuple(
                {
                    "from_base": from_base_callable(
                        tuple_var[base_unit_index].get("from_base"), number
                    ),
                    "to_base": to_base_callable(
                        tuple_var[base_unit_index].get("to_base"), number
                    ),
                }
                for base_unit_index in BaseUnit
            )

        new_conversion = list(tuple_var)
        new_conversion[index] = {
            "from_base": from_base_callable(tuple_var[index].get("from_base"), number),
            "to_base": to_base_callable(tuple_var[index].get("to_base"), number),
        }
        return tuple(new_conversion)

    def __pow__(self, power, modulo=None):
        if not isinstance(power, (int, float)):
            raise TypeError("Can only exponentiate int's and float's")
        new_conversion = self.__tuple_number_conversion_operation(
            tuple_var=self.conversion_tuple,
            number=power,
            from_base_callable=lambda t, n: t**n,
            to_base_callable=lambda t, n: t**n,
        )
        result_attrs = self.__form_result_attrs(
            dimension=self.dimension * power,
            conversion_tuple=new_conversion,
            resize=self.resize**power,
        )
        return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

    def __add__(self, other):
        raise TypeError("Scales offset are not allowed yet.")

    def __sub__(self, other):
        raise TypeError("Scales offset are not allowed yet.")

    def __radd__(self, other):
        raise TypeError("Scales offset are not allowed yet.")

    def __rsub__(self, other):
        raise TypeError("Scales offset are not allowed yet.")

    def __rpow__(self, other):
        raise TypeError("A dimensional thing be a exponent.")


class Scale(metaclass=BaseScale):
    dimension: Dimension
    conversion_tuple: tuple
    resize: float
    value: float = None

    def __init__(self, dimension, conversion_tuple, resize, value):
        self.dimension = dimension
        self.conversion_tuple = conversion_tuple
        self.resize = resize
        self.value = value

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            value = self.value * other
            return type(self)(
                dimension=self.dimension,
                conversion_tuple=self.conversion_tuple,
                resize=self.resize,
                value=value,
            )
        if isinstance(other, type(self)) or issubclass(other, type(self)):
            dimension = self.dimension + other.dimension
            resize = self.resize * other.resize
            conversion_tuple = tuple(
                {
                    "from_base": self.conversion_tuple[base_unit_index].get("from_base")
                    * other.conversion_tuple[base_unit_index].get("from_base"),
                    "to_base": self.conversion_tuple[base_unit_index].get("to_base")
                    * other.conversion_tuple[base_unit_index].get("to_base"),
                }
                for base_unit_index in BaseUnit
            )
            value = self.value * other.value
            return type(self)(
                dimension=dimension,
                conversion_tuple=conversion_tuple,
                resize=resize,
                value=value,
            )
        raise TypeError(f"Operation between {type(self)} and {type(other)} not allowed")

    def __rmul__(self, other):
        try:
            to_return = self.__mul__(other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            value = self.value / other
            return type(self)(
                dimension=self.dimension,
                conversion_tuple=self.conversion_tuple,
                resize=self.resize,
                value=value,
            )
        if isinstance(other, type(self)) or issubclass(other, type(self)):
            new_conversion = tuple(
                {
                    "from_base": self.conversion_tuple[base_unit_index].get("from_base")
                    / other.conversion_tuple[base_unit_index].get("from_base"),
                    "to_base": self.conversion_tuple[base_unit_index].get("to_base")
                    / other.conversion_tuple[base_unit_index].get("to_base"),
                }
                for base_unit_index in BaseUnit
            )
            return type(self)(
                dimension=self.dimension - other.dimension,
                conversion_tuple=new_conversion,
                resize=self.resize / other.resize,
                value=None,
            )


class Meter(Scale):
    dimension: Dimension = Dimension.new_length(power=1)


class Second(Scale):
    dimension: Dimension = Dimension.new_time(power=1)


if __name__ == "__main__":
    a = (4 * Meter) * (7 * Second)
    t = 1 / a
    Velocity = Meter / Second
    Km = Meter * 1000
    V9 = Km**2
    V10 = Km * Km
    Mm = 0.001 * Meter
    Hrs = 3600 * Second
    V2 = Km / Hrs
    V3 = 1/V2
    # V3 = 15 * V2
    V4 = Mm / Hrs
    V5 = 100 / V4
    V6 = 1 / V5
    # r = Velocity(50)
    c = V5.new(10)
    s = c * 10
    (c * c) / c
    q = c / 2
    f = 3 * (c * 5)
    k = c * s
    d = k / 3
    print()
