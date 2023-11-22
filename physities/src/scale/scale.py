from math import prod
from dataclasses import dataclass

from kobject import Kobject

from physities.src.dimension import Dimension
from physities.src.dimension.base_dimensions import BaseDimension


@dataclass(frozen=True, slots=True)
class Scale(Kobject):
    """
        dimension:

        from_base_conversions:

        rescale_value:
    """
    dimension: Dimension
    from_base_conversions: tuple[
        float | int, float | int, float | int, float | int, float | int, float | int, float | int
    ]
    rescale_value: float | int

    # def __post_init__(self):
    #     if not isinstance(self.dimension, Dimension):
    #         raise TypeError(f"dimension is not of the type {type(Dimension)}.")
    #     if not isinstance(self.from_base_conversions, tuple):
    #         raise TypeError(f"from_base_conversions is not of the type {type(tuple)}.")
    #     if len(self.from_base_conversions) != len(BaseDimension):
    #         raise ValueError(
    #             f"Invalid length of tuple. Expected {len(BaseDimension)}, but got {len(self.from_base_conversions)}."
    #         )
    #     if not isinstance(self.rescale_value, float):
    #         raise TypeError(f"rescale_value is not of the type {type(float)} ou {type(int)}.")

    @classmethod
    def new(
            cls,
            dimension: Dimension = Dimension.new_dimensionless(),
            from_base_conversions: tuple[
                float, float, float, float, float, float, float
            ] = (1., 1., 1., 1., 1., 1., 1.),
            rescale_value: float = 1
    ):
        return cls(dimension=dimension, from_base_conversions=from_base_conversions, rescale_value=rescale_value)

    @property
    def is_dimensionless(self) -> bool:
        if not self.dimension.get_dimensions():
            return True
        return False

    @property
    def conversion_factor(self) -> float:
        return self.rescale_value * prod(self.from_base_conversions)

    @staticmethod
    def __get_annulled_dimension(
        dimension_1: Dimension, dimension_2: Dimension, result_dimension: Dimension
    ) -> list[BaseDimension, BaseDimension, BaseDimension, BaseDimension, BaseDimension, BaseDimension]:
        set_1 = set(dimension_1.get_dimensions())
        set_2 = set(dimension_2.get_dimensions())
        set_3 = set(result_dimension.get_dimensions())
        return list((set_1 - set_3).union(set_2 - set_3))

    @staticmethod
    def __fit_scale_and_dimension(
        dimension_instance: Dimension,
        from_base_conversions: tuple[
            float, float, float, float, float, float, float
        ],
        value: float,
        rescale_value: float,
    ):
        dimension = dimension_instance.get_dimensions()
        if len(dimension) == 1:
            index = dimension.pop()
            from_base_conversions_list = list(from_base_conversions)
            from_base_conversions_list[index] *= value
            new_from_base_conversions = tuple(from_base_conversions_list)
            return 1, new_from_base_conversions
        return rescale_value * value, from_base_conversions

    def __eq__(self, other):
        if isinstance(other, Scale):
            if self.dimension == other.dimension and self.from_base_conversions == other.from_base_conversions:
                return True
        return False


    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=self.dimension,
                from_base_conversions=self.from_base_conversions,
                rescale_value=self.rescale_value,
                value=other,
            )
            return Scale(
                dimension=self.dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        if isinstance(other, Scale):
            new_dimension = self.dimension + other.dimension
            new_from_base_conversions_list = [
                self.from_base_conversions[i] * other.from_base_conversions[i]
                for i in BaseDimension
            ]
            annulled_dimensions = self.__get_annulled_dimension(
                dimension_1=self.dimension,
                dimension_2=other.dimension,
                result_dimension=new_dimension,
            )
            rescale_factor = 1
            for annulled_index in annulled_dimensions:
                rescale_factor *= new_from_base_conversions_list[annulled_index]
                new_from_base_conversions_list[annulled_index] = 1
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=new_dimension,
                from_base_conversions=tuple(new_from_base_conversions_list),
                rescale_value=self.rescale_value,
                value=rescale_factor,
            )
            return Scale(
                dimension=new_dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        return TypeError(
            f"{Scale} can only be multiplied by {Scale}, {int} or {float}. This operation is not implemented for {type(other)}."
        )

    def __rmul__(self, other):
        try:
            to_return = Scale.__mul__(self, other)
        except TypeError as e:
            raise e
        return to_return

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=self.dimension,
                from_base_conversions=self.from_base_conversions,
                rescale_value=self.rescale_value,
                value=1 / other,
            )
            return Scale(
                dimension=self.dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        if isinstance(other, Scale):
            new_dimension = self.dimension - other.dimension
            annulled_dimensions = self.__get_annulled_dimension(
                dimension_1=self.dimension,
                dimension_2=other.dimension,
                result_dimension=new_dimension,
            )
            rescale_factor = 1
            new_from_base_conversions_list = [
                self.from_base_conversions[i] / other.from_base_conversions[i]
                for i in BaseDimension
            ]
            for annulled_index in annulled_dimensions:
                rescale_factor *= new_from_base_conversions_list[annulled_index]
                new_from_base_conversions_list[annulled_index] = 1.
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=new_dimension,
                from_base_conversions=tuple(new_from_base_conversions_list),
                rescale_value=self.rescale_value,
                value=rescale_factor,
            )
            return Scale(
                dimension=new_dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        return TypeError(
            f"{Scale} can only be divided by {Scale}, {int} or {float}. This operation is not implemented for {type(other)}."
        )

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_dimension = self.dimension * -1
            new_rescale_value = 1 / self.rescale_value
            new_from_base_conversions_list = [
                1 / self.from_base_conversions[i]
                for i in BaseDimension
            ]
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=new_dimension,
                from_base_conversions=tuple(new_from_base_conversions_list),
                rescale_value=new_rescale_value,
                value=other,
            )
            return Scale(
                dimension=new_dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        return TypeError(
            f"{Scale} can only divide {Scale}, {int} or {float}. This operation is not implemented for {type(other)}."
        )

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            new_dimension = self.dimension * power
            new_from_base_conversions = tuple(i**power for i in self.from_base_conversions)
            new_rescale_value = self.rescale_value**power
            return Scale(
                dimension=new_dimension, from_base_conversions=new_from_base_conversions, rescale_value=new_rescale_value
            )
        return TypeError(
            f"{Scale} can only be powered by {int} or {float}. This operation is not implemented for {type(other)}."
        )

