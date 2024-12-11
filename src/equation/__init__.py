######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Инициализация модуля equation
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from .simple_equation_solver import SimpleEquationSolver, ProductSimpleEquationSolver
from .polynomial_equation_solver import PolynomialEquationSolver, ProductPolynomialEquationSolver
from .system_equation_solver import SystemEquationSolver


__all__ = [
    'SimpleEquationSolver',
    'ProductSimpleEquationSolver',
    'PolynomialEquationSolver',
    'ProductPolynomialEquationSolver',
    'SystemEquationSolver'
]
