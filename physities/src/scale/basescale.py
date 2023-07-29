from physities.src.dimension import Dimension
from physities.src.scale.scale_convertor import ScaleConvertor
from physities.src.enums.base_units import BaseDimensions
from physities.src.enums.length import LengthType
from physities.src.enums.mass import MassType
from physities.src.enums.quantity import AmountType
from physities.src.enums.temperature import TemperatureType
from physities.src.enums.time import TimeType


default_scale = {
    BaseDimensions.LENGTH: LengthType.METER,
    BaseDimensions.MASS: MassType.KILOGRAM,
    BaseDimensions.TEMPERATURE: TemperatureType.KELVIN,
    BaseDimensions.TIME: TimeType.SECONDS,
    BaseDimensions.AMOUNT: AmountType.UNITS,
}


# @dataclass(frozen=True, slots=True)
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

    def __rpow__(self, other):
        raise TypeError("Dimensional thing can't be a exponent")

    def __add__(self, other):
        raise TypeError("Offsets are not allowed yet.")

    def __sub__(self, other):
        raise TypeError("Offsets are not allowed yet.")

    def __radd__(self, other):
        raise TypeError("Offsets are not allowed yet.")

    def __rsub__(self, other):
        raise TypeError("Offsets are not allowed yet.")


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

if __name__ == "__main__":
    class Meter(Scale):
        scale_conv: ScaleConvertor = ScaleConvertor(from_base_conversions=(1, 1, 1, 1, 1, 1, 1), dimension=Dimension.new_instance(dimensions_tuple=(1, 0, 0, 0, 0, 0, 0)), rescale_value=1)
        value: float

    M2 = 3*Meter*Meter
    d = M2(5)
    c = d*d
    h = 3*c*c
    h2 = 2 / h
    h3 = c**2
    h4 = c/h3
    M3 = M2*Meter
    e = M3(10)
    input()

