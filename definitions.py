from enum import StrEnum


class Scale(StrEnum):
    M = "m"


class BaseDimensions:
    d: float
    s: Scale
    v: float

    def __init__(self, d=1.0, s=Scale.M, v=None):
        self.d = d
        self.s = s
        self.v = v

    def __repr__(self):
        if self.v is None:
            return f"BaseUnitDefinition(dimension={self.d}, scale={self.s})"
        return f"BaseDimensions(dimension={self.d}, scale={self.s}, value={self.v})"

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            if self.v is None:
                print("Is a valuation of definition")
                return type(self)(d=self.d, s=self.s, v=other)
            else:
                print("Is a revaluation of resolution")
                return type(self)(d=self.d, s=self.s, v=self.v * other)
        elif isinstance(other, type(self)) or issubclass(other, type(self)):
            if self.s == other.s:
                if self.v is None and other.v is None:
                    print("Is a definition")
                    return type(self)(d=self.d + other.d, s=self.s)
                else:
                    print("Is a resolution")
                    return type(self)(d=self.d + other.d, s=self.s, v=self.v * other.v)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            if self.v is None:
                print("Is a valuation of definition")
                return type(self)(d=self.d, s=self.s, v=other)
            else:
                print("Is a revaluation of resolution")
                return type(self)(d=self.d, s=self.s, v=self.v * other)
        elif isinstance(other, type(self)) or issubclass(other, type(self)):
            if self.s == other.s:
                if self.v is None and other.v is None:
                    print("Is a definition")
                    return type(self)(d=self.d + other.d, s=self.s)
                else:
                    print("Is a resolution")
                    return type(self)(d=self.d + other.d, s=self.s, v=self.v * other.v)


meters = BaseUnit()
