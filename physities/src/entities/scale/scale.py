from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class Scale:
    scale_tuple: tuple[BaseUnit]

    @classmethod
    def new_instance(
        cls,
        scale_tuple: tuple[BaseUnit] = None,
        length: LengthType = None,
        mass: MassType = None,
        temperature: TemperatureType = None,
        time: TimeType = None,
        quantity: AmountType = None,
    ):
        if scale_tuple:
            return cls(scale_tuple=scale_tuple)
        scales = [None, None, None, None, None]
        scales = Scale._set_scale_on_scale_list(
            base_unit_type=BaseUnit.LENGTH, value=length, scale_list=scales
        )
        scales = Scale._set_scale_on_scale_list(
            base_unit_type=BaseUnit.MASS, value=mass, scale_list=scales
        )
        scales = Scale._set_scale_on_scale_list(
            base_unit_type=BaseUnit.TEMPERATURE, value=temperature, scale_list=scales
        )
        scales = Scale._set_scale_on_scale_list(
            base_unit_type=BaseUnit.TIME, value=time, scale_list=scales
        )
        scales = Scale._set_scale_on_scale_list(
            base_unit_type=BaseUnit.AMOUNT, value=quantity, scale_list=scales
        )
        return cls(scale_tuple=tuple(scales))

    @staticmethod
    def _set_scale_on_scale_list(
        base_unit_type: BaseUnit,
        value: LengthType | MassType | TemperatureType | TimeType | AmountType,
        scale_list: list,
    ):
        if value:
            scale_list[base_unit_type] = value
        else:
            scale_list[base_unit_type] = default_scale[base_unit_type]
        return scale_list
