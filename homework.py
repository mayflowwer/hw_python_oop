from typing import Union

import constants


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training) -> None:
        self.training_type = training.training_type
        self.duration = training.duration
        self.distance = training.distance
        self.mean_speed = training.mean_speed
        self.calories = training.calories

    def get_message(self):
        """Возвращает строку с инфомацией о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {round(self.duration, 3)} ч.; '
                f'Дистанция: {round(self.distance, 3)} км; '
                f'Ср. скорость: {round(self.mean_speed, 3)} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.training_type = 'default'
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * constants.LEN_STEP / constants.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, training) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training)


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)
        self.training_type = 'Running'
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в беге."""
        return (constants.RUN_COEFF_CALORIE_1 * self.mean_speed
                - constants.RUN_COEFF_CALORIE_2) * self.weight / constants.M_IN_KM * (
                    self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        self.height = height
        super().__init__(action, duration, weight)
        self.training_type = 'Sports_walking'
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в ходьбе."""
        return (constants.WALK_COEFF_CALORIE_1 * self.weight
                + (self.mean_speed ** 2 // self.height)
                * 0.029 * self.weight) * (self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self, action, duration, weight, length_pool, count_pool):
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)
        self.training_type = 'Swimming'
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * constants.LEN_PADDLE / constants.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / (
                M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.mean_speed + constants.SWIM_COEFF_CALORIE_1) * (
                constants.SWIM_COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = None
    if workout_type == 'SWM':
        training = Swimming(*data)
    if workout_type == 'RUN':
        training = Running(*data)
    elif workout_type == 'WLK':
        training = SportsWalking(*data)

    return training


def main(training: Union[Training, Running, SportsWalking, Swimming]) -> None:
    """Главная функция."""
    print(training.show_training_info(training).get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
