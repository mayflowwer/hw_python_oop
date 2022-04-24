from dataclasses import dataclass, asdict
from typing import Union

import constants


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Возвращает строку с инфомацией о тренировке."""
        return ('Тип тренировки: {}; '
                'Длительность: {:.3f} ч.; '
                'Дистанция: {:.3f} км; '
                'Ср. скорость: {:.3f} км/ч; '
                'Потрачено ккал: {:.3f}.').format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = constants.LEN_STEP
    M_IN_KM: int = constants.M_IN_KM

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.calories = None
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / constants.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = constants.LEN_STEP

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в беге."""
        return ((constants.RN_CALORIE_COEFF_1
                * self.get_mean_speed()
                - constants.RN_CALORIE_COEFF_2)
                * self.weight
                / constants.M_IN_KM
                * self.duration
                * constants.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = constants.LEN_STEP

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в ходьбе."""
        return ((constants.WLK_CALORIE_COEFF_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * constants.WLK_CALORIE_COEFF_2 * self.weight)
                * self.duration * constants.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = constants.LEN_PADDLE

    def __init__(self, action, duration, weight, length_pool, count_pool):
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / constants.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool\
            / constants.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + constants.SWM_CALORIE_COEFF_1)
                * constants.SWM_CALORIE_COEFF_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dct = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    for code, class_name in dct.items():
        if workout_type == code:
            training = dct[code](*data)

    return training


def main(training: Union[Training, Running, SportsWalking, Swimming]) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
