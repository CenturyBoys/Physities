import pytest

from physities.src.dimension import Dimension
from physities.src.scale.basescale import BaseScale, ScaleConvertor
from physities.src.enums.base_units import BaseDimensions


@pytest.mark.unit
class TestBaseScale:
    @staticmethod
    def test_call_method(dimensions_group_test, conversion_tuple_test):
        for dimension_tuple in dimensions_group_test:
            dimension = dimension_tuple
            conversion_tuple = conversion_tuple_test
            value = 10
            resize = 1
            instance = BaseScale.__call__(
                BaseScale,
                value=value,
                dimension=dimension,
                conversion_tuple=conversion_tuple,
                resize=resize,
            )
            assert isinstance(instance, ScaleConvertor)
            assert instance.dimension == dimension_tuple
            assert instance.conversion_tuple == conversion_tuple
            assert instance.value == value
            assert instance.resize == resize

    @staticmethod
    def test_new_function(dimensions_group_test, conversion_tuple_test):
        for dimension_tuple in dimensions_group_test:
            dimension = dimension_tuple
            conversion_tuple = conversion_tuple_test
            value = 10
            resize = 1
            base_scale = BaseScale
            base_scale.dimension = dimension
            base_scale.conversion_tuple = conversion_tuple
            base_scale.resize = resize
            instance = base_scale.new(value=value)
            assert isinstance(instance, ScaleConvertor)
            assert instance.dimension == dimension_tuple
            assert instance.conversion_tuple == conversion_tuple
            assert instance.value == value
            assert instance.resize == resize

    @staticmethod
    def test_addition(base_scales):
        tests = [
            (base_scales[0], base_scales[2]),
            (base_scales[0], 1),
            (0.5, base_scales[0]),
        ]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] + test[1]
            assert str(error.value) == "Scales offset are not allowed yet."

    @staticmethod
    def test_subtraction(base_scales):
        tests = [
            (base_scales[0], base_scales[2]),
            (base_scales[0], 1),
            (0.5, base_scales[0]),
        ]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] - test[1]
            assert str(error.value) == "Scales offset are not allowed yet."

    @staticmethod
    def test_multiplication_result_type(base_scales):
        for base_scale_1 in base_scales:
            for base_scale_2 in base_scales:
                result = base_scale_1 * base_scale_2
                assert isinstance(result, BaseScale)

    @staticmethod
    def test_multiplication_scalar_monodimensional(base_scales):
        base_scale = base_scales[0]
        result = 4 * base_scale

        index = base_scale.dimension.get_dimensions().pop()
        from_base_value = result.conversion_tuple[index]
        assert from_base_value == 4

    @staticmethod
    def test_multiplication_scalar_multidimensional(base_scales):
        base_scale = base_scales[2]
        result = 3 * base_scale
        assert result.resize == 3
        assert result.dimension == base_scale.dimension
        assert result.conversion_tuple == base_scale.conversion_tuple

    @staticmethod
    def test_multiplication_monodimensional_multidimensional_with_annulled_dimension(
        base_scales,
    ):
        base_scale_0 = base_scales[0]
        base_scale_1 = base_scales[2]
        aux_1 = 4 * base_scale_0
        result = base_scale_1 * aux_1

        assert result.resize == 4
        assert result.dimension == aux_1.dimension + base_scale_1.dimension
        assert result.conversion_tuple == (1, 1, 1, 1, 1)

    @staticmethod
    def test_multiplication_monodimensional_monodimensional(base_scales):
        base_scale = base_scales[0]
        aux_1 = 5 * base_scale
        aux_2 = (1 / 5) * base_scale
        result = aux_1 * aux_2
        for i in result.conversion_tuple:
            assert i == 1
        assert len(result.dimension.get_dimensions()) == 1
        assert result.resize == 1

    @staticmethod
    def test_multiplication_multidimensional_multidimensional(base_scales):
        base_scale_1 = base_scales[1]
        base_scale_2 = base_scales[2]
        aux_1 = 3 * base_scale_1
        result = base_scale_2 * aux_1

        for i in result.conversion_tuple:
            assert i == 1
        assert result.resize == 3
        assert result.dimension == base_scale_2.dimension + base_scale_1.dimension

    @staticmethod
    def test_multiplication_two_same_instances(base_scales):
        base_scale = base_scales[1]
        result = base_scale * base_scale

        assert result.resize == 1
        assert result.dimension == 2 * base_scale.dimension
        assert result.conversion_tuple == base_scale.conversion_tuple

    @staticmethod
    def test_multiplication_commutativity(base_scales):
        base_scale_0 = base_scales[0]
        base_scale_2 = base_scales[2]
        result_1 = base_scale_0 * base_scale_2
        result_2 = base_scale_2 * base_scale_0
        result_3 = 7 * base_scale_0
        result_4 = base_scale_0 * 7

        assert result_1 == result_2
        assert result_3 == result_4

    @staticmethod
    def test_division_same_dimension(base_scales):
        base_scale = base_scales[1]
        aux_1 = 3 * base_scale
        result = base_scale / aux_1

        for i in result.conversion_tuple:
            assert i == 1
        assert result.dimension == Dimension.new_instance(
            dimensions_tuple=tuple(0 for i in BaseDimensions)
        )
        assert result.resize == 1 / 3

    @staticmethod
    def test_division_scalar_by_monodimensional(base_scales):
        base_scale = base_scales[0]
        aux_1 = 4 * base_scale
        result = 2 / aux_1

        index = base_scale.dimension.get_dimensions().pop()
        from_base_value = result.conversion_tuple[index]
        assert from_base_value == 0.5
        assert result.dimension == aux_1.dimension * -1
        assert result.resize == 1

    @staticmethod
    def test_division_scalar_by_multidimensional(base_scales):
        base_scale = base_scales[2]
        aux_1 = 4 * base_scale
        result = 2 / aux_1

        for i in BaseDimensions:
            assert result.conversion_tuple[i] == 1 / base_scale.conversion_tuple[i]
        assert result.dimension == aux_1.dimension * -1
        assert result.resize == 2 / aux_1.resize

    @staticmethod
    def test_division_multidimensional_by_scalar(base_scales):
        base_scale = base_scales[2]
        aux_1 = 4 * base_scale
        result = aux_1 / 2

        for i in BaseDimensions:
            assert result.conversion_tuple[i] == base_scale.conversion_tuple[i]
        assert result.dimension == aux_1.dimension
        assert result.resize == aux_1.resize / 2

    @staticmethod
    def test_division_different_dimension(base_scales):
        base_scale_0 = base_scales[0]
        base_scale_1 = base_scales[2]
        aux_1 = 4 * base_scale_0
        print()
