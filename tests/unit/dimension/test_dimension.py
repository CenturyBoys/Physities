import pytest as pytest

from physities.src.dimension import Dimension
from physities.src.enums.base_units import BaseDimensions


@pytest.mark.unit
class TestDimension:
    @staticmethod
    def test_instantiation_success():
        obj_dimension = Dimension(dimensions_tuple=tuple(i for i in BaseDimensions))
        assert isinstance(obj_dimension, Dimension)

    @staticmethod
    def test_invalid_type_instantiation():
        invalid_tuples = [[], {}, 1, 0.0]
        for invalid_tuple in invalid_tuples:
            with pytest.raises(TypeError) as error:
                obj_dimension = Dimension(dimensions_tuple=invalid_tuple)
            assert (
                str(error.value)
                == f"dimensions_tuple is not of the type {type(tuple)}."
            )

    @staticmethod
    def test_invalid_length_instantiation():
        invalid_tuples = [(), (1,), (1, 2, 3), (1, 2, 3, 4, 5, 6, 7, 8)]
        for invalid_tuple in invalid_tuples:
            with pytest.raises(ValueError) as error:
                obj_dimension = Dimension(dimensions_tuple=invalid_tuple)
            assert (
                str(error.value)
                == f"Invalid length of tuple. Expected {len(BaseDimensions)}, but got {len(invalid_tuple)}."
            )

    @staticmethod
    def test_new_methods_invalid_power():
        invalid_powers = [[], "1", {}, ()]
        new_methods = [
            Dimension.new_time,
            Dimension.new_length,
            Dimension.new_amount,
            Dimension.new_mass,
            Dimension.new_temperature,
        ]
        for method in new_methods:
            for invalid_power in invalid_powers:
                with pytest.raises(TypeError) as error:
                    result = method(power=invalid_power)
                assert (
                    str(error.value) == "The exponentiation must be a int or a float."
                )

    @staticmethod
    def test_new_methods_success():
        new_methods = [
            Dimension.new_time,
            Dimension.new_length,
            Dimension.new_amount,
            Dimension.new_mass,
            Dimension.new_temperature,
        ]
        expected_tuple = [
            BaseDimensions.TIME,
            BaseDimensions.LENGTH,
            BaseDimensions.AMOUNT,
            BaseDimensions.MASS,
            BaseDimensions.TEMPERATURE,
        ]
        for index in range(len(new_methods)):
            expec_dim_tuple = [0 for i in BaseDimensions]
            dimension = new_methods[index](power=3.5)
            expec_dim_tuple[expected_tuple[index]] = 3.5
            assert type(dimension) == Dimension
            assert dimension.dimensions_tuple == tuple(expec_dim_tuple)

    @staticmethod
    def test_equality():
        class A(Dimension):
            pass

        class B:
            dimensions_tuple = (1, 2, 3, 4, 5)

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 2, 3, 4, 5))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(1, 2, 3, 4, 5))
        dimension_3 = A.new_instance(dimensions_tuple=(1, 2, 3, 4, 5))
        dimension_4 = B()
        assert dimension_2 == dimension_1
        assert dimension_3 == dimension_1
        assert dimension_2 == dimension_3
        assert dimension_4 != dimension_1

    @staticmethod
    def test_addition():
        class A(Dimension):
            pass

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 2, 3, 4, 5))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(5, 4, 3, 2, 1))
        dimension_3 = A.new_instance(dimensions_tuple=(5, 4, 3, 2, 1))
        dimension_4 = Dimension.new_instance(dimensions_tuple=(-1, -2, -3, -4, -5))
        dimension_result_1 = dimension_1 + dimension_2
        dimension_result_2 = dimension_2 + dimension_1
        dimension_result_3 = dimension_3 + dimension_1
        dimension_result_4 = dimension_1 + dimension_4
        assert isinstance(dimension_result_1, Dimension)
        assert dimension_result_1.dimensions_tuple == (6, 6, 6, 6, 6)
        assert isinstance(dimension_result_2, Dimension)
        assert dimension_result_2.dimensions_tuple == (6, 6, 6, 6, 6)
        assert dimension_result_4.dimensions_tuple == (0, 0, 0, 0, 0)
        assert dimension_result_3.dimensions_tuple == (6, 6, 6, 6, 6)

    @staticmethod
    def test_addition_invalid():
        class B:
            dimensions_tuple = (1, 2, 3, 4, 5)

        dimension_1 = B()
        dimension_2 = Dimension.new_instance(dimensions_tuple=(5, 4, 3, 2, 1))
        tests = [(dimension_1, dimension_2), (dimension_2, 1), (dimension_2, [])]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] + test[1]
            assert (
                str(error.value)
                == "Dimension only allow addition between same instance."
            )

    @staticmethod
    def test_subtraction():
        class A(Dimension):
            pass

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        dimension_3 = A.new_instance(dimensions_tuple=(2, 1, 1, 1, 1))
        dimension_result_1 = dimension_1 - dimension_2
        dimension_result_2 = dimension_2 - dimension_1
        dimension_result_3 = dimension_3 - dimension_1
        assert isinstance(dimension_result_1, Dimension)
        assert dimension_result_1.dimensions_tuple == (0, 0, 0, 0, 2)
        assert isinstance(dimension_result_2, Dimension)
        assert dimension_result_2.dimensions_tuple == (0, 0, 0, 0, -2)
        assert dimension_result_3.dimensions_tuple == (1, 0, 0, 0, 0)

    @staticmethod
    def test_subtraction_invalid():
        class B:
            dimensions_tuple = (1, 2, 3, 4, 5)

        dimension_1 = B()
        dimension_2 = Dimension.new_instance(dimensions_tuple=(5, 4, 3, 2, 1))
        tests = [(dimension_1, dimension_2), (dimension_2, 1), (dimension_2, [])]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] - test[1]
            assert (
                str(error.value)
                == "Dimension only allow subtraction between same instance."
            )

    @staticmethod
    def test_multiplication():
        class A(Dimension):
            pass

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        dimension_3 = A.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        result_1 = -3 * dimension_1
        result_2 = dimension_2 * -3
        result_3 = 0.5 * dimension_2
        result_4 = -1.24 * dimension_3
        assert result_1.dimensions_tuple == (-3, -3, -3, -3, -3)
        assert result_2.dimensions_tuple == (-3, -3, -3, -3, 3)
        assert result_3.dimensions_tuple == (0.5, 0.5, 0.5, 0.5, -0.5)
        assert result_4.dimensions_tuple == (-1.24, -1.24, -1.24, -1.24, 1.24)

    @staticmethod
    def test_multiplication_invalid():
        class B:
            dimensions_tuple = (1, 2, 3, 4, 5)

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        dimension_3 = B()
        tests = [
            (dimension_1, dimension_2),
            (dimension_1, dimension_3),
            (dimension_1, ()),
            (dimension_3, dimension_1),
        ]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] * test[1]
            assert (
                str(error.value)
                == "Dimension only allow multiplication with int or floats."
            )

    @staticmethod
    def test_division():
        class A(Dimension):
            pass

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_3 = A.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        result_1 = dimension_1 / 5
        result_2 = 5 / dimension_1
        result_3 = dimension_3 / 4
        result_4 = 4.35 / dimension_3
        assert result_1.dimensions_tuple == (0.2, 0.2, 0.2, 0.2, 0.2)
        assert result_2.dimensions_tuple == (5, 5, 5, 5, 5)
        assert result_3.dimensions_tuple == (0.25, 0.25, 0.25, 0.25, -0.25)
        assert result_4.dimensions_tuple == (4.35, 4.35, 4.35, 4.35, -4.35)

    @staticmethod
    def test_division_invalid():
        class B:
            dimensions_tuple = (1, 2, 3, 4, 5)

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        dimension_3 = B()
        tests = [
            (dimension_1, dimension_2),
            (dimension_1, dimension_3),
            (dimension_1, ()),
            (dimension_3, dimension_1),
        ]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] / test[1]
            assert str(error.value) == "Dimension only allow division by int or floats."

    @staticmethod
    def test_pow_invalid():
        class A(Dimension):
            pass

        class B:
            dimensions_tuple = (1, 2, 3, 4, 5)

        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_2 = A.new_instance(dimensions_tuple=(1, 1, 1, 1, -1))
        dimension_3 = B()
        tests = [
            (dimension_1, dimension_2),
            (dimension_2, dimension_1),
            (dimension_1, dimension_3),
            (dimension_2, 1),
        ]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] ** test[1]
            assert str(error.value) == "Exponentiation with Dimension is not allowed."

    @staticmethod
    def test_show_dimension():
        dimension_1 = Dimension.new_instance(dimensions_tuple=(1, 1, 1, 1, 1))
        dimension_2 = Dimension.new_instance(dimensions_tuple=(-1, -1, -1, -1, -1))
        dimension_3 = Dimension.new_instance(dimensions_tuple=(19, 0.75, 4, -0.3333, 1))
        assert dimension_1.show_dimension() == "L¹m¹T¹t¹N¹"
        assert dimension_2.show_dimension() == "1 / L¹m¹T¹t¹N¹"
        assert dimension_3.show_dimension() == "L¹⁹m⁰ˑ⁷⁵T⁴N¹ / t⁰ˑ³³³³"
