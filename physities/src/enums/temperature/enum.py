from enum import IntEnum


class TemperatureType(IntEnum):
    CELSIUS = 1
    FAHRENHEIT = 2
    KELVIN = 3


to_default_temperature = {
    TemperatureType.KELVIN: lambda x: x,
    TemperatureType.FAHRENHEIT: lambda x: (x - 32) * (5 / 9) + 273.15,
    TemperatureType.CELSIUS: lambda x: x + 273.15,
}

from_default_temperature = {
    TemperatureType.KELVIN: lambda x: x,
    TemperatureType.FAHRENHEIT: lambda x: (x - 273.15) * 9 / 5 + 32,
    TemperatureType.CELSIUS: lambda x: x - 273.15,
}
