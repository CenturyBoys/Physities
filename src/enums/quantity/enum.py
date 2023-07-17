from enum import IntEnum

import numpy as np


class QuantityType(IntEnum):
    UNITS = 1
    DOZEN = 2
    MOLES = 3
    PAIRS = 4
    SCORE = 5


to_default_quantity = {
    QuantityType.UNITS: lambda x: np.float64(x),
    QuantityType.DOZEN: lambda x: np.float64(x) * 12,
    QuantityType.MOLES: lambda x: np.float64(x) * 6.022 * 10**23,
    QuantityType.PAIRS: lambda x: np.float64(x) * 2,
    QuantityType.SCORE: lambda x: np.float64(x) * 20,
}
from_default_quantity = {
    QuantityType.UNITS: lambda x: np.float64(x),
    QuantityType.DOZEN: lambda x: np.float64(x) / 12,
    QuantityType.MOLES: lambda x: np.float64(x) / (6.022 * 10**23),
    QuantityType.PAIRS: lambda x: np.float64(x) / 2,
    QuantityType.SCORE: lambda x: np.float64(x) / 20,
}
