######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# абстрактный класс Т-нормы
#
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
import numpy as np

from abc import ABC, abstractmethod


class Tnorm(ABC):
    @abstractmethod
    def __call__(self, first: float, second: float) -> float:
        pass
    

class LogicalProduct(Tnorm):
    def __call__(self, first: float, second: float) -> float:
        return np.minimum(first, second)