#
# class BaseScale2(type):
#     dimension: Dimension = None
#     value: float = None
#     resize: float = 1
#     conversion_tuple: tuple[float, float, float, float, float] = tuple(
#         1 for i in BaseDimensions
#     )
#
#     def __call__(cls, value, dimension, conversion_tuple, resize):
#         # This method creates an instance of the dynamically generated class
#         instance = ScaleConvertor.__new__(ScaleConvertor)
#         instance.__init__(
#             dimension=dimension,
#             conversion_tuple=conversion_tuple,
#             resize=resize,
#             value=value,
#         )
#         return instance
#
#     @classmethod
#     def new(cls, value):
#         instance = cls.__call__(
#             cls,
#             dimension=cls.dimension,
#             conversion_tuple=cls.conversion_tuple,
#             resize=cls.resize,
#             value=value,
#         )
#         return instance
#
#     @staticmethod
#     def __form_result_attrs(dimension, conversion_tuple, resize):
#         return {
#             "dimension": dimension,
#             "conversion_tuple": conversion_tuple,
#             "resize": resize,
#             "value": None,
#         }
#
#     def __eq__(self, other):
#         if isinstance(other, BaseScale):
#             if (
#                 self.dimension == other.dimension
#                 and self.resize == other.resize
#                 and self.conversion_tuple == other.conversion_tuple
#             ):
#                 return True
#         return False
#
#     def __mul__(self, other):
#         if self.value is None:
#             if isinstance(other, (int, float)):
#                 dimensions = self.dimension.get_dimensions()
#                 if len(dimensions) == 1:
#                     index = dimensions.pop().value
#                     new_conversion = self.__tuple_number_conversion_operation(
#                         tuple_var=self.conversion_tuple,
#                         number=other,
#                         from_base_callable=lambda t, n: t * n,
#                         index=index,
#                     )
#                     result_attrs = self.__form_result_attrs(
#                         dimension=self.dimension,
#                         conversion_tuple=new_conversion,
#                         resize=self.resize,
#                     )
#                     return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#
#                 result_attrs = self.__form_result_attrs(
#                     dimension=self.dimension,
#                     conversion_tuple=self.conversion_tuple,
#                     resize=self.resize * other,
#                 )
#                 return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#
#             elif isinstance(other, type(self)) or issubclass(other, type(self)):
#                 new_dimension = self.dimension + other.dimension
#                 new_conversion, resize_factor = self.__tuple_tuple_conversion_operation(
#                     tuple_1=self.conversion_tuple,
#                     tuple_2=other.conversion_tuple,
#                     dimension_1=self.dimension,
#                     dimension_2=other.dimension,
#                     result_dimension=new_dimension,
#                     from_base_callable=lambda s, o: s * o,
#                 )
#                 result_attrs = self.__form_result_attrs(
#                     dimension=new_dimension,
#                     conversion_tuple=new_conversion,
#                     resize=resize_factor * self.resize * other.resize,
#                 )
#                 return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#
#             else:
#                 raise TypeError
#
#     def __rmul__(self, other):
#         try:
#             to_return = BaseScale.__mul__(self, other)
#         except TypeError as e:
#             raise e
#         return to_return
#
#     def __truediv__(self, other):
#         if self.value is None:
#             if isinstance(other, (int, float)):
#                 dimensions = self.dimension.get_dimensions()
#                 if len(dimensions) == 1:
#                     index = dimensions.pop().value
#                     new_conversion = self.__tuple_number_conversion_operation(
#                         tuple_var=self.conversion_tuple,
#                         number=other,
#                         from_base_callable=lambda t, n: t / n,
#                         index=index,
#                     )
#                     result_attrs = self.__form_result_attrs(
#                         dimension=self.dimension,
#                         conversion_tuple=new_conversion,
#                         resize=self.resize,
#                     )
#                     return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#
#                 result_attrs = self.__form_result_attrs(
#                     dimension=self.dimension,
#                     conversion_tuple=self.conversion_tuple,
#                     resize=self.resize / other,
#                 )
#                 return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#             elif isinstance(other, type(self)) or issubclass(other, type(self)):
#                 new_dimension = self.dimension - other.dimension
#                 new_conversion, resize_factor = self.__tuple_tuple_conversion_operation(
#                     tuple_1=self.conversion_tuple,
#                     tuple_2=other.conversion_tuple,
#                     dimension_1=self.dimension,
#                     dimension_2=other.dimension,
#                     result_dimension=new_dimension,
#                     from_base_callable=lambda s, o: s / o,
#                 )
#                 result_attrs = self.__form_result_attrs(
#                     dimension=new_dimension,
#                     conversion_tuple=new_conversion,
#                     resize=resize_factor * (self.resize / other.resize),
#                 )
#                 return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#             else:
#                 raise TypeError
#
#     def __rtruediv__(self, other):
#         if self.value is None:
#             if isinstance(other, (int, float)):
#                 dimensions = self.dimension.get_dimensions()
#                 dimension = self.dimension * -1
#                 if len(dimensions) == 1:
#                     index = dimensions.pop().value
#                     new_conversion = self.__tuple_number_conversion_operation(
#                         tuple_var=self.conversion_tuple,
#                         number=other,
#                         from_base_callable=lambda t, n: n / t,
#                         index=index,
#                     )
#                     result_attrs = self.__form_result_attrs(
#                         dimension=dimension,
#                         conversion_tuple=new_conversion,
#                         resize=self.resize,
#                     )
#                     return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#
#                 new_conversion = self.__tuple_number_conversion_operation(
#                     tuple_var=self.conversion_tuple,
#                     number=1,
#                     from_base_callable=lambda t, n: 1 / t,
#                 )
#                 result_attrs = self.__form_result_attrs(
#                     dimension=dimension,
#                     conversion_tuple=new_conversion,
#                     resize=other / self.resize,
#                 )
#                 return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#         else:
#             raise TypeError
#
#     @staticmethod
#     def __get_annulled_dimensions(
#         dimension_1: Dimension, dimension_2: Dimension, result_dimension: Dimension
#     ):
#         set_1 = set(dimension_1.get_dimensions())
#         set_2 = set(dimension_2.get_dimensions())
#         set_1_2 = set(result_dimension.get_dimensions())
#         return list((set_1 - set_1_2).union(set_2 - set_1_2))
#
#     @staticmethod
#     def __tuple_tuple_conversion_operation(
#         tuple_1, tuple_2, dimension_1, dimension_2, result_dimension, from_base_callable
#     ):
#         annulled_dimensions = BaseScale.__get_annulled_dimensions(
#             dimension_1=dimension_1,
#             dimension_2=dimension_2,
#             result_dimension=result_dimension,
#         )
#         operated_conversion_list = list(
#             from_base_callable(tuple_1[base_unit_index], tuple_2[base_unit_index])
#             for base_unit_index in BaseDimensions
#         )
#         resize_factor = 1
#         for index in annulled_dimensions:
#             resize_factor *= operated_conversion_list[index]
#             operated_conversion_list[index] = 1
#         new_conversion = tuple(operated_conversion_list)
#         return new_conversion, resize_factor
#
#     @staticmethod
#     def __tuple_number_conversion_operation(
#         tuple_var, number, from_base_callable, index=None
#     ):
#         if index is None:
#             return tuple(
#                 from_base_callable(tuple_var[base_unit_index], number)
#                 for base_unit_index in BaseDimensions
#             )
#         new_conversion = list(tuple_var)
#         new_conversion[index] = from_base_callable(tuple_var[index], number)
#         return tuple(new_conversion)
#
#     def __pow__(self, power, modulo=None):
#         if not isinstance(power, (int, float)):
#             raise TypeError("Can only exponentiate int's and float's")
#         new_conversion = self.__tuple_number_conversion_operation(
#             tuple_var=self.conversion_tuple,
#             number=power,
#             from_base_callable=lambda t, n: t**n,
#         )
#         result_attrs = self.__form_result_attrs(
#             dimension=self.dimension * power,
#             conversion_tuple=new_conversion,
#             resize=self.resize**power,
#         )
#         return type(self)(BaseScale.__name__, (BaseScale,), result_attrs)
#
    # def __add__(self, other):
    #     raise TypeError("Scales offset are not allowed yet.")
    #
    # def __sub__(self, other):
    #     raise TypeError("Scales offset are not allowed yet.")
    #
    # def __radd__(self, other):
    #     raise TypeError("Scales offset are not allowed yet.")
    #
    # def __rsub__(self, other):
    #     raise TypeError("Scales offset are not allowed yet.")
