from enum import IntEnum


class AmountType(IntEnum):
    UNITS = 1
    DOZEN = 2
    MOLES = 3
    PAIRS = 4
    SCORE = 5


to_default_quantity = {
    AmountType.UNITS: lambda x, p: x,
    AmountType.DOZEN: lambda x, p: x * (12 ** p),
    AmountType.MOLES: lambda x, p: x * ((6.022 * 10 ** 23) ** p),
    AmountType.PAIRS: lambda x, p: x * (2 ** p),
    AmountType.SCORE: lambda x, p: x * (20 ** p),
}
from_default_quantity = {
    AmountType.UNITS: lambda x, p: x,
    AmountType.DOZEN: lambda x, p: x / (12 ** p),
    AmountType.MOLES: lambda x, p: x / ((6.022 * 10 ** 23) ** p),
    AmountType.PAIRS: lambda x, p: x / (2 ** p),
    AmountType.SCORE: lambda x, p: x / (20 ** p),
}
