######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Основной модуль программы
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from .equation import (
    ProductSimpleEquationSolver,
    ProductPolynomialEquationSolver,
    SystemEquationSolver
)
from .logic import FuzzyLogicAlgebra
from .set import FuzzySetAlgebra
from .parser import Parser


def main(input_file: str):
    with open(input_file) as f:
        input = f.read()
    parser = Parser()
    name, consequent, rule = parser.parse(input)

    logic_algebra = FuzzyLogicAlgebra()
    set_algebra = FuzzySetAlgebra(logic_algebra)
    simple_solver = ProductSimpleEquationSolver()
    polynomial_solver = ProductPolynomialEquationSolver(simple_solver)
    system_solver = SystemEquationSolver(polynomial_solver, set_algebra)

    answer = system_solver.solve(rule, consequent)

    if not answer:
        print("No solutions")
        return

    print('U'.join('(' + 'x'.join(str(x) for x in branch) + ')' for branch in answer) + ' э <' + 
          ','.join(f"{name}({x})" for x in rule.domain) + '>')
    

if __name__ == '__main__':
    main('input.txt')