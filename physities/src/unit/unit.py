from typing import Self

from physities.src.scale.scale import Scale


class MetaUnit(type):
    scale: Scale

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_scale = self.scale * other
            return type(self)(f"Unit", (Unit,), {"scale": new_scale, "value": None})
        if isinstance(other, MetaUnit):
            new_scale = self.scale * other.scale
            return type(f"Unit", (Unit,), {"scale": new_scale, "value": None})
        raise TypeError(f"{self} only allows multiplication by {self}, {int}, and {float}")

    def __rmul__(self, other):
        try:
            to_return = MetaUnit.__mul__(self, other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_scale = self.scale / other
            return type(f"Unit", (Unit,), {"scale": new_scale, "value": None})
        if isinstance(other, MetaUnit):
            new_scale = self.scale / other.scale
            return type(f"Unit", (Unit,), {"scale": new_scale, "value": None})
        raise TypeError(f"{self} only allows division by {self}, {int}, and {float}")

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_scale = other / self.scale
            return type(f"Unit", (Unit,), {"scale": new_scale, "value": None})
        raise TypeError(f"{self} can divide only {self}, {int} and {float}")

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            new_scale = self.scale ** power
            return type(f"Unit", (Unit,), {"scale": new_scale, "value": None})
        raise TypeError(f"{self} can only be powered by {int} and {float}")


class Unit(metaclass=MetaUnit):
    scale: Scale
    value: float

    def __init__(self, value):
        self.value = value

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_value = self.value * other
            new_instance = type(self)(new_value)
            new_instance.scale = self.scale
            return new_instance
        if isinstance(other, type(self)):
            new_scale = self.scale * other.scale
            new_value = self.value * other.value
            new_instance = type(self)(new_value)
            new_instance.scale = new_scale
            return new_instance
        raise TypeError

    def __rmul__(self, other):
        try:
            to_return = Unit.__mul__(self, other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_value = self.value / other
            new_instance = type(self)(new_value)
            new_instance.scale = self.scale
            return new_instance
        if isinstance(other, type(self)):
            new_scale = self.scale / other.scale
            new_value = self.value / other.value
            new_instance = type(self)(new_value)
            new_instance.scale = new_scale
            return new_instance
        raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_value = other / self.value
            new_scale = 1 / self.scale
            new_instance = type(self)(new_value)
            new_instance.scale = new_scale
            return new_instance
        raise TypeError

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            new_value = self.value ** 2
            new_scale = self.scale ** 2
            new_instance = type(self)(new_value)
            new_instance.scale = new_scale
            return new_instance

    def convert(self, unit: Self) -> Self:
        if self.scale.dimension == unit.scale.dimension:
            new_value = self.value * self.scale.conversion_factor / unit.scale.conversion_factor
            new_instance = type(self)(new_value)
            new_instance.scale = unit.scale
            return new_instance
        raise TypeError
