from tests.fixtures import *


@pytest.mark.unit
class TestScale:
    @staticmethod
    def test_instantiation(dimension_sample, from_base_scale_conversion_sample):
        base_scale_conversions = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        obj_scale = Scale(
            dimension=dimension_sample,
            rescale_value=1,
            from_base_scale_conversions=base_scale_conversions,
        )
        obj_scale_2 = Scale.new()
        obj_scale_3 = Scale.new(dimension=dimension_sample)
        obj_scale_4 = Scale.new(rescale_value=3)
        obj_scale_5 = Scale.new(
            from_base_scale_conversions=from_base_scale_conversion_sample
        )
        obj_scale_6 = Scale.new(
            dimension=dimension_sample,
            rescale_value=3,
            from_base_scale_conversions=(-1, 0, 1, 2, 3, 4, 5),
        )
        assert isinstance(obj_scale, Scale)
        assert obj_scale.dimension == dimension_sample
        assert obj_scale.rescale_value == 1.0
        assert obj_scale.from_base_scale_conversions == base_scale_conversions

        assert isinstance(obj_scale_2, Scale)
        assert obj_scale_2.dimension == Dimension.new_dimensionless()
        assert obj_scale_2.from_base_scale_conversions == base_scale_conversions
        assert obj_scale_2.rescale_value == 1.0

        assert isinstance(obj_scale_3, Scale)
        assert obj_scale_3.dimension == dimension_sample
        assert obj_scale_3.from_base_scale_conversions == base_scale_conversions
        assert obj_scale_3.rescale_value == 1.0

        assert isinstance(obj_scale_4, Scale)
        assert obj_scale_4.dimension == Dimension.new_dimensionless()
        assert obj_scale_4.from_base_scale_conversions == base_scale_conversions
        assert obj_scale_4.rescale_value == 3

        assert isinstance(obj_scale_5, Scale)
        assert obj_scale_5.dimension == Dimension.new_dimensionless()
        assert (
            obj_scale_5.from_base_scale_conversions == from_base_scale_conversion_sample
        )
        assert obj_scale_5.rescale_value == 1.0

        assert isinstance(obj_scale_6, Scale)
        assert obj_scale_6.dimension == dimension_sample
        assert (
            obj_scale_6.from_base_scale_conversions == from_base_scale_conversion_sample
        )
        assert obj_scale_6.rescale_value == 3

    @staticmethod
    def test_equality(dimension_sample, velocity_dimension):
        scale_1 = Scale.new(dimension=dimension_sample, rescale_value=3)
        scale_2 = Scale.new(
            dimension=dimension_sample,
            from_base_scale_conversions=(1.0, 2, 3, 4, 5, 6, 7),
            rescale_value=3,
        )
        scale_3 = Scale.new(
            from_base_scale_conversions=(1.0, 2, 3, 4, 5, 6, 7), rescale_value=3
        )
        scale_4 = Scale.new(dimension=dimension_sample, rescale_value=6)
        scale_5 = Scale.new(dimension=dimension_sample, rescale_value=3)
        scale_6 = Scale.new(
            dimension=velocity_dimension,
            from_base_scale_conversions=(1000, 1, 1, 1, 1, 1, 1),
        )
        scale_7 = Scale.new(
            dimension=velocity_dimension,
            from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
            rescale_value=1000,
        )
        # check exactly same params
        assert scale_1 == scale_5
        # check different from_base_scale_conversions
        assert scale_1 != scale_2
        # check different dimension
        assert scale_2 != scale_3
        # check different rescale_value
        assert scale_4 != scale_5
        # check same conversion_factor different scales
        assert scale_6 == scale_7

    @staticmethod
    def test_multiplication(
        second_scale,
        second_inverse_scale,
        joule_scale,
        cal_scale,
        newton_scale,
        meter_scale,
        kilometer_scale,
    ):
        # composition check
        assert newton_scale * meter_scale == joule_scale
        # check multidimensional scale stretch and compression
        assert joule_scale * 4.184 == cal_scale
        # check unidimensional scale stretch and compression
        assert 1000 * meter_scale == kilometer_scale
        # check scale annulation
        assert second_scale * second_inverse_scale == Scale.new()
        # check multidimensional to unit scale stretch/compression
        assert (
            1000 * (meter_scale * second_inverse_scale) * second_scale
            == kilometer_scale
        )

    @staticmethod
    def test_multiplication_invalid(joule_scale):
        class A:
            pass

        invalid_values = [(), {}, A, []]
        for i in invalid_values:
            with pytest.raises(TypeError) as error:
                joule_scale * i
            assert (
                str(error.value)
                == f"{Scale} can only be multiplied by {Scale}, {int} or {float}. This operation is not implemented for {type(i)}."
            )

    @staticmethod
    def test_division(
        second_scale,
        second_inverse_scale,
        joule_scale,
        cal_scale,
        meter_scale,
        kilometer_scale,
    ):
        # check scale unidimensional inversion
        assert 1 / second_scale == second_inverse_scale
        # check scale multidimensional inversion
        assert 1 / (meter_scale / second_scale) == second_scale / meter_scale
        # check scale annulation
        assert second_scale / second_scale == Scale.new()
        # check unidimensional scale stretch/compression
        assert kilometer_scale / 1000 == meter_scale
        # check multidimensional to unit scale stretch/compression
        assert (
            meter_scale / second_scale
        ) / second_inverse_scale == kilometer_scale / 1000
        # check check multidimensional scale stretch/compression
        # TODO floating precision correction
        assert cal_scale / 4.184 == joule_scale

    @staticmethod
    def test_division_invalid(joule_scale):
        class A:
            pass

        invalid_values = [(), {}, A, []]
        for i in invalid_values:
            with pytest.raises(TypeError) as error:
                joule_scale / i
            with pytest.raises(TypeError) as error2:
                i / joule_scale
            assert (
                str(error.value)
                == f"{Scale} can only be divided by {Scale}, {int} or {float}. This operation is not implemented for {type(i)}."
            )
            assert (
                str(error2.value)
                == f"{Scale} can only divide {Scale}, {int} or {float}. This operation is not implemented for {type(i)}."
            )

    @staticmethod
    def test_power(
        meter_scale,
        kilometer_scale,
        kilometer_square_scale,
        second_scale,
        kilometer_per_second_square_scale,
    ):
        # check multidimensional scale stretch/compression
        assert (1000 * (meter_scale / second_scale)) ** 2 == 1000000 * (
            meter_scale / second_scale
        ) ** 2
        # check multidimensional scale powered specific
        assert (kilometer_scale / second_scale) ** 2 == kilometer_per_second_square_scale
        # check unidimensional scale powered
        assert kilometer_scale**2 == kilometer_square_scale
        # check unidimensional scale powered stretch/compression
        assert 1000000 * meter_scale**2 == kilometer_square_scale

    @staticmethod
    def test_power_invalid(meter_scale, second_scale):
        class A:
            pass
        invalid_values = [second_scale, [], {}, (), A]
        for i in invalid_values:
            with pytest.raises(TypeError) as error:
                meter_scale ** i
            assert str(error.value) == f"{Scale} can only be powered by {int} or {float}. This operation is not implemented for {type(i)}."
