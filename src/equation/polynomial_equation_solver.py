######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс решателя полиномиальных уравнений
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

from ..set import FuzzySet
from .simple_equation_solver import SimpleEquationSolver


class PolynomialEquationSolver(ABC):
    def __init__(
        self,
        simple_solver: SimpleEquationSolver
    ):
        self._simple_solver = simple_solver

    @abstractmethod
    def is_solution_empty(self, a: FuzzySet, b: float) -> bool:
        pass
    
    @abstractmethod
    def base_solution(self, a: FuzzySet, b: float) -> FuzzySet:
        pass

    @abstractmethod
    def branch_solutions(self, a: FuzzySet, b: float) -> list[FuzzySet]:
        pass

    @abstractmethod
    def make_intervals(self, base: FuzzySet, branch: FuzzySet) -> list[I.Interval]:
        pass
    

class ProductPolynomialEquationSolver(PolynomialEquationSolver):
    def is_solution_empty(self, a: FuzzySet, b: float) -> bool:
        return a.membership.max() <= b
    
    def base_solution(self, a: FuzzySet, b: float) -> FuzzySet:
        return FuzzySet({x: self._simple_solver.max(m, b) for x, m in a})
    
    def branch_solutions(self, a: FuzzySet, b: float) -> list[FuzzySet]:
        branches = []
        for x, m in a:
            if m < b:
                continue
            branch = FuzzySet(domain=a.domain)
            branch[x] = self._simple_solver.min(m, b)
            branches.append(branch)
        return branches
    
    def make_intervals(self, base: FuzzySet, branch: FuzzySet) -> list[I.Interval]:
        pairs = zip(branch.membership, base.membership)
        intervals = [*map(lambda x: I.closed(float(x[0]), float(x[1])), pairs)]
        return intervals
        