from enum import IntEnum


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
    MassType.KILOGRAM: lambda x, p: x,
    MassType.POUND: lambda x, p: x * (0.453592**p),
    MassType.OUNCE: lambda x, p: x * (0.0283495**p),
    MassType.GRAM: lambda x, p: x * (0.001**p),
    MassType.MILLIGRAM: lambda x, p: x * (0.000001**p),
    MassType.TONNE: lambda x, p: x * (1000**p),
    MassType.STONE: lambda x, p: x * (6.35029**p),
    MassType.CARAT: lambda x, p: x * (0.0002**p),
    MassType.GRAIN: lambda x, p: x * (0.0000647989**p),
    MassType.SLUG: lambda x, p: x * (14.5939**p),
}

from_default_mass = {
    MassType.KILOGRAM: lambda x, p: x,
    MassType.POUND: lambda x, p: x / (0.453592**p),
    MassType.OUNCE: lambda x, p: x / (0.0283495**p),
    MassType.GRAM: lambda x, p: x / (0.001**p),
    MassType.MILLIGRAM: lambda x, p: x / (0.000001**p),
    MassType.TONNE: lambda x, p: x / (1000**p),
    MassType.STONE: lambda x, p: x / (6.35029**p),
    MassType.CARAT: lambda x, p: x / (0.0002**p),
    MassType.GRAIN: lambda x, p: x / (0.0000647989**p),
    MassType.SLUG: lambda x, p: x / (14.5939**p),
}
