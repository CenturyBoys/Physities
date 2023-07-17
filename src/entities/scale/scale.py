from dataclasses import dataclass

from src.enums.base_units import BaseUnit
from src.enums.length import LengthType
from src.enums.mass import MassType
from src.enums.quantity import QuantityType
from src.enums.temperature import TemperatureType
from src.enums.time import TimeType


default_scale = {
    BaseUnit.LENGTH: LengthType.METER,
    BaseUnit.MASS: MassType.KILOGRAM,
    BaseUnit.TEMPERATURE: TemperatureType.KELVIN,
    BaseUnit.TIME: TimeType.SECONDS,
    BaseUnit.QUANTITY: QuantityType.UNITS,
}


@dataclass(frozen=True, slots=True)
class Scale:
    scale_tuple: tuple[LengthType, MassType, TemperatureType, TimeType, QuantityType]

    @classmethod
    def new_instance(
        cls,
        scale_tuple: tuple[
            LengthType, MassType, TemperatureType, TimeType, QuantityType
        ] = None,
        length: LengthType = None,
        mass: MassType = None,
        temperature: TemperatureType = None,
        time: TimeType = None,
        quantity: QuantityType = None,
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
            base_unit_type=BaseUnit.QUANTITY, value=quantity, scale_list=scales
        )
        return cls(scale_tuple=tuple(scales))

    @staticmethod
    def _set_scale_on_scale_list(
        base_unit_type: BaseUnit,
        value: LengthType | MassType | TemperatureType | TimeType | QuantityType,
        scale_list: list,
    ):
        if value:
            scale_list[base_unit_type] = value
        else:
            scale_list[base_unit_type] = default_scale[base_unit_type]
        return scale_list
