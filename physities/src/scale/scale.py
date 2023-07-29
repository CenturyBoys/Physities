from physities.src.dimension import Dimension
from physities.src.scale.scale_convertor import ScaleConvertor


class MetaScale(type):
    scale_conv: ScaleConvertor

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_scale_conv = self.scale_conv * other
            return type(self)(MetaScale.__name__, (MetaScale,), {"scale_conv": new_scale_conv, "value": None})
        if isinstance(other, MetaScale):
            new_scale_conv = self.scale_conv * other.scale_conv
            return type(f"Scale_", (Scale,), {"scale_conv": new_scale_conv, "value": None})
        raise TypeError(f"{self} only allows multiplication by {self}, {int}, and {float}")

    def __rmul__(self, other):
        try:
            to_return = MetaScale.__mul__(self, other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_scale_conv = self.scale_conv / other
            return type(f"Scale_", (Scale,), {"scale_conv": new_scale_conv, "value": None})
        if isinstance(other, MetaScale):
            new_scale_conv = self.scale_conv / other.scale_conv
            return type(f"Scale_", (Scale,), {"scale_conv": new_scale_conv, "value": None})
        raise TypeError(f"{self} only allows division by {self}, {int}, and {float}")

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_scale_conv = other / self.scale_conv
            return type(f"Scale_", (Scale,), {"scale_conv": new_scale_conv, "value": None})
        raise TypeError(f"{self} can divide only {self}, {int} and {float}")

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            new_scale_conv = self.scale_conv ** power
            return type(f"Scale_", (Scale,), {"scale_conv": new_scale_conv, "value": None})
        raise TypeError(f"{self} can only be powered by {int} and {float}")


class Scale(metaclass=MetaScale):
    scale_conv: ScaleConvertor
    value: float

    def __init__(self, value):
        self.value = value

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_value = self.value * other
            new_instance = type(self)(new_value)
            new_instance.scale_conv = self.scale_conv
            return new_instance
        if isinstance(other, type(self)):
            new_scale_conv = self.scale_conv * other.scale_conv
            new_value = self.value * other.value
            new_instance = type(self)(new_value)
            new_instance.scale_conv = new_scale_conv
            return new_instance
        raise TypeError

    def __rmul__(self, other):
        try:
            to_return = Scale.__mul__(self, other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_value = self.value / other
            new_instance = type(self)(new_value)
            new_instance.scale_conv = self.scale_conv
            return new_instance
        if isinstance(other, type(self)):
            new_scale_conv = self.scale_conv / other.scale_conv
            new_value = self.value / other.value
            new_instance = type(self)(new_value)
            new_instance.scale_conv = new_scale_conv
            return new_instance
        raise TypeError

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_value = other / self.value
            new_scale_conv = 1 / self.scale_conv
            new_instance = type(self)(new_value)
            new_instance.scale_conv = new_scale_conv
            return new_instance
        raise TypeError

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            new_value = self.value **2
            new_scale_conv = self.scale_conv**2
            new_instance = type(self)(new_value)
            new_instance.scale_conv = new_scale_conv
            return new_instance

