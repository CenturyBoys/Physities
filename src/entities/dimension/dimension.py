from dataclasses import dataclass
from fractions import Fraction
from typing import Self

from src.enums.base_units import BaseUnit


@dataclass(frozen=True, slots=True)
class Dimension:
    dimensions_tuple: tuple[float, ...]

    @property
    def length(self):
        return self.dimensions_tuple[BaseUnit.LENGTH]

    @property
    def mass(self):
        return self.dimensions_tuple[BaseUnit.MASS]

    @property
    def temperature(self):
        return self.dimensions_tuple[BaseUnit.TEMPERATURE]

    @property
    def time(self):
        return self.dimensions_tuple[BaseUnit.TIME]

    @property
    def quantity(self):
        return self.dimensions_tuple[BaseUnit.QUANTITY]

    @classmethod
    def new_time(cls, power: float = None) -> Self:
        if power is None:
            power = 1
        dimensions_tuple = [0.0 for i in BaseUnit]
        dimensions_tuple[BaseUnit.TIME] = power
        return cls.new_instance(dimensions_tuple=tuple(dimensions_tuple))

    @classmethod
    def new_length(cls, power: float = None) -> Self:
        if power is None:
            power = 1
        dimensions_tuple = [0.0 for i in BaseUnit]
        dimensions_tuple[BaseUnit.LENGTH] = power
        return cls.new_instance(dimensions_tuple=tuple(dimensions_tuple))

    @classmethod
    def new_temperature(cls, power: float = None) -> Self:
        if power is None:
            power = 1
        dimensions_tuple = [0.0 for i in BaseUnit]
        dimensions_tuple[BaseUnit.TEMPERATURE] = power
        return cls.new_instance(dimensions_tuple=tuple(dimensions_tuple))

    @classmethod
    def new_mass(cls, power: float = None) -> Self:
        if power is None:
            power = 1
        dimensions_tuple = [0.0 for i in BaseUnit]
        dimensions_tuple[BaseUnit.MASS] = power
        return cls.new_instance(dimensions_tuple=tuple(dimensions_tuple))

    @classmethod
    def new_quantity(cls, power: float = None) -> Self:
        if power is None:
            power = 1
        dimensions_tuple = [0.0 for i in BaseUnit]
        dimensions_tuple[BaseUnit.QUANTITY] = power
        return cls.new_instance(dimensions_tuple=tuple(dimensions_tuple))

    @classmethod
    def new_instance(cls, dimensions_tuple: tuple[float, ...]):
        if dimensions_tuple:
            return cls(dimensions_tuple=dimensions_tuple)

    @staticmethod
    def _has_one_type_dimension(dimensions_tuple):
        return len(dimensions_tuple) - dimensions_tuple.count(0) == 1

    def get_dimensions(self):
        return [
            BaseUnit(i)
            for i in range(len(self.dimensions_tuple))
            if self.dimensions_tuple[i]
        ]

    def __add__(self, other):
        if isinstance(other, Dimension):
            dimensions_tuple = tuple(
                sum(i) for i in zip(self.dimensions_tuple, other.dimensions_tuple)
            )
            return Dimension(dimensions_tuple=dimensions_tuple)
        else:
            raise TypeError("Dimension only allow addition between same instance")

    def __sub__(self, other):
        if isinstance(other, Dimension):
            negative_other_dimensions_tuple = tuple(-i for i in other.dimensions_tuple)
            dimensions_tuple = tuple(
                sum(i)
                for i in zip(self.dimensions_tuple, negative_other_dimensions_tuple)
            )
            return Dimension(dimensions_tuple=dimensions_tuple)
        else:
            raise TypeError("Dimension only allow subtraction between same instance")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            dimensions_tuple = tuple(other * i for i in self.dimensions_tuple)
            return Dimension(dimensions_tuple=dimensions_tuple)
        else:
            TypeError("Dimension only allow multiplication with int or floats")

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            dimensions_tuple = tuple(other * i for i in self.dimensions_tuple)
            return Dimension(dimensions_tuple=dimensions_tuple)
        else:
            TypeError("Dimension only allow multiplication with int or floats")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            dimensions_tuple = tuple(i / other for i in self.dimensions_tuple)
            return Dimension(dimensions_tuple=dimensions_tuple)
        else:
            TypeError("Dimension only allow division by int or floats")

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            dimensions_tuple = tuple(other / i for i in self.dimensions_tuple)
            return Dimension(dimensions_tuple=dimensions_tuple)
        else:
            TypeError("Dimension only allow division by int or floats")

    def __eq__(self, other):
        if isinstance(other, Dimension):
            if other.dimensions_tuple == self.dimensions_tuple:
                return True
        if isinstance(other, (int, float)):
            if other == 0 and set(self.dimensions_tuple) == set((0,)):
                return True
            if self._has_one_type_dimension(self.dimensions_tuple):
                return sum(self.dimensions_tuple) == other
        return False

    def show_units(self, power_denominator_limit: int = None):
        symbols = {
            BaseUnit.LENGTH: "L",
            BaseUnit.MASS: "m",
            BaseUnit.TIME: "t",
            BaseUnit.TEMPERATURE: "T",
            BaseUnit.QUANTITY: "N",
        }
        number_str_to_power_str = {
            "0": "⁰",
            "1": "¹",
            "2": "²",
            "3": "³",
            "4": "⁴",
            "5": "⁵",
            "6": "⁶",
            "7": "⁷",
            "8": "⁸",
            "9": "⁹",
        }
        numerator = ""
        denominator = ""
        for i in range(len(self.dimensions_tuple)):
            is_numerator = True
            power = self.dimensions_tuple[i]
            if power == 0:
                continue
            if power < 0:
                is_numerator = False
                power = abs(power)
            power_fraction = Fraction(power)
            if power_denominator_limit:
                power_fraction = power_fraction.limit_denominator(
                    power_denominator_limit
                )
            power_fraction_numerator = power_fraction.numerator
            power_fraction_denominator = power_fraction.denominator
            power_numerator = "".join(
                [number_str_to_power_str[i] for i in str(power_fraction_numerator)]
            )
            power_denominator = "".join(
                [number_str_to_power_str[i] for i in str(power_fraction_denominator)]
            )
            if power_fraction_denominator == 1:
                power_str = f"{power_numerator}"
            else:
                power_str = f"{power_numerator}ᐟ{power_denominator}"
            if is_numerator:
                numerator += f"{symbols[BaseUnit(i)]}{power_str}"
            else:
                denominator += f"{symbols[BaseUnit(i)]}{power_str}"
        if not denominator:
            print(f"{numerator}")
        elif not numerator:
            print(f"1 / {denominator}")
        else:
            print(f"{numerator} / {denominator}")
