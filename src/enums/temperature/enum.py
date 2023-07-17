from enum import IntEnum
import numpy as np


class TemperatureType(IntEnum):
    CELSIUS = 1
    FAHRENHEIT = 2
    KELVIN = 3


to_default_temperature = {
    TemperatureType.KELVIN: lambda x, p: x,
    TemperatureType.FAHRENHEIT: lambda x, p: (np.float64(x) - 32) * (5 / 9) + 273.15,
    TemperatureType.CELSIUS: lambda x, p: x + 273.15,
}

from_default_temperature = {
    TemperatureType.KELVIN: lambda x, p: x,
    TemperatureType.FAHRENHEIT: lambda x, p: (np.float64(x) - 273.15) * 9 / 5 + 32,
    TemperatureType.CELSIUS: lambda x, p: np.float64(x) - 273.15,
}
