from enum import IntEnum

import numpy as np


class LengthType(IntEnum):
    METER = 1
    DECIMETER = 12
    CENTIMETER = 5
    MILLIMETER = 6
    KILOMETER = 7
    FOOT = 2
    YARD = 3
    INCH = 4
    HECTOMETER = 8
    MILE = 9
    FURLONG = 10
    ROD = 11


to_default_length = {
    LengthType.METER: lambda x, p: np.float64(x),
    LengthType.DECIMETER: lambda x, p: np.float64(x) * (0.1**p),
    LengthType.CENTIMETER: lambda x, p: np.float64(x) * (0.01**p),
    LengthType.MILLIMETER: lambda x, p: np.float64(x) * (0.001**p),
    LengthType.KILOMETER: lambda x, p: np.float64(x) * (1000**p),
    LengthType.FOOT: lambda x, p: np.float64(x) * (0.3048**p),
    LengthType.YARD: lambda x, p: np.float64(x) * (0.9144**p),
    LengthType.INCH: lambda x, p: np.float64(x) * (0.0254**p),
    LengthType.HECTOMETER: lambda x, p: np.float64(x) * (100**p),
    LengthType.MILE: lambda x, p: np.float64(x) * (1609.34**p),
    LengthType.FURLONG: lambda x, p: np.float64(x) * (201.168**p),
    LengthType.ROD: lambda x, p: np.float64(x) * (5.0292**p),
}

from_default_length = {
    LengthType.METER: lambda x, p: np.float64(x),
    LengthType.DECIMETER: lambda x, p: np.float64(x) / (0.1**p),
    LengthType.CENTIMETER: lambda x, p: np.float64(x) / (0.01**p),
    LengthType.MILLIMETER: lambda x, p: np.float64(x) / (0.001**p),
    LengthType.KILOMETER: lambda x, p: np.float64(x) / (1000**p),
    LengthType.FOOT: lambda x, p: np.float64(x) / (0.3048**p),
    LengthType.YARD: lambda x, p: np.float64(x) / (0.9144**p),
    LengthType.INCH: lambda x, p: np.float64(x) / (0.0254**p),
    LengthType.HECTOMETER: lambda x, p: np.float64(x) / (100**p),
    LengthType.MILE: lambda x, p: np.float64(x) / (1609.34**p),
    LengthType.FURLONG: lambda x, p: np.float64(x) / (201.168**p),
    LengthType.ROD: lambda x, p: np.float64(x) / (5.0292**p),
}
