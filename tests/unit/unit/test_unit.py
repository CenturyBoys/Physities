from physities.src.unit import Meter, Second, Minute, Kilometer, Candela
from physities.src.unit.unit import MetaUnit
from tests.fixtures import *


@pytest.mark.unit
class TestMetaUnit:

    @staticmethod
    def test_hashable(joule_unit):
        hash(Meter)
        hash(joule_unit)

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
    def test_power(dimensionless_scale, meter_per_second_unit, inverse_meter_per_second_unit, kilometer_square_unit, kilometer_per_second_unit, kilometer_per_second_square_unit):
        square_kilometer = Kilometer ** 2
        kilometer_per_second_square_unit_2 = kilometer_per_second_unit ** 2
        inverse_meter_per_second_unit_2 = meter_per_second_unit ** -1
        # check inverse power
        assert inverse_meter_per_second_unit_2 == inverse_meter_per_second_unit
        # check unidimensional power
        assert square_kilometer == kilometer_square_unit
        # check multidimensional power
        assert kilometer_per_second_square_unit_2 == kilometer_per_second_square_unit
        # check zero power
        assert (Kilometer ** 0).scale == dimensionless_scale

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
    def test_instantiation(meter_per_second_unit, meter_scale, meter_per_second_scale):
        # check unidimensional instance
        meter = Meter(50.1)
        assert meter.scale == meter_scale
        assert meter.value == 50.1
        # check multidimensional instance
        speed = meter_per_second_unit(32.5)
        assert speed.scale == meter_per_second_scale
        assert speed.value == 32.5

    @staticmethod
    def test_equality(calories_unit, joule_unit):
        energy_1 = joule_unit(50)
        energy_2 = calories_unit(11.950286806883364)
        distance_1 = Meter(1000)
        distance_2 = Kilometer(1)
        # check unidimensional equality
        assert distance_1 == distance_2
        # check multidimensional equality
        assert energy_1 == energy_2

    @staticmethod
    def test_multiplication(
            inverse_meter_per_second_unit,
            kilogram_unit,
            inverse_second_unit,
            newton_scale,
            second_scale,
            dimensionless_scale
    ):
        meter_second_inverse = inverse_meter_per_second_unit(10)
        meter = Meter(10)
        second = meter_second_inverse * meter
        inverse_second = inverse_second_unit(10)
        scalar = second * inverse_second
        inverse_second_square = inverse_second * inverse_second
        kilogram = kilogram_unit(10)
        force = meter * inverse_second_square * kilogram

        # annulation
        assert second.value == 100
        assert second.scale == second_scale
        # scalar annulation
        assert scalar.value == 1000
        assert scalar.scale == dimensionless_scale
        # multidimensional composition
        assert force.value == 10000
        assert force.scale == newton_scale

    @staticmethod
    def test_multiplication_invalid(meter_per_second_unit):
        class A:
            pass
        meter = Meter(60)
        meter_per_second = meter_per_second_unit(10)
        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                meter * value
            with pytest.raises(TypeError) as error_2:
                meter_per_second * value
            assert str(error_1.value) == f"{type(meter)} can be multiplied only by {type(meter)}, {float} and {int}"
            assert str(error_2.value) == f"{type(meter_per_second)} can be multiplied only by {type(meter_per_second)}, {float} and {int}"

    @staticmethod
    def test_division(kilogram_unit, newton_scale, dimensionless_scale, meter_per_second_unit, second_inverse_scale):
        square_second = (Second**2)(10)
        kilogram_meter = (kilogram_unit * Meter)(100)
        meter = Meter(10)
        inverse_second = meter_per_second_unit(15) / meter

        newton = kilogram_meter / square_second
        scalar = Meter(144) / Meter(12)

        # multidimensional composition
        assert newton.value == 10
        assert newton.scale == newton_scale
        # scalar annulation
        assert scalar.value == 12
        assert scalar.scale == dimensionless_scale
        # annulation
        assert inverse_second.scale == second_inverse_scale
        assert inverse_second.value == 1.5

    @staticmethod
    def test_division_invalid(meter_per_second_unit):
        class A:
            pass

        meter = Meter(60)
        meter_per_second = meter_per_second_unit(10)
        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                meter / value
            with pytest.raises(TypeError) as error_2:
                meter_per_second / value
            with pytest.raises(TypeError) as error_3:
                value / meter
            with pytest.raises(TypeError) as error_4:
                value / meter_per_second
            assert str(error_1.value) == f"{type(meter)} only allows division by {type(meter)}, {int} and {float}"
            assert str(error_2.value) == f"{type(meter_per_second)} only allows division by {type(meter_per_second)}, {int} and {float}"
            if value in (Meter, meter_per_second_unit):
                assert str(error_1.value) == f"{type(meter)} only allows division by {type(meter)}, {int} and {float}"
                assert str(error_2.value) == f"{type(meter_per_second)} only allows division by {type(meter_per_second)}, {int} and {float}"
            else:
                assert str(error_3.value) == f"{type(meter)} can divide only {type(meter)}, {int} and {float}"
                assert str(error_4.value) == f"{type(meter_per_second)} can divide only {type(meter_per_second)}, {int} and {float}"

    @staticmethod
    def test_power(kilometer_per_second_unit, kilometer_square_unit, kilometer_per_second_square_unit, dimensionless_scale):
        kilometer_square = Kilometer(12) ** 2
        kilometer_per_second_square = kilometer_per_second_unit(5) ** 2
        kilometer = kilometer_square_unit(100) ** 0.5
        unit_scalar = (kilometer_per_second_square ** 0)

        # unidimensional power
        assert kilometer_square == kilometer_square_unit(144)
        # multidimensional power
        assert kilometer_per_second_square == kilometer_per_second_square_unit(25)
        # fractional power
        assert kilometer == Kilometer(10)
        # zero power
        assert unit_scalar.scale == dimensionless_scale
        assert unit_scalar.value == 1

    @staticmethod
    def test_power_invalid(meter_per_second_unit):
        class A:
            pass

        meter = Meter(60)
        meter_per_second = meter_per_second_unit(10)
        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                meter ** value
            with pytest.raises(TypeError) as error_2:
                meter_per_second ** value
            assert str(error_1.value) == f"{type(meter)} can only be powered by {int} and {float}"
            assert str(error_2.value) == f"{type(meter_per_second)} can only be powered by {int} and {float}"

    @staticmethod
    def test_addition(meter_per_second_unit):
        # check unidimensional addition
        assert Candela(10) + Candela(34) == Candela(44)
        # check multidimensional addition
        assert meter_per_second_unit(52) + meter_per_second_unit(89) == meter_per_second_unit(141)
        # check distributive property
        assert (Meter(10) + Meter(15))/Second(2) == Meter(10)/Second(2) + Meter(15)/Second(2)

    @staticmethod
    def test_addition_invalid(meter_per_second_unit):
        class A:
            pass

        meter = Meter(60)
        meter_per_second = meter_per_second_unit(10)
        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                meter + value
            with pytest.raises(TypeError) as error_2:
                meter_per_second + value
            assert str(error_1.value) == f"{type(value)} is not from type {type(meter)}"
            assert str(error_2.value) == f"{type(value)} is not from type {type(meter_per_second)}"
        with pytest.raises(TypeError) as error:
            meter_per_second + Second(10)
        assert str(error.value) == f"Dimensions do not match {meter_per_second_unit.scale.dimension} != {Second.scale.dimension}"

    @staticmethod
    def test_subtraction(meter_per_second_unit):
        # check unidimensional addition
        assert Candela(10) - Candela(34) == Candela(-24)
        # check multidimensional addition
        assert meter_per_second_unit(52) - meter_per_second_unit(89) == meter_per_second_unit(-37)
        # check distributive property
        assert (Meter(10) - Meter(15)) / Second(2) == Meter(10) / Second(2) - Meter(15) / Second(2)

    @staticmethod
    def test_subtraction_invalid(meter_per_second_unit):
        class A:
            pass

        meter = Meter(60)
        meter_per_second = meter_per_second_unit(10)
        invalid_values = [[], {}, A, (1, 2), Meter, meter_per_second_unit]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                meter - value
            with pytest.raises(TypeError) as error_2:
                meter_per_second - value
            assert str(error_1.value) == f"{type(value)} is not from type {type(meter)}"
            assert str(error_2.value) == f"{type(value)} is not from type {type(meter_per_second)}"
        with pytest.raises(TypeError) as error:
            meter_per_second + Second(10)
        assert str(
            error.value) == f"Dimensions do not match {meter_per_second_unit.scale.dimension} != {Second.scale.dimension}"

    @staticmethod
    def test_conversion(joule_unit, calories_unit):
        joule = joule_unit(50)
        calories = calories_unit(11.950286806883364)
        meter = Meter(1000)
        kilometer = Kilometer(1)
        # check unidimensional equality
        assert meter.convert(Kilometer) == kilometer
        assert kilometer.convert(Meter) == meter
        # check multidimensional equality
        assert round(joule.convert(calories_unit).value, 13) == round(calories.value, 13)
        assert round(calories.convert(joule_unit).value, 13) == round(joule.value, 13)

    @staticmethod
    def test_conversion_invalid(meter_per_second_unit):
        class A:
            pass

        meter = Meter(60)
        meter_per_second = meter_per_second_unit(10)
        invalid_values = [[], {}, A, (1, 2)]
        for value in invalid_values:
            with pytest.raises(TypeError) as error_1:
                meter.convert(value)
            with pytest.raises(TypeError) as error_2:
                meter_per_second.convert(value)
            assert str(error_1.value) == f"Invalid param type {type(value)} != {type(MetaUnit)}"
            assert str(error_2.value) == f"Invalid param type {type(value)} != {type(MetaUnit)}"
        with pytest.raises(TypeError) as error:
            meter_per_second.convert(Second)
        assert str(error.value) == "Dimensions do not match"

    @staticmethod
    def test_to_si(calories_unit, kilometer_unit, joule_unit):
        joule = joule_unit(50)
        calories = calories_unit(11.950286806883364)
        kilometer = kilometer_unit(10)
        meter = Meter(10000)
        assert kilometer.to_si().value == meter.value
        assert kilometer.to_si().scale.rescale_value == meter.scale.rescale_value
        index = 0
        while index < 7:
            assert kilometer.to_si().scale.from_base_scale_conversions[index] == meter.scale.from_base_scale_conversions[index]
            assert calories.to_si().scale.from_base_scale_conversions[index] == joule.scale.from_base_scale_conversions[index]
            index += 1
        assert round(calories.to_si().value, 13) == round(joule.value, 13)
        assert calories.to_si().scale.rescale_value == joule.scale.rescale_value

