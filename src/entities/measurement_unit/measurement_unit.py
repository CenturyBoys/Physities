from dataclasses import dataclass

import numpy as np

from src.entities.dimension import Dimension
from src.enums.base_units import BaseUnit
from src.enums.length import LengthType, to_default_length, from_default_length
from src.enums.mass import MassType, to_default_mass, from_default_mass
from src.enums.quantity import QuantityType, to_default_quantity, from_default_quantity
from src.enums.temperature import (
    TemperatureType,
    to_default_temperature,
    from_default_temperature,
)
from src.enums.time import TimeType, to_default_time, from_default_time


@dataclass(frozen=True, slots=True)
class MeasurementUnit:
    value: np.float64
    dimension: Dimension
    scale: tuple[LengthType, MassType, TemperatureType, TimeType, QuantityType] = (
        LengthType.METER,
        MassType.KILOGRAM,
        TemperatureType.KELVIN,
        TimeType.SECONDS,
        QuantityType.UNITS,
    )

    @classmethod
    def new_instance(
        cls,
        dimension: Dimension,
        value: float = 1,
        length_scale=LengthType.METER,
        mass_scale=MassType.KILOGRAM,
        temperature_scale=TemperatureType.KELVIN,
        time_scale=TimeType.SECONDS,
        quantity_scale=QuantityType.UNITS,
    ):
        value = np.float64(value)
        return cls(
            value=value,
            scale=(
                length_scale,
                mass_scale,
                temperature_scale,
                time_scale,
                quantity_scale,
            ),
            dimension=dimension,
        )

    def __eq__(self, other):
        if not isinstance(other, MeasurementUnit):
            return False
        has_same_dimension = other.dimension == self.dimension
        if not has_same_dimension:
            return False
        has_same_scale = other.scale == self.scale
        if has_same_scale:
            return True

    def __add__(self, other):
        if self == other:
            value = self.value + other.value
            return MeasurementUnit(
                scale=self.scale,
                dimension=self.dimension,
                value=value,
            )
        else:
            raise TypeError(f"The dimensions do not match ! ")

    def __sub__(self, other):
        if self == other:
            value = self.value - other.value
            return MeasurementUnit(
                scale=self.scale,
                dimension=self.dimension,
                value=value,
            )
        else:
            raise TypeError(f"The dimensions do not match ! ")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            value = self.value * other
            return self.__class__(value=value, dimension=self.dimension)
        if isinstance(other, MeasurementUnit):
            value = self.value * other.value
            dimension = self.dimension + other.dimension
            if dimension == 0:
                return value
            return MeasurementUnit(dimension=dimension, value=value)
        else:
            raise TypeError(
                f"Operation not defined between {self.__class__} and {type(other)}"
            )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            value = self.value / other
            return self.__class__(dimension=self.dimension, value=value)
        if isinstance(other, MeasurementUnit):
            value = self.value / other.value
            dimension = self.dimension - other.dimension
            if dimension == 0:
                return value
            return MeasurementUnit(dimension=dimension, value=value)
        else:
            raise TypeError(
                f"Operation not defined between {self.__class__} and {type(other)}"
            )

    def __rdiv__(self, other):
        if isinstance(other, (int, float)):
            value = other / self.value
            dimension = (-1) * self.dimension
            return MeasurementUnit(dimension=dimension, value=value)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            value = self.value * other
            return MeasurementUnit(dimension=self.dimension, value=value)

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            if power == 0:
                return 1
            value = self.value**power
            dimension = power * self.dimension
            return MeasurementUnit(dimension=dimension, value=value)

    def show_units(self, power_denominator_limit: int = None):
        self.dimension.show_units(power_denominator_limit=power_denominator_limit)

    def _length_converter(self, value, length_type: LengthType):
        length_power = self.dimension.length
        actual_type = self.scale[BaseUnit.LENGTH]
        value = to_default_length[actual_type](value, length_power)
        value = from_default_length[length_type](value, length_power)
        return value

    def _mass_converter(self, value, mass_type: MassType):
        mass_power = self.dimension.mass
        actual_type = self.scale[BaseUnit.MASS]
        value = to_default_mass[actual_type](value, mass_power)
        value = from_default_mass[mass_type](value, mass_power)
        return value

    def _time_converter(self, value, time_type: TimeType):
        time_power = self.dimension.time
        actual_type = self.scale[BaseUnit.TIME]
        value = to_default_time[actual_type](value, time_power)
        value = from_default_time[time_type](value, time_power)
        return value

    def _temperature_converter(self, value, temperature_type: TemperatureType):
        temperature_power = self.dimension.temperature
        actual_type = self.scale[BaseUnit.TEMPERATURE]
        if temperature_power
        temperature_inverse_power = 1 / temperature_power
        value = value**temperature_inverse_power
        value = to_default_temperature[actual_type](value, temperature_power)
        value = from_default_temperature[temperature_type](value, temperature_power)
        value = value**temperature_power
        return value

    def _quantity_converter(self, value, quantity_type: QuantityType):
        quantity_power = self.dimension.quantity
        actual_type = self.scale[BaseUnit.QUANTITY]
        value = to_default_quantity[actual_type](value, quantity_power)
        value = from_default_quantity[quantity_type](value, quantity_power)
        return value

    def convert(
        self, length=None, mass=None, time=None, temperature=None, quantity=None
    ):
        value = self.value
        scale = [i for i in self.scale]
        if length:
            scale[BaseUnit.LENGTH] = length
            value = self._length_converter(value=value, length_type=length)
        if mass:
            scale[BaseUnit.MASS] = mass
            value = self._mass_converter(value=value, mass_type=mass)
        if time:
            scale[BaseUnit.TIME] = time
            value = self._time_converter(value=value, time_type=time)
        if temperature:
            scale[BaseUnit.TEMPERATURE] = temperature
            value = self._temperature_converter(
                value=value, temperature_type=temperature
            )
        if quantity:
            scale[BaseUnit.QUANTITY] = quantity
            value = self._quantity_converter(value=value, quantity_type=quantity)
        return self.__class__(dimension=self.dimension, value=value, scale=tuple(scale))


if __name__ == "__main__":
    a = MeasurementUnit(dimension=Dimension.new_length(), value=4)
    b = MeasurementUnit(dimension=Dimension.new_mass(), value=1)
    c = MeasurementUnit(dimension=Dimension.new_time(), value=2)
    d = MeasurementUnit(dimension=Dimension.new_temperature(), value=2)
    (d * d).convert(temperature=TemperatureType.FAHRENHEIT)
    print()
