import pytest

from physities.src.dimension import Dimension
from physities.src.dimension.base_dimensions import BaseDimension
from physities.src.scale import Scale


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
def velocity_dimension():
    return Dimension.new_instance((1, 0, 0, -1, 0, 0, 0))


@pytest.fixture()
def velocity_square_dimension():
    return Dimension.new_instance((2, 0, 0, -2, 0, 0, 0))


@pytest.fixture()
def newton_scale(force_dimension):
    return Scale.new(
        dimension=force_dimension,
        from_base_scale_conversions=(1, 1000, 1, 1, 1, 1, 1),
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
        from_base_scale_conversions=(1, 1000, 1, 1, 1, 1, 1),
        rescale_value=1,
    )


@pytest.fixture()
def cal_scale(energy_dimension):
    return Scale.new(
        dimension=energy_dimension,
        from_base_scale_conversions=(1, 1000, 1, 1, 1, 1, 1),
        rescale_value=0.2390,
    )


@pytest.fixture()
def kilometer_square_scale():
    return Scale.new(
        dimension=Dimension.new_length(2),
        from_base_scale_conversions=(1000000, 1, 1, 1, 1, 1, 1),
    )


@pytest.fixture()
def kilometer_per_second_square(velocity_square_dimension):
    return Scale.new(
        dimension=velocity_square_dimension,
        from_base_scale_conversions=(1000000, 1, 1, 1, 1, 1, 1),
    )
