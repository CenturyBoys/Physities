from physities.src.dimension import Dimension, BaseDimension
from physities.src.scale import Scale
from .unit import Unit


class Meter(Unit):
    scale = Scale(
        dimension=Dimension.new_length(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


class Second(Unit):
    scale = Scale(
        dimension=Dimension.new_time(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


class Gram(Unit):
    scale = Scale(
        dimension=Dimension.new_mass(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


class Kelvin(Unit):
    scale = Scale(
        dimension=Dimension.new_temperature(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


class Unity(Unit):
    scale = Scale(
        dimension=Dimension.new_amount(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


class Ampere(Unit):
    scale = Scale(
        dimension=Dimension.new_electric_current(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


class Candela(Unit):
    scale = Scale(
        dimension=Dimension.new_luminous_intensity(),
        from_base_conversions=(1., 1., 1., 1., 1., 1., 1.),
        rescale_value=1
    )
    value = None


Centimeter = 0.01 * Meter

