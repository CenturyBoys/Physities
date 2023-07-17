from enum import IntEnum

import numpy as np


class MassType(IntEnum):
    KILOGRAM = 1
    POUND = 2
    OUNCE = 3
    GRAM = 4
    MILLIGRAM = 5
    TONNE = 6
    STONE = 7
    CARAT = 8
    GRAIN = 9
    SLUG = 10


to_default_mass = {
    MassType.KILOGRAM: lambda x: np.float64(x),
    MassType.POUND: lambda x: np.float64(x) * 0.453592,
    MassType.OUNCE: lambda x: np.float64(x) * 0.0283495,
    MassType.GRAM: lambda x: np.float64(x) * 0.001,
    MassType.MILLIGRAM: lambda x: np.float64(x) * 0.000001,
    MassType.TONNE: lambda x: np.float64(x) * 1000,
    MassType.STONE: lambda x: np.float64(x) * 6.35029,
    MassType.CARAT: lambda x: np.float64(x) * 0.0002,
    MassType.GRAIN: lambda x: np.float64(x) * 0.0000647989,
    MassType.SLUG: lambda x: np.float64(x) * 14.5939,
}

from_default_mass = {
    MassType.KILOGRAM: lambda x: np.float64(x),
    MassType.POUND: lambda x: np.float64(x) / 0.453592,
    MassType.OUNCE: lambda x: np.float64(x) / 0.0283495,
    MassType.GRAM: lambda x: np.float64(x) / 0.001,
    MassType.MILLIGRAM: lambda x: np.float64(x) / 0.000001,
    MassType.TONNE: lambda x: np.float64(x) / 1000,
    MassType.STONE: lambda x: np.float64(x) / 6.35029,
    MassType.CARAT: lambda x: np.float64(x) / 0.0002,
    MassType.GRAIN: lambda x: np.float64(x) / 0.0000647989,
    MassType.SLUG: lambda x: np.float64(x) / 14.5939,
}
