######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс решателя системы уравнений
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from functools import reduce
from itertools import product

import intervals

from ..map import FuzzyMap
from ..set import FuzzySetAlgebra, FuzzySet
from ..map import FuzzyMapAlgebra

from .polynomial_equation_solver import PolynomialEquationSolver


class SystemEquationSolver:
    def __init__(
        self,
        polynomial_solver: PolynomialEquationSolver,
        set_algebra: FuzzySetAlgebra,
        map_algebra: FuzzyMapAlgebra | None = None
    ):
        self.polynomial_solver = polynomial_solver
        self.set_algebra = set_algebra
        
        if map_algebra is None:
            map_algebra = FuzzyMapAlgebra(set_algebra)
        
        self.map_algebra = map_algebra

    def solve(self, a: FuzzyMap, b: FuzzySet) -> list[list[intervals.Interval]]:
        bases = [self.polynomial_solver.base_solution(a.ycut(x), b[x]) for x in b.domain]
        base = reduce(lambda x, y: self.set_algebra.intersection(x, y), bases)

        if self.map_algebra.composition(base, a) != b:
            return []

        polynomial_branches = [self.polynomial_solver.branch_solutions(a.ycut(x), b[x]) for x in b.domain]
        branches = []
        for branch in (reduce(lambda x, y: self.set_algebra.union(x, y), z) for z in product(*polynomial_branches)):
            for other in branches:
                if other < branch or other == branch:
                    break
            else:
                branches.append(branch)
        
        answer = []
        for branch_solution in branches:
            branch_answer = self.polynomial_solver.make_intervals(base, branch_solution)
            answer.append(branch_answer)

        return answer
