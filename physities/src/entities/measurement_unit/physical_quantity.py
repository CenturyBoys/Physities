from dataclasses import dataclass


from physities.src.entities.dimension import Dimension
from physities.src.enums.base_units import BaseUnit
from physities.src.enums.length import (
    LengthType,
    to_default_length,
    from_default_length,
)
from physities.src.enums.mass import MassType, to_default_mass, from_default_mass
from physities.src.enums.quantity import (
    AmountType,
    to_default_quantity,
    from_default_quantity,
)
from physities.src.enums.temperature import (
    TemperatureType,
    to_default_temperature,
    from_default_temperature,
)
from physities.src.enums.time import TimeType, to_default_time, from_default_time


@dataclass(frozen=True, slots=True)
class PhysicalQuantity:
    value: float
    dimension: Dimension
    scale: tuple[BaseUnit] = (
        LengthType.METER,
        MassType.KILOGRAM,
        TemperatureType.KELVIN,
        TimeType.SECONDS,
        AmountType.UNITS,
    )

    @classmethod
    def new_instance(
        cls,
        dimension: Dimension,
        value: float = 0,
        length_scale=LengthType.METER,
        mass_scale=MassType.KILOGRAM,
        temperature_scale=TemperatureType.KELVIN,
        time_scale=TimeType.SECONDS,
        quantity_scale=AmountType.UNITS,
    ):
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
        if not isinstance(other, PhysicalQuantity):
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
            return PhysicalQuantity(
                scale=self.scale,
                dimension=self.dimension,
                value=value,
            )
        else:
            raise TypeError(f"The dimensions do not match ! ")

    def __sub__(self, other):
        if self == other:
            value = self.value - other.value
            return PhysicalQuantity(
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
        if isinstance(other, PhysicalQuantity):
            value = self.value * other.value
            dimension = self.dimension + other.dimension
            if dimension == 0:
                return value
            return PhysicalQuantity(dimension=dimension, value=value)
        else:
            raise TypeError(
                f"Operation not defined between {self.__class__} and {type(other)}"
            )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            value = self.value / other
            return self.__class__(dimension=self.dimension, value=value)
        if isinstance(other, PhysicalQuantity):
            value = self.value / other.value
            dimension = self.dimension - other.dimension
            if dimension == 0:
                return value
            return PhysicalQuantity(dimension=dimension, value=value)
        else:
            raise TypeError(
                f"Operation not defined between {self.__class__} and {type(other)}"
            )

    def __rdiv__(self, other):
        if isinstance(other, (int, float)):
            value = other / self.value
            dimension = (-1) * self.dimension
            return PhysicalQuantity(dimension=dimension, value=value)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            value = self.value * other
            return PhysicalQuantity(dimension=self.dimension, value=value)

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            if power == 0:
                return 1
            value = self.value**power
            dimension = power * self.dimension
            return PhysicalQuantity(dimension=dimension, value=value)

    def show_dimension(self, power_denominator_limit: int = None):
        self.dimension.show_dimension(power_denominator_limit=power_denominator_limit)

    def _length_converter(self, value, length_type: LengthType):
        length_power = self.dimension.length
        if length_power == 0:
            return value
        actual_type = self.scale[BaseUnit.LENGTH]
        value = to_default_length[actual_type](value, length_power)
        value = from_default_length[length_type](value, length_power)
        return value

    def _mass_converter(self, value, mass_type: MassType):
        mass_power = self.dimension.mass
        if mass_power == 0:
            return value
        actual_type = self.scale[BaseUnit.MASS]
        value = to_default_mass[actual_type](value, mass_power)
        value = from_default_mass[mass_type](value, mass_power)
        return value

    def _time_converter(self, value, time_type: TimeType):
        time_power = self.dimension.time
        if time_power == 0:
            return value
        actual_type = self.scale[BaseUnit.TIME]
        value = to_default_time[actual_type](value, time_power)
        value = from_default_time[time_type](value, time_power)
        return value

    def _temperature_converter(self, value, temperature_type: TemperatureType):
        temperature_power = self.dimension.temperature
        if temperature_power == 0:
            return value
        temperature_inverse_power = 1 / temperature_power
        actual_type = self.scale[BaseUnit.TEMPERATURE]
        value = value**temperature_inverse_power
        value = to_default_temperature[actual_type](value)
        value = from_default_temperature[temperature_type](value)
        value = value**temperature_power
        return value

    def _quantity_converter(self, value, quantity_type: AmountType):
        quantity_power = self.dimension.amount
        if quantity_power:
            return value
        actual_type = self.scale[BaseUnit.AMOUNT]
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
            scale[BaseUnit.AMOUNT] = quantity
            value = self._quantity_converter(value=value, quantity_type=quantity)
        return self.__class__(dimension=self.dimension, value=value, scale=tuple(scale))


if __name__ == "__main__":
    a = PhysicalQuantity(dimension=Dimension.new_length(), value=4)
    b = PhysicalQuantity(dimension=Dimension.new_mass(), value=1)
    c = PhysicalQuantity(dimension=Dimension.new_time(), value=2)
    d = PhysicalQuantity(dimension=Dimension.new_temperature(), value=2)
    (d * d).convert(temperature=TemperatureType.FAHRENHEIT)
    print()
