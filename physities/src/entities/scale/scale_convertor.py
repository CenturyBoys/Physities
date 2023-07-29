import time
from dataclasses import dataclass
from enum import IntEnum

from physities.src.entities.dimension import Dimension
from physities.src.enums.base_units import BaseDimensions


@dataclass(frozen=True, slots=True)
class ScaleConvertor:
    dimension: Dimension
    from_base_conversions: tuple[
        float | int, float | int, float | int, float | int, float | int
    ]
    rescale_value: float

    @staticmethod
    def __get_annulled_dimension(
        dimension_1: Dimension, dimension_2: Dimension, result_dimension: Dimension
    ) -> list[BaseDimensions, BaseDimensions, BaseDimensions, BaseDimensions, BaseDimensions, BaseDimensions]:
        set_1 = set(dimension_1.get_dimensions())
        set_2 = set(dimension_2.get_dimensions())
        set_3 = set(result_dimension.get_dimensions())
        return list((set_1 - set_3).union(set_2 - set_3))

    @staticmethod
    def __fit_scale_and_dimension(
        dimension_instance: Dimension,
        from_base_conversions: tuple[
            float | int, float | int, float | int, float | int, float | int
        ],
        value: float | int,
        rescale_value: float | int,
    ):
        dimension = dimension_instance.get_dimensions()
        if len(dimension) == 1:
            index = dimension.pop()
            from_base_conversions_list = list(from_base_conversions)
            from_base_conversions_list[index] *= value
            new_from_base_conversions = tuple(from_base_conversions_list)
            return 1, new_from_base_conversions
        return rescale_value * value, from_base_conversions

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=self.dimension,
                from_base_conversions=self.from_base_conversions,
                rescale_value=self.rescale_value,
                value=other,
            )
            return ScaleConvertor(
                dimension=self.dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        if isinstance(other, ScaleConvertor):
            new_dimension = self.dimension + other.dimension
            new_from_base_conversions_list = [
                self.from_base_conversions[i] * other.from_base_conversions[i]
                for i in BaseDimensions
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
            return ScaleConvertor(
                dimension=new_dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        return TypeError(
            f"{ScaleConvertor} can only be multiplied by {ScaleConvertor}, {int} or {float}. This operation is not implemented for {type(other)}."
        )

    def __rmul__(self, other):
        try:
            to_return = ScaleConvertor.__mul__(self, other)
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
            return ScaleConvertor(
                dimension=self.dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        if isinstance(other, ScaleConvertor):
            new_dimension = self.dimension - other.dimension
            annulled_dimensions = self.__get_annulled_dimension(
                dimension_1=self.dimension,
                dimension_2=other.dimension,
                result_dimension=new_dimension,
            )
            rescale_factor = 1
            new_from_base_conversions_list = [
                self.from_base_conversions[i] / other.from_base_conversions[i]
                for i in BaseDimensions
            ]
            for annulled_index in annulled_dimensions:
                rescale_factor *= new_from_base_conversions_list[annulled_index]
                new_from_base_conversions_list[annulled_index] = 1
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=new_dimension,
                from_base_conversions=tuple(new_from_base_conversions_list),
                rescale_value=self.rescale_value,
                value=rescale_factor,
            )
            return ScaleConvertor(
                dimension=new_dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        return TypeError(
            f"{ScaleConvertor} can only be divided by {ScaleConvertor}, {int} or {float}. This operation is not implemented for {type(other)}."
        )

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_dimension = self.dimension * -1
            new_rescale_value = 1 / self.rescale_value
            new_value, new_from_base_conversions = self.__fit_scale_and_dimension(
                dimension_instance=new_dimension,
                from_base_conversions=self.from_base_conversions,
                rescale_value=new_rescale_value,
                value=other,
            )
            return ScaleConvertor(
                dimension=self.dimension,
                from_base_conversions=new_from_base_conversions,
                rescale_value=new_value,
            )
        return TypeError(
            f"{ScaleConvertor} can only divide {ScaleConvertor}, {int} or {float}. This operation is not implemented for {type(other)}."
        )

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            new_dimension = self.dimension * power
            new_from_base_conversions = tuple(i**power for i in self.from_base_conversions)
            new_rescale_value = self.rescale_value**power
            return ScaleConvertor(
                dimension=new_dimension, from_base_conversions=new_from_base_conversions, rescale_value=new_rescale_value
            )
        return TypeError(
            f"{ScaleConvertor} can only be powered by {int} or {float}. This operation is not implemented for {type(other)}."
        )