#
#     def __rpow__(self, other):
#         raise TypeError("A dimensional thing be a exponent.")
#
#
# class Scale2(metaclass=BaseScale):
#     dimension: Dimension
#     conversion_tuple: tuple
#     resize: float
#     value: float = None
#
#     def __init__(self, dimension, conversion_tuple, resize, value):
#         self.dimension = dimension
#         self.conversion_tuple = conversion_tuple
#         self.resize = resize
#         self.value = value
#
#     def __mul__(self, other):
#         if isinstance(other, (int, float)):
#             value = self.value * other
#             return type(self)(
#                 dimension=self.dimension,
#                 conversion_tuple=self.conversion_tuple,
#                 resize=self.resize,
#                 value=value,
#             )
#         if isinstance(other, type(self)) or issubclass(other, type(self)):
#             dimension = self.dimension + other.dimension
#             resize = self.resize * other.resize
#             conversion_tuple = tuple(
#                 {
#                     "from_base": self.conversion_tuple[base_unit_index].get("from_base")
#                     * other.conversion_tuple[base_unit_index].get("from_base"),
#                     "to_base": self.conversion_tuple[base_unit_index].get("to_base")
#                     * other.conversion_tuple[base_unit_index].get("to_base"),
#                 }
#                 for base_unit_index in BaseDimensions
#             )
#             value = self.value * other.value
#             return type(self)(
#                 dimension=dimension,
#                 conversion_tuple=conversion_tuple,
#                 resize=resize,
#                 value=value,
#             )
#         raise TypeError(f"Operation between {type(self)} and {type(other)} not allowed")
#
#     def __rmul__(self, other):
#         try:
#             to_return = self.__mul__(other)
#         except TypeError as e:
#             raise e
#         return to_return
#
#     def __truediv__(self, other):
#         if isinstance(other, (int, float)):
#             value = self.value / other
#             return type(self)(
#                 dimension=self.dimension,
#                 conversion_tuple=self.conversion_tuple,
#                 resize=self.resize,
#                 value=value,
#             )
#         if isinstance(other, type(self)) or issubclass(other, type(self)):
#             new_conversion = tuple(
#                 {
#                     "from_base": self.conversion_tuple[base_unit_index].get("from_base")
#                     / other.conversion_tuple[base_unit_index].get("from_base"),
#                     "to_base": self.conversion_tuple[base_unit_index].get("to_base")
#                     / other.conversion_tuple[base_unit_index].get("to_base"),
#                 }
#                 for base_unit_index in BaseDimensions
#             )
#             return type(self)(
#                 dimension=self.dimension - other.dimension,
#                 conversion_tuple=new_conversion,
#                 resize=self.resize / other.resize,
#                 value=None,
#             )
#
#
# class Meter(ScaleConvertor):
#     dimension: Dimension = Dimension.new_length(power=1)
#
#
# class Second(ScaleConvertor):
#     dimension: Dimension = Dimension.new_time(power=1)
#
#
# if __name__ == "__main__":
#     a = (4 * Meter) * (7 * Second)
#     t = 1 / a
#     Velocity = Meter / Second
#     Km = Meter * 1000
#     V9 = Km**2
#     V10 = Km * Km
#     Mm = 0.001 * Meter
#     Hrs = 3600 * Second
#     V2 = Km / Hrs
#     V3 = Km / V2
#     # V3 = 15 * V2
#     V4 = Mm / Hrs
#     V5 = 100 / V4
#     V6 = 1 / V5
#     # r = Velocity(50)
#     c = V5.new(10)
#     s = c * 10
#     (c * c) / c
#     q = c / 2
#     f = 3 * (c * 5)
#     k = c * s
#     d = k / 3
#     print()