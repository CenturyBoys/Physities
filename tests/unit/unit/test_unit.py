from physities.src.unit import Meter, Second, Minute, Kilometer
from tests.fixtures import *


@pytest.mark.unit
class TestMetaUnit:

    @staticmethod
    def test_class_definition_invalid_scale():
        class A:
            pass

        invalid_values = [[], {}, (1, 2, 3, 4, 5, 6, 7), A, A()]
        for value in invalid_values:
            # check for each value
            with pytest.raises(TypeError) as error:
                class B(Unit):
                    scale = value
            assert str(error.value) == f"Subclass of {Unit} must define class attribute 'scale' of type {Scale}."

        # check without scale
        with pytest.raises(TypeError) as error:
            class C(Unit):
                pass

    @staticmethod
    def test_equality(kilometer_unit, inverse_second_unit):

        class Kilometer2(Unit):
            scale = Scale.new(
                dimension=Dimension.new_length(),
                from_base_scale_conversions=(1000, 1., 1., 1., 1., 1., 1.)
            )
            value = None

        class OtherKilometer(kilometer_unit):
            pass

        # check inheritance equality
        assert OtherKilometer == kilometer_unit
        # check same content classes
        assert Kilometer2 == OtherKilometer
        # check different dimensions
        assert kilometer_unit != inverse_second_unit
        # check different scale
        assert kilometer_unit != Meter

    @staticmethod
    def test_multiplication(
        inverse_second_unit,
        meter_per_second_unit,
        meter_per_second_scale,
    ):
        speed_unit = Meter*inverse_second_unit
        stretched_speed_unit = 50 * speed_unit
        kilometer_unit = 1000*Meter
        meter_unit = speed_unit * Second
        kilometer_unit_2 = (1000 * speed_unit) * Second

        # check composition
        assert speed_unit == meter_per_second_unit
        # check multidimensional scale stretch and compression
        assert stretched_speed_unit.scale.from_base_scale_conversions == meter_per_second_scale.from_base_scale_conversions
        assert stretched_speed_unit.scale.rescale_value == 50
        # check unidimensional scale stretch and compression
        assert kilometer_unit.scale.from_base_scale_conversions[BaseDimension.LENGTH] == 1000
        assert kilometer_unit.scale.rescale_value == 1.
        # check scale annulation
        assert meter_unit == Meter
        # check multidimensional to unit scale stretch/compression
        assert kilometer_unit_2 == kilometer_unit

    @staticmethod
    def test_multiplication_invalid(meter_per_second_unit):
        class A:
            pass
        invalid_values = [[], {}, A, (1, 2)]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                Meter * value
            with pytest.raises(TypeError) as error_2:
                meter_per_second_unit * value
            assert str(error_1.value) == f"{Meter} only allows multiplication by {Meter}, {int}, and {float}"
            assert str(error_2.value) == f"{meter_per_second_unit} only allows multiplication by {meter_per_second_unit}, {int}, and {float}"

    @staticmethod
    def test_division(
            inverse_second_unit,
            meter_per_second_unit,
            inverse_meter_per_second_unit,
            kilometer_per_second_unit
    ):
        inverse_second_unit_2 = 1/Second
        inverse_meter_per_second_unit_2 = 1 / meter_per_second_unit
        second_2 = Minute / 60
        meter_per_second_unit_2 = kilometer_per_second_unit / 1000
        inverse_second_unit_3 = meter_per_second_unit / Meter
        # check scale unidimensional inversion
        assert inverse_second_unit_2 == inverse_second_unit
        # check scale multidimensional inversion
        assert inverse_meter_per_second_unit_2 == inverse_meter_per_second_unit
        # check scale annulation
        assert inverse_second_unit_3 == inverse_second_unit
        # check unidimensional scale stretch/compression
        assert second_2 == Second
        # check multidimensional to unit scale stretch/compression
        assert meter_per_second_unit_2 == meter_per_second_unit
        # check multidimensional to unidimensional rescale
        assert inverse_second_unit_3 == inverse_second_unit

    @staticmethod
    def test_division_invalid(meter_per_second_unit):
        class A:
            pass
        invalid_values = [[], {}, A, (1, 2)]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                Meter / value
            with pytest.raises(TypeError) as error_2:
                value / Meter
            with pytest.raises(TypeError) as error_3:
                meter_per_second_unit / value
            with pytest.raises(TypeError) as error_4:
                value / meter_per_second_unit
            assert str(error_1.value) == f"{Meter} only allows division by {Meter}, {int}, and {float}"
            assert str(error_2.value) == f"{Meter} can divide only {Meter}, {int} and {float}"
            assert str(error_3.value) == f"{meter_per_second_unit} only allows division by {meter_per_second_unit}, {int}, and {float}"
            assert str(error_4.value) == f"{meter_per_second_unit} can divide only {meter_per_second_unit}, {int} and {float}"

    @staticmethod
    def test_power(meter_per_second_unit, inverse_meter_per_second_unit, kilometer_square_unit, kilometer_per_second_unit, kilometer_per_second_square_unit):
        square_kilometer = Kilometer ** 2
        kilometer_per_second_square_unit_2 = kilometer_per_second_unit ** 2
        inverse_meter_per_second_unit_2 = meter_per_second_unit ** -1
        # check inverse power
        assert inverse_meter_per_second_unit_2 == inverse_meter_per_second_unit
        # check unidimensional power
        assert square_kilometer == kilometer_square_unit
        # check multidimensional power
        assert kilometer_per_second_square_unit_2 == kilometer_per_second_square_unit

    @staticmethod
    def test_power_invalid(meter_per_second_unit):
        class A:
            pass

        invalid_values = [[], {}, A, (1, 2)]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                Meter ** value
            with pytest.raises(TypeError) as error_2:
                meter_per_second_unit ** value
            assert str(error_1.value) == f"{Meter} can only be powered by {int} and {float}"
            assert str(error_2.value) == f"{meter_per_second_unit} can only be powered by {int} and {float}"

    @staticmethod
    def test_addition_invalid(meter_per_second_unit):
        class A:
            pass
        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                Meter + value
            with pytest.raises(TypeError) as error_2:
                meter_per_second_unit + value
            assert str(error_1.value) == f"Units with translated scale are not allowed yet."
            assert str(error_2.value) == f"Units with translated scale are not allowed yet."

    @staticmethod
    def test_subtraction_invalid(meter_per_second_unit):
        class A:
            pass

        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                Meter - value
            with pytest.raises(TypeError) as error_2:
                meter_per_second_unit - value
            assert str(error_1.value) == f"Units with translated scale are not allowed yet."
            assert str(error_2.value) == f"Units with translated scale are not allowed yet."


@pytest.mark.unit
class TestUnit:

    @staticmethod
    def test_instantiation_success(meter_per_second_unit, meter_scale, meter_per_second_scale):
        # check unidimensional instance
        meter = Meter(50.1)
        assert meter.scale == meter_scale
        assert meter.value == 50.1
        # check multidimensional instance
        speed = meter_per_second_unit(32.5)
        assert speed.scale == meter_per_second_scale
        assert speed.value == 32.5

    @staticmethod
    def test_instantiation_invalid_value(meter_scale):
        class A(Unit):
            scale = meter_scale

        class B:
            pass

        invalid_values = [[], {}, (1, 2, 3, 4, 5, 6, 7), B, B()]
        for value in invalid_values:
            # check for each value
            with pytest.raises(TypeError) as error:
                A(value)
                print()
            assert str(error.value) == f"Property 'value' must be of the type <class 'float'> or <class 'int'>"

    @staticmethod
    def test_equality():
        pass

    @staticmethod
    def test_multiplication():
        pass

    @staticmethod
    def test_multiplication_invalid():
        pass

    @staticmethod
    def test_division():
        pass

    @staticmethod
    def test_division_invalid():
        pass

    @staticmethod
    def test_power():
        pass

    @staticmethod
    def test_power_invalid():
        pass

    @staticmethod
    def test_addition():
        pass

    @staticmethod
    def test_addition_invalid():
        pass

    @staticmethod
    def test_subtraction():
        pass

    @staticmethod
    def test_subtraction_invalid():
        pass

    @staticmethod
    def test_conversion():
        pass

    @staticmethod
    def test_conversion_invalid():
        pass

    @staticmethod
    def test_to_si():
        pass

    @staticmethod
    def test_to_si_invalid():
        pass