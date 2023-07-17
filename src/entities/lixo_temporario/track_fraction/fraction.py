# from dataclasses import dataclass
#
# from src.enums.base_units import BaseUnit
#
#
# @dataclass(frozen=True, slots=True)
# class Tracker:
#     unit_type: BaseUnit
#     name: str
#     power: tuple[int,int] = (1, 1)
#
#     def _get_power_str(self):
#         power_str_dict = {
#             "0": "⁰",
#             "1": "¹",
#             "2": "²",
#             "3": "³",
#             "4": "⁴",
#             "5": "⁵",
#             "6": "⁶",
#             "7": "⁷",
#             "8": "⁸",
#             "9": "⁹"
#         }
#         numerator = "".join([power_str_dict[i] for i in str(self.power[0])])
#         if self.power[1] == 1:
#             if self.power[0] == 1:
#                 return ""
#             return f"{numerator}"
#         denominator = "".join([power_str_dict[i] for i in str(self.power[1])])
#         return f"{numerator}ᐟ{denominator}"
#
#     def __add__(self, other):
#         if isinstance(other, Tracker):
#             if self.unit_type == other.unit_type:
#                 if self.name == other.name and self.power == other.power:
#                     return Tracker(unit_type=self.unit_type, name=self.name, power=self.power)
#                 name = f'{self.name}{self._get_power_str()} + {other.name}{other._get_power_str()}'
#                 return Tracker(unit_type=self.unit_type, name=name, power=(1, 1))
#             raise TypeError("Tracker can't add different BaseUnits")
#         raise TypeError(f" Addition not implemented between {type(self)} and {type(other)}")
#
#     def __sub__(self, other):
#         if isinstance(other, Tracker):
#             if self.unit_type == other.unit_type:
#                 if self.name == other.name and self.power == other.power:
#                     return Tracker(unit_type=self.unit_type, name=self.name, power=self.power)
#                 name = f'{self.name}{self._get_power_str()} - {other.name}{other._get_power_str()}'
#                 return Tracker(unit_type=self.unit_type, name=name, power=(1, 1))
#             raise TypeError("Tracker can't subtract different BaseUnits")
#         raise TypeError(f" Subtraction not implemented between {type(self)} and {type(other)}")
#
#     def __mul__(self, other):
#         if isinstance(other, Tracker):
#             if self.unit_type == other.unit_type:
#                 if self.name == other.name:
#                     power = (self.power[0] + other.power[0], self.power[1] + other.power[1])
#                     return Tracker(unit_type=self.unit_type, name=self.name, power=power)
#                 name = f"{self.name}{self._get_power_str()}{other.name}{other._get_power_str()}"
#                 return Tracker(unit_type=self.unit_type, name=name, power=(1, 1))
#             return [self, other]
#
# @dataclass(frozen=True, slots=True)
# class Fraction:
#     numerator: list[Tracker, ...]
#     denominator: list[Tracker, ...]
#
#     def __add__(self, other):
#
#
# @staticmethod
# def _simplify_fraction(numerator: list, denominator: list):
#     while intersection := set(numerator).intersection(set(denominator)):
#         for base_type in intersection:
#             numerator.remove(base_type)
#             denominator.remove(base_type)
#     return numerator, denominator
