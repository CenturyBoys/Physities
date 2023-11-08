from physities.src.dimension import Dimension, BaseDimension
from physities.src.scale import Scale
from .unit import Unit


class Metre(Unit):
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


# Length

Gigametre = 1000000000 * Metre
Megametre = 1000000 * Metre
Kilometre = 1000 * Metre
Hectometre = 100 * Metre
Decametre = 10 * Metre
Decimetre = 0.1 * Metre
Centimetre = 0.01 * Metre
Millimetre = 0.001 * Metre
Micrometre = 0.000001 * Metre
Nanometre = 0.000000001 * Metre
Foot = 0.3048 * Metre
Yard = 0.9144 * Metre
Inch = 0.0254 * Metre
Mile = 1609.34 * Metre
Furlong = 201.168 * Metre
Rod = 5.0292 * Metre

# Time

Nanosecond = 0.000000001 * Second
Microsecond = 0.000001 * Second
Millisecond = 0.001 * Second
Centisecond = 0.01 * Second
Decisecond = 0.1 * Second
Minute = 60 * Second
Hour = 3600 * Second
Day = 86400 * Second
Week = 604800 * Second
Month = 2628288 * Second
Year = 31557600 * Second
Decade = 315576000 * Second
Century = 3155760000 * Second
Millennium = 31_557_600_000 * Second

#Unit

Dozen = 12 * Unity
Moles = 6.02214076 * 10**23 * Unity
Pairs = 2 * Unity
Score = 20 * Unity

#Mass

Gigagram = 1000000000 * Gram
Megagram = 1000000 * Gram
Kilogram = 1000 * Gram
Hectogram = 100 * Gram
Decagram = 10 * Gram
Decigram = 0.1 * Gram
Centigram = 0.01 * Gram
Milligram = 0.001 * Gram
Microgram = 0.000001 * Gram
Nanogram = 0.000000001 * Gram
Pound = 0.453592 * Gram
Ounce = 0.0283495 * Gram
Tonne = 1000 * Gram
Stone = 6.35029 * Gram
Carat = 0.0002 * Gram
Grain = 0.0000647989 * Gram
Slug = 14.5939 * Gram

#Eletric Current

Gigaampere = 1000000000 * Ampere
Megaampere = 1000000 * Ampere
Kiloampere = 1000 * Ampere
Milliampere = 0.001 * Ampere
Microampere = 0.000001 * Ampere
Nanoampere = 0.000000001 * Ampere

#Area

Gigametre2 = Gigametre * Gigametre
Megametre2 = Megametre * Megametre
Kilometre2 = Kilometre * Kilometre
Hectometre2 = Hectare = Hectometre * Hectometre
Decametre2 = Decametre * Decametre
Metre2 = Metre * Metre
Decimetre2 = Decimetre * Decimetre
Centimetre2 = Centimetre * Centimetre
Millimetre2 = Millimetre * Millimetre
Micrometre2 = Micrometre * Micrometre
Nanometre2 = Nanometre * Nanometre
Foot2 = Foot * Foot
Yard2 = Yard * Yard
Inch2 = Inch * Inch
Mile2 = Mile * Mile
Furlong2 = Furlong * Furlong
Rod2 = Rod * Rod
Acre = 4046.860107422 * Metre2

#Volume

Gigametre3 = Gigametre2 * Gigametre
Megametre3 = Megametre2 * Megametre
Kilometre3 = Kilometre2 * Kilometre
Hectometre3 = Hectometre2 * Hectometre
Decametre3 = Decametre2 * Decametre
Metre3 = Kiloliter = Metre2 * Metre
Decimetre3 = Liter = Decimetre2 * Decimetre
Centimetre3 = Milliliter = Centimetre2 * Centimetre
Millimetre3 = Millimetre2 * Millimetre
Micrometre3 = Micrometre2 * Micrometre
Nanometre3 = Nanometre2 * Nanometre
Foot3 = Foot2 * Foot
Yard3 = Yard2 * Yard
Inch3 = Inch2 * Inch
Mile3 = Mile2 * Mile
Furlong3 = Furlong2 * Furlong
Rod3 = Rod2 * Rod
Gallon = 3785.411784 * Milliliter
Pint = 473 * Milliliter
Barrel = 0.158987294928 * Metre3


