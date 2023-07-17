from enum import IntEnum

import numpy as np


class TimeType(IntEnum):
    SECONDS = 1
    MINUTES = 2
    HOURS = 3
    DAYS = 4
    WEEKS = 5
    MONTHS = 6
    YEARS = 7


to_default_time = {
    TimeType.SECONDS: lambda x, p: np.float64(x),
    TimeType.MINUTES: lambda x, p: np.float64(x) * 60,
    TimeType.HOURS: lambda x, p: np.float64(x) * 3600,
    TimeType.DAYS: lambda x, p: np.float64(x) * 86400,
    TimeType.WEEKS: lambda x, p: np.float64(x) * 604800,
    TimeType.MONTHS: lambda x, p: np.float64(x) * 2628000,
    TimeType.YEARS: lambda x, p: np.float64(x) * 231536000,
}

from_default_time = {
    TimeType.SECONDS: lambda x, p: np.float64(x),
    TimeType.MINUTES: lambda x, p: np.float64(x) / 60,
    TimeType.HOURS: lambda x, p: np.float64(x) / 3600,
    TimeType.DAYS: lambda x, p: np.float64(x) / 86400,
    TimeType.WEEKS: lambda x, p: np.float64(x) / 604800,
    TimeType.MONTHS: lambda x, p: np.float64(x) / 2628000,
    TimeType.YEARS: lambda x, p: np.float64(x) / 231536000,
}
