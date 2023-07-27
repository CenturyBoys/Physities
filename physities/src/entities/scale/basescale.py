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


# @dataclass(frozen=True, slots=True)
class BaseScale(type):
    dimension: Dimension
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

    def __mul__(self, other):
        if self.value is None:
            if isinstance(other, (int, float)):
                dimensions = self.dimension.get_dimensions()
                if len(dimensions) == 1:
                    index = dimensions.pop().value
                    new_conversion = list(self.conversion_tuple)
                    new_conversion[index] = {
                        "from_base": self.conversion_tuple[index].get("from_base")
                        / other,
                        "to_base": self.conversion_tuple[index].get("to_base") * other,
                    }
                    new_conversion = tuple(new_conversion)
                    result_attrs = {
                        "dimension": self.dimension,
                        "conversion_tuple": new_conversion,
                        "resize": self.resize,
                        "value": None,
                    }
                    return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

                result_attrs = {
                    "dimension": self.dimension,
                    "conversion_tuple": self.conversion_tuple,
                    "resize": self.resize * other,
                    "value": None,
                }
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
            elif isinstance(other, type(self)) or issubclass(other, type(self)):
                new_conversion = tuple(
                    {
                        "from_base": self.conversion_tuple[base_unit_index].get(
                            "from_base"
                        )
                        * other.conversion_tuple[base_unit_index].get("from_base"),
                        "to_base": self.conversion_tuple[base_unit_index].get("to_base")
                        * other.conversion_tuple[base_unit_index].get("to_base"),
                    }
                    for base_unit_index in BaseUnit
                )
                result_attrs = {
                    "dimension": self.dimension + other.dimension,
                    "conversion_tuple": new_conversion,
                    "resize": self.resize * other.resize,
                    "value": None,
                }
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
                    new_conversion = list(self.conversion_tuple)
                    new_conversion[index] = {
                        "from_base": self.conversion_tuple[index].get("from_base")
                        * other,
                        "to_base": self.conversion_tuple[index].get("to_base") / other,
                    }
                    new_conversion = tuple(new_conversion)
                    result_attrs = {
                        "dimension": self.dimension,
                        "conversion_tuple": new_conversion,
                        "resize": self.resize,
                        "value": None,
                    }
                    return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

                result_attrs = {
                    "dimension": self.dimension,
                    "conversion_tuple": self.conversion_tuple,
                    "resize": self.resize / other,
                    "value": None,
                }
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
            elif isinstance(other, type(self)) or issubclass(other, type(self)):
                new_conversion = tuple(
                    {
                        "from_base": self.conversion_tuple[base_unit_index].get(
                            "from_base"
                        )
                        / other.conversion_tuple[base_unit_index].get("from_base"),
                        "to_base": self.conversion_tuple[base_unit_index].get("to_base")
                        / other.conversion_tuple[base_unit_index].get("to_base"),
                    }
                    for base_unit_index in BaseUnit
                )
                result_attrs = {
                    "dimension": self.dimension - other.dimension,
                    "conversion_tuple": new_conversion,
                    "resize": self.resize / other.resize,
                    "value": None,
                }
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
                    new_conversion = list(self.conversion_tuple)
                    new_conversion[index] = {
                        "from_base": self.conversion_tuple[index].get("from_base")
                        * other,
                        "to_base": other / self.conversion_tuple[index].get("to_base"),
                    }
                    new_conversion = tuple(new_conversion)
                    result_attrs = {
                        "dimension": dimension,
                        "conversion_tuple": new_conversion,
                        "resize": self.resize,
                        "value": None,
                    }
                    return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

                result_attrs = {
                    "dimension": dimension,
                    "conversion_tuple": self.conversion_tuple,
                    "resize": other / self.resize,
                    "value": None,
                }
                return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

    def __pow__(self, power, modulo=None):
        if not isinstance(power, (int, float)):
            raise TypeError("Can only exponentiate int's and float's")
        conversion_tuple = tuple(
            {
                "from_base": self.conversion_tuple[base_unit_index].get("from_base")
                ** power,
                "to_base": self.conversion_tuple[base_unit_index].get("to_base")
                ** power,
            }
            for base_unit_index in BaseUnit
        )
        result_attrs = {
            "dimension": self.dimension * power,
            "conversion_tuple": conversion_tuple,
            "resize": self.resize**power,
            "value": None,
        }
        return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)

    def __add__(self, other):
        raise TypeError("Can't shift scales")

    def __sub__(self, other):
        raise TypeError("Can't shift scales")

    def __radd__(self, other):
        raise TypeError("Can't shift scales")

    def __rsub__(self, other):
        raise TypeError("Can't shift scales")

    def __rpow__(self, other):
        raise TypeError("Can't exponentiate dimensional thing")


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
                    "from_base": self.conversion_tuple[base_unit_index].get(
                        "from_base"
                    )
                                 / other.conversion_tuple[base_unit_index].get("from_base"),
                    "to_base": self.conversion_tuple[base_unit_index].get("to_base")
                               / other.conversion_tuple[base_unit_index].get("to_base"),
                }
                for base_unit_index in BaseUnit
            )
            result_attrs = {
                "dimension": self.dimension - other.dimension,
                "conversion_tuple": new_conversion,
                "resize": self.resize / other.resize,
                "value": None,
            }
            return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)


class Meter(Scale):
    dimension: Dimension = Dimension.new_length(power=1)


class Second(Scale):
    dimension: Dimension = Dimension.new_time(power=1)


if __name__ == "__main__":
    Velocity = Meter / Second
    Km = Meter * 1000
    V9 = Km**2
    V10 = Km * Km
    Mm = 0.001 * Meter
    Hrs = 3600 * Second
    V2 = Km / Hrs
    V3 = 15 * V2
    V4 = Mm / Hrs
    V5 = 100 / V4
    V6 = 1 / V5
    # r = Velocity(50)
    c = V5.new(10)
    s = c * 10
    f = 3 * (c * 5)
    k = c * s
    d = k /3
    print()
