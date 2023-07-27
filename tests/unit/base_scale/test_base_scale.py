import pytest

from physities.src.entities.scale.basescale import BaseScale, Scale
from tests.fixtures import dimensions_group_test, conversion_tuple_test, base_scales


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
            assert isinstance(instance, Scale)
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
            assert isinstance(instance, Scale)
            assert instance.dimension == dimension_tuple
            assert instance.conversion_tuple == conversion_tuple
            assert instance.value == value
            assert instance.resize == resize

    @staticmethod
    def test_addition(base_scales):
        tests = [(base_scales[0], base_scales[2]), (base_scales[0], 1), (0.5, base_scales[0])]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] + test[1]
            assert str(error.value) == "Scales offset are not allowed yet."

    @staticmethod
    def test_subtraction(base_scales):
        tests = [(base_scales[0], base_scales[2]), (base_scales[0], 1), (0.5, base_scales[0])]
        for test in tests:
            with pytest.raises(TypeError) as error:
                result = test[0] - test[1]
            assert str(error.value) == "Scales offset are not allowed yet."

    @staticmethod
    def test_multiplication(base_scales):
        base_scale_0 = base_scales[0]
        base_scale_1 = base_scales[1]
        base_scale_2 = base_scales[2]


        result_0 = 4*base_scale_0
        result_1 = 3 * base_scale_2
        result_2 = base_scale_1 * result_0
        result_3 = base_scale_1*base_scale_2
        result_4 = base_scale_1*base_scale_1
        result_5 = base_scale_2 * 3
        results = [result_0, result_1, result_2, result_3, result_4, result_5]

        for result in results:
            assert isinstance(result, BaseScale)
        assert result_0.resize == 1

        index = result_0.dimension.get_dimensions().pop()
        from_to_dict = result_0.conversion_tuple[index]
        assert from_to_dict.get("from_base") == 4
        assert from_to_dict.get("to_base") == 0.25

        assert result_1.resize == 3
        assert result_1.dimension == base_scale_2.dimension
        assert result_1.conversion_tuple == base_scale_2.conversion_tuple

        print()


