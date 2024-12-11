######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс решателя простых уравнений
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from abc import ABC, abstractmethod

import intervals as I


class SimpleEquationSolver(ABC):
    @abstractmethod
    def min(self, a: float, b: float) -> float:
        pass
    
    @abstractmethod
    def max(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def is_solution_empty(self, a: float, b: float) -> bool:
        pass

    @abstractmethod
    def _solve(self, a: float, b: float) -> I.Interval:
        pass
    

class ProductSimpleEquationSolver(SimpleEquationSolver):
    def min(self, a, b):
        return 1.0 if a < b else b / a if 0 < b <= a else 0.0
    
    def max(self, a, b):
        return 1 if a <= b else b / a 

    def is_solution_empty(self, a, b):
        return a < b
    
    def _solve(self, a, b):
        return I.closed(self.min(a, b), self.max(a, b))
    

if __name__ == '__main__':
    solver = ProductSimpleEquationSolver()
    print(solver.solve(0.4, 0.2))
