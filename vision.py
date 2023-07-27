from dataclasses import dataclass, field


class MetaMath(type):
    def __mul__(cls1, cls2):
        if (
            hasattr(cls1, "p")
            and hasattr(cls2, "p")
            and isinstance(cls1.p, list)
            and isinstance(cls2.p, list)
        ):
            multiplied_p = [x * y for x, y in zip(cls1.p, cls2.p)]
            class_name = f"{cls1.__name__}Times{cls2.__name__}"

            # Define a new class with frozen and slots set to True
            new_class = type(class_name, (), {"p": multiplied_p})
            new_class = dataclass(frozen=True, slots=True)(new_class)
            return new_class
        else:
            raise TypeError("Both classes must have a 'p' list attribute.")


@dataclass(frozen=True, slots=True)
class A(metaclass=MetaMath):
    p: list[int] = field(default_factory=lambda: [1, 2, 3])


@dataclass(frozen=True, slots=True)
class B(metaclass=MetaMath):
    p: list[int] = field(default_factory=lambda: [2, 2, 2])


if __name__ == "__main__":
    # Non-instantiated class multiplication
    C = A * B
    print(C.p)  # Output: [2, 4, 6]
