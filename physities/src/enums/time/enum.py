from enum import IntEnum


class TimeType(IntEnum):
    SECONDS = 1
    MINUTES = 2
    HOURS = 3
    DAYS = 4
    WEEKS = 5
    MONTHS = 6
    YEARS = 7


to_default_time = {
    TimeType.SECONDS: lambda x, p: x,
    TimeType.MINUTES: lambda x, p: x * (60**p),
    TimeType.HOURS: lambda x, p: x * (3600**p),
    TimeType.DAYS: lambda x, p: x * (86400**p),
    TimeType.WEEKS: lambda x, p: x * (604800**p),
    TimeType.MONTHS: lambda x, p: x * (2628000**p),
    TimeType.YEARS: lambda x, p: x * (231536000**p),
}

from_default_time = {
    TimeType.SECONDS: lambda x, p: x,
    TimeType.MINUTES: lambda x, p: x / (60**p),
    TimeType.HOURS: lambda x, p: x / (3600**p),
    TimeType.DAYS: lambda x, p: x / (86400**p),
    TimeType.WEEKS: lambda x, p: x / (604800**p),
    TimeType.MONTHS: lambda x, p: x / (2628000**p),
    TimeType.YEARS: lambda x, p: x / (231536000**p),
}
