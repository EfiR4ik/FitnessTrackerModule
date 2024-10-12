class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} "
                f"км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    training_type = ' '
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.training_type,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    training_type = 'Running'

    def get_spent_calories(self) -> float:
        """Переопределенный метод получения количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) *
                self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIES_WEIGHT_MULTIPLIER_1 = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2 = 0.029
    KMH_IN_MS = 0.278
    SM_IN_M = 100
    training_type = 'SportsWalking'

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Переопределенный метод получения количество затраченных калорий."""
        return (self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight +
                ((self.get_mean_speed() * self.KMH_IN_MS) ** 2 / self.height * self.SM_IN_M) *
                self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight) * self.duration * self.MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    MEAN_SPEAD_ADD = 1.1
    GET_CALORIES_MULT = 2
    training_type = 'Swimming'

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.MEAN_SPEAD_ADD) * self.GET_CALORIES_MULT * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    workout_class = workout_classes.get(workout_type)
    return workout_class(*data)


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
