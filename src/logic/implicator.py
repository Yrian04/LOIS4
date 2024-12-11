######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# абстрактный класс импликатора
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#

from abc import ABC, abstractmethod


class Implicator(ABC):
    @abstractmethod
    def __call__(self, first: float, second: float) -> float:
        pass
    

class GodelImplicator(Implicator):
    def __call__(self, first: float, second: float) -> float:
        return 1. if first <= second else second
    