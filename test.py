# class MetaClass(type):
#     def __mul__(cls, other):
#         result_name = f"{cls.__name__}MultipliedBy{other.__name__}"
#         result_attrs = {"value": cls.value * other.value}
#         result_class = type(result_name, (ClassA,), result_attrs)
#         return result_class
#
#     def __call__(cls, *args, **kwargs):
#         # This method creates an instance of the dynamically generated class
#         instance = cls.__new__(cls)
#         instance.__init__(*args, **kwargs)
#         return instance
#
#
# class ClassA(metaclass=MetaClass):
#     value = None
#
#     def __init__(self, value):
#         self.value = value
#
#     def __repr__(self):
#         return f"{self.__class__.__name__}({self.value})"
#
#
# if __name__ == "__main__":
#     # Set the value for ClassA
#     ClassA.value = 5
#
#     # Example usage without instantiating ClassA
#     result_class = ClassA * ClassA
#     print(result_class)  # Output: ClassAMultipliedByClassA(25)
#
#     # Create an instance of result_class using the __call__ method
#     instance = result_class(10)
#     print(instance)  # Output: ClassAMultipliedByClassA(10)


def custom_class_name(class_name):
    def class_decorator(cls):
        class CustomClass(cls):
            def __repr__(self):
                return f"{class_name}({self.value})"

        return CustomClass

    return class_decorator


@custom_class_name("result_class")
class ClassA:
    value = None

    def __init__(self, value):
        self.value = value


if __name__ == "__main__":
    # Set the value for ClassA
    ClassA.value = 5

    # Example usage without instantiating ClassA
    result_class = ClassA * ClassA
    print(result_class)  # Output: result_class(25)

    # Create an instance of result_class using the __call__ method
    instance = result_class(10)
    print(instance)  # Output: result_class(10)
