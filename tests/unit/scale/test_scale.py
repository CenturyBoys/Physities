import pytest

from physities.src.dimension import BaseDimension, Dimension
from physities.src.scale import Scale
from tests.fixtures import dimension_sample, from_base_conversion_sample


@pytest.mark.unit
class TestScale:

    @staticmethod
    def test_instantiation_success(dimension_sample, from_base_conversion_sample):
        base_conversions = (1., 1., 1., 1., 1., 1., 1.)
        obj_scale = Scale(
            dimension=dimension_sample,
            rescale_value=1,
            from_base_conversions=base_conversions
        )
        obj_scale_2 = Scale.new()
        obj_scale_3 = Scale.new(dimension=dimension_sample)
        obj_scale_4 = Scale.new(rescale_value=3)
        obj_scale_5 = Scale.new(from_base_conversions=from_base_conversion_sample)
        obj_scale_6 = Scale.new(
            dimension=dimension_sample,
            rescale_value=3,
            from_base_conversions=(-1, 0, 1, 2, 3, 4, 5)
        )
        assert isinstance(obj_scale, Scale)
        assert obj_scale.dimension == dimension_sample
        assert obj_scale.rescale_value == 1.
        assert obj_scale.from_base_conversions == base_conversions

        assert isinstance(obj_scale_2, Scale)
        assert obj_scale_2.dimension == Dimension.new_dimensionless()
        assert obj_scale_2.from_base_conversions == base_conversions
        assert obj_scale_2.rescale_value == 1.

        assert isinstance(obj_scale_3, Scale)
        assert obj_scale_3.dimension == dimension_sample
        assert obj_scale_3.from_base_conversions == base_conversions
        assert obj_scale_3.rescale_value == 1.

        assert isinstance(obj_scale_4, Scale)
        assert obj_scale_4.dimension == Dimension.new_dimensionless()
        assert obj_scale_4.from_base_conversions == base_conversions
        assert obj_scale_4.rescale_value == 3

        assert isinstance(obj_scale_5, Scale)
        assert obj_scale_5.dimension == Dimension.new_dimensionless()
        assert obj_scale_5.from_base_conversions == from_base_conversion_sample
        assert obj_scale_5.rescale_value == 1.

        assert isinstance(obj_scale_6, Scale)
        assert obj_scale_6.dimension == dimension_sample
        assert obj_scale_6.from_base_conversions == from_base_conversion_sample
        assert obj_scale_6.rescale_value == 3

    @staticmethod
    def test_invalid_dimension_type_instantiation(from_base_conversion_sample):
        invalid_dimensions = [[], {}, 1, 0.0, (1,2,3,4,5,6,7)]
        for invalid_dimension in invalid_dimensions:
            with pytest.raises(TypeError) as error:
                Scale(
                    dimension=invalid_dimension,
                    rescale_value=1,
                    from_base_conversions=from_base_conversion_sample
                )
            with pytest.raises(TypeError) as error2:
                Scale.new(dimension=invalid_dimension)
            assert (
                str(error.value) == f"Class 'Scale' type error:\n Wrong type for dimension: {Dimension} != '{type(invalid_dimension)}'"
            )
            assert (
                str(error2.value) == f"Class 'Scale' type error:\n Wrong type for dimension: {Dimension} != '{type(invalid_dimension)}'"
            )

    @staticmethod
    def test_invalid_rescale_value_type_instantiation(dimension_sample, from_base_conversion_sample):
        invalid_rescale_values = [[], (1,), {}]
        for invalid_rescale_value in invalid_rescale_values:
            with pytest.raises(TypeError) as error:
                Scale(
                    dimension=dimension_sample,
                    rescale_value=invalid_rescale_value,
                    from_base_conversions=from_base_conversion_sample
                )
            with pytest.raises(TypeError) as error2:
                Scale.new(rescale_value=invalid_rescale_value)
            assert (
                str(error.value) == f"Class 'Scale' type error:\n Wrong type for rescale_value: {float | int} != '{type(invalid_rescale_value)}'"
            )
            assert (
                str(error2.value) == f"Class 'Scale' type error:\n Wrong type for rescale_value: {float | int} != '{type(invalid_rescale_value)}'"
            )

    @staticmethod
    def test_invalid_from_base_conversions_type_instantiation(dimension_sample):
        invalid_from_base_conversions_list = [1, 2., {}, [1,2,3,4,5,6,7]]
        for invalid_from_base_conversions in invalid_from_base_conversions_list:
            with pytest.raises(TypeError) as error:
                Scale(
                    dimension=dimension_sample,
                    rescale_value=1,
                    from_base_conversions=invalid_from_base_conversions
                )
            with pytest.raises(TypeError) as error2:
                Scale.new(from_base_conversions=invalid_from_base_conversions)
            assert (
                str(error.value) == f"Class 'Scale' type error:\n Wrong type for from_base_conversions: {tuple[float | int, float | int, float | int, float | int, float | int, float | int, float | int]} != '{type(invalid_from_base_conversions)}'"
            )
            assert (
                str(error.value) == f"Class 'Scale' type error:\n Wrong type for from_base_conversions: {tuple[float | int, float | int, float | int, float | int, float | int, float | int, float | int]} != '{type(invalid_from_base_conversions)}'"
            )

    # @staticmethod
    # test_