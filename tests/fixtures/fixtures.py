import pytest

from physities.src.dimension import Dimension
from physities.src.dimension.base_dimensions import BaseDimension
from physities.src.scale import Scale
from physities.src.unit import Unit


@pytest.fixture()
def dimension_sample():
    return Dimension.new_instance(dimensions_tuple=(-1, -8.8, 0, 4.3333, 1.0, 9.7, 9))


@pytest.fixture()
def from_base_scale_conversion_sample():
    return -1, 0, 1, 2.0, 3, 4, 5


@pytest.fixture()
def energy_dimension():
    return Dimension.new_instance((2, 1, 0, -2, 0, 0, 0))


@pytest.fixture()
def force_dimension():
    return Dimension.new_instance((1, 1, 0, -2, 0, 0, 0))

@pytest.fixture()
def mass_dimension():
    return Dimension.new_instance((0, 1, 0, 0, 0, 0, 0))

@pytest.fixture()
def velocity_dimension():
    return Dimension.new_instance((1, 0, 0, -1, 0, 0, 0))


@pytest.fixture()
def inverse_velocity_dimension():
    return Dimension.new_instance((-1, 0, 0, 1, 0, 0, 0))


@pytest.fixture()
def velocity_square_dimension():
    return Dimension.new_instance((2, 0, 0, -2, 0, 0, 0))


@pytest.fixture()
def dimensionless_dimension():
    return Dimension.new_instance((0, 0, 0, 0, 0, 0, 0))

@pytest.fixture()
def dimensionless_scale(dimensionless_dimension):
    return Scale(
        dimension=dimensionless_dimension,
        from_base_scale_conversions=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), rescale_value=1
    )

@pytest.fixture()
def inverse_velocity_scale(inverse_velocity_dimension):
    return Scale.new(dimension=inverse_velocity_dimension)

@pytest.fixture()
def newton_scale(force_dimension):
    return Scale.new(
        dimension=force_dimension,
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
        rescale_value=1,
    )


@pytest.fixture()
def kilogram_scale(mass_dimension):
    return Scale.new(
        dimension=mass_dimension,
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
        rescale_value=1,
    )


@pytest.fixture()
def second_scale():
    return Scale.new(
        dimension=Dimension.new_time(1),
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def second_inverse_scale():
    return Scale.new(
        dimension=Dimension.new_time(-1),
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def kilometer_per_second_scale(velocity_dimension):
    return Scale(
        dimension=velocity_dimension,
        from_base_scale_conversions=(1000, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
        rescale_value=1,
    )

@pytest.fixture()
def meter_scale():
    return Scale.new(
        dimension=Dimension.new_length(1),
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def kilometer_scale():
    return Scale.new(
        dimension=Dimension.new_length(1),
        from_base_scale_conversions=(1000, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def joule_scale(energy_dimension):
    return Scale.new(
        dimension=energy_dimension,
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
        rescale_value=1,
    )


@pytest.fixture()
def cal_scale(energy_dimension):
    return Scale.new(
        dimension=energy_dimension,
        from_base_scale_conversions=(1, 1, 1, 1, 1, 1, 1),
        rescale_value=4.184,
    )


@pytest.fixture()
def kilometer_square_scale():
    return Scale.new(
        dimension=Dimension.new_length(2),
        from_base_scale_conversions=(1000000, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def meter_per_second_scale(velocity_dimension):
    return Scale(
            dimension=velocity_dimension,
            from_base_scale_conversions=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            rescale_value=1,
        )


@pytest.fixture()
def kilometer_per_second_square_scale(velocity_square_dimension):
    return Scale.new(
        dimension=velocity_square_dimension,
        from_base_scale_conversions=(1000000, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def kilometer_per_second_square_unit(kilometer_per_second_square_scale):
    class KilometerPetSecondSquare(Unit):
        scale = kilometer_per_second_square_scale
        value = None

    return KilometerPetSecondSquare


@pytest.fixture()
def inverse_second_unit(second_inverse_scale,):
    class InverseSecond(Unit):
        scale = second_inverse_scale
        value = None

    return InverseSecond


@pytest.fixture()
def kilogram_unit(kilogram_scale,):
    class Kilogram(Unit):
        scale = kilogram_scale
        value = None

    return Kilogram


@pytest.fixture()
def meter_per_second_unit(meter_per_second_scale):
    class MeterPerSecond(Unit):
        scale = meter_per_second_scale
        value = None
    return MeterPerSecond


@pytest.fixture()
def kilometer_unit(kilometer_scale):
    class Kilometer(Unit):
        scale = kilometer_scale
        value = None
    return Kilometer


@pytest.fixture()
def inverse_meter_per_second_unit(inverse_velocity_scale):
    class InverseMeterPerSecond(Unit):
        scale = inverse_velocity_scale
        value = None
    return InverseMeterPerSecond


@pytest.fixture()
def kilometer_per_second_unit(kilometer_per_second_scale):
    class KilometerPerSecond(Unit):
        scale = kilometer_per_second_scale
        value = None
    return KilometerPerSecond


@pytest.fixture()
def kilometer_square_unit(kilometer_square_scale):
    class KilometerSquare(Unit):
        scale = kilometer_square_scale
        value = None
    return KilometerSquare


@pytest.fixture()
def joule_unit(joule_scale):
    class Joule(Unit):
        scale = joule_scale
        value = None
    return Joule


@pytest.fixture()
def calories_unit(cal_scale):
    class Calorie(Unit):
        scale = cal_scale
        value = None
    return Calorie