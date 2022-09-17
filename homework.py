from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    TIME_IN_HOUR: ClassVar[int] = 60
    LEN_STEP: ClassVar[float] = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[float] = 18
    COEFF_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2
            )
            * self.weight / self.M_IN_KM * self.duration
            * self.TIME_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFF_CALORIE_1: ClassVar[float] = 0.035
    COEFF_CALORIE_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """"Получить количество затрачиваемых калорий"""
        return (
            (
                self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_2
                * self.weight
            )
            * self.duration * self.TIME_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    COEFF_CALORIE_1: ClassVar[float] = 1.1
    COEFF_CALORIE_2: ClassVar[float] = 2
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Расчет калорий Swimming"""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    WORKOUT_TYPE: dict[str, list[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in WORKOUT_TYPE:
        return WORKOUT_TYPE[workout_type](*data)
    raise ValueError('Такой вид тренировки не найден')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
