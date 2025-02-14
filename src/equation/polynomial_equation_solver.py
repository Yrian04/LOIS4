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

    def solve(self, a: FuzzySet, b: float) -> list:
        if self.is_solution_empty(a, b):
            return []
        base = self.base_solution(a, b)
        answer = []
        for branch_solution in self.branch_solutions(a, b):
            branch_answer = self.make_intervals(base, branch_solution)
            answer.append(branch_answer)
        
        return answer
    

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
    

if __name__ == '__main__':
    from .simple_equation_solver import ProductSimpleEquationSolver

    solver = ProductPolynomialEquationSolver(ProductSimpleEquationSolver())
    print(
        solver.solve(
            FuzzySet(
                {
                    'x1': 0.2,
                    'x2': 0.7,
                    'x3': 0.0,
                    'x4': 0.5
                }
            ),
            0.4
        )
    )
        