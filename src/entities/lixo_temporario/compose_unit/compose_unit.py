from dataclasses import dataclass

from src.entities.dimension import Dimension
from src.entities.measurement_unit import MeasurementUnit
from src.enums.length import LengthType
from src.enums.mass import MassType
from src.enums.quantity import QuantityType
from src.enums.temperature import TemperatureType
from src.enums.time import TimeType


@dataclass(frozen=True, slots=True)
class ComposeUnit:
    dimension: Dimension
    value: float
    scale: tuple[LengthType, MassType, TemperatureType, TimeType, QuantityType] = (
        LengthType.METER,
        MassType.KILOGRAM,
        TemperatureType.KELVIN,
        TimeType.SECONDS,
        QuantityType.UNITS,
    )

    def __eq__(self, other):
        if is_base_unit := isinstance(other, self.__class__):
            has_same_dimension = other.dimension == self.dimension
            has_same_scale = other.scale == self.scale
            has_same_name = other.__class__.__name__ == self.__class__.__name__
            return (
                is_base_unit and has_same_dimension and has_same_scale and has_same_name
            )
        return False

    def _has_same_dimension(self, obj):
        return (
            isinstance(obj, self.__class__)
            and sorted(self.numerator) == sorted(obj.numerator)
            and sorted(self.denominator) == sorted(obj.denominator)
        )

    @staticmethod
    def _simplify_dimension(numerator: list, denominator: list):
        while intersection := set(numerator).intersection(set(denominator)):
            for base_type in intersection:
                numerator.remove(base_type)
                denominator.remove(base_type)
        return numerator, denominator

    def __add__(self, other):
        if self._has_same_dimension(other):
            value = self.value + other.value
            return ComposeUnit(
                dimension=self.dimension,
                numerator=self.numerator,
                denominator=self.denominator,
                value=value,
            )
        else:
            raise TypeError(f"The dimensions do not match ! ")

    def __sub__(self, other):
        if self._has_same_dimension(other):
            value = self.value - other.value
            return ComposeUnit(
                dimension=self.dimension,
                numerator=self.numerator,
                denominator=self.denominator,
                value=value,
            )
        else:
            raise TypeError(f"The dimensions do not match ! ")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            value = self.value * other
            return ComposeUnit(
                dimension=self.dimension,
                numerator=self.numerator,
                denominator=self.denominator,
                value=value,
            )
        if isinstance(other, MeasurementUnit):
            value = self.value * other.value
            dimension = self.dimension + other.dimension
            numerator = self.numerator + [other.get_simple_unit_tracker()]
            numerator, denominator = ComposeUnit._simplify_dimension(
                numerator=numerator, denominator=self.denominator
            )
            if dimension == 0:
                return value
            return ComposeUnit(
                dimension=dimension,
                numerator=numerator,
                denominator=denominator,
                value=value,
            )
        if isinstance(other, ComposeUnit):
            value = self.value * other.value
            dimension = self.dimension + other.dimension
            numerator = self.numerator + other.numerator
            denominator = self.denominator + other.denominator
            numerator, denominator = self._simplify_dimension(numerator, denominator)
            if dimension == 0:
                return value
            if dimension == 1:
                return MeasurementUnit(dimension=dimension, value=value)
            return ComposeUnit(
                dimension=dimension,
                numerator=numerator,
                denominator=denominator,
                value=value,
            )
        else:
            raise TypeError(
                f"Operation not defined between {self.__class__} and {type(other)}"
            )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            value = self.value / other
            return ComposeUnit(
                dimension=self.dimension,
                numerator=self.numerator,
                denominator=self.denominator,
                value=value,
            )
        if isinstance(other, MeasurementUnit):
            value = self.value / other.value
            dimension = self.dimension + other.dimension
            denominator = self.denominator + [other.get_simple_unit_tracker()]
            numerator, denominator = ComposeUnit._simplify_dimension(
                numerator=self.numerator, denominator=denominator
            )
            if dimension == 1:
                return MeasurementUnit(dimension=dimension, value=value)
            return ComposeUnit(
                numerator=numerator, denominator=denominator, value=value
            )
        if isinstance(other, self.__class__):
            value = self.value / other.value
            numerator = self.numerator + other.denominator
            denominator = self.denominator + other.numerator
            numerator, denominator = ComposeUnit._simplify_dimension(
                numerator=numerator, denominator=denominator
            )
            if not numerator and not denominator:
                return value
            if len(numerator) == 1 and not denominator:
                return MeasurementUnit(yyy=numerator[0], value=value)
            return ComposeUnit(
                numerator=numerator, denominator=denominator, value=value
            )

    def __rdiv__(self, other):
        if isinstance(other, (int, float)):
            value = other / self.value
            numerator = self.denominator
            denominator = self.denominator
            if len(numerator) == 1 and not denominator:
                return MeasurementUnit(yyy=numerator[0], value=value)
            return ComposeUnit(
                numerator=numerator, denominator=denominator, value=value
            )

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            value = self.value * other
            return ComposeUnit(
                numerator=self.numerator, denominator=self.denominator, value=value
            )
