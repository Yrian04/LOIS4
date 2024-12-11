######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс парсера
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from enum import Enum

from pyparsing import Word, alphas, nums, Literal, Group, Optional, Combine, delimitedList, LineEnd, Char, alphanums, ParseException, ParserElement, Suppress

from .set import FuzzySet
from .map import FuzzyMap

ParserElement.set_default_whitespace_chars("")

class Parser:
    class tags(Enum):
        NAME = '0'
        CONSEQUENT = 1
        RULE = 2

    def __init__(
        self,
    ):
        # Определение базовых элементов
        letter = Char(alphas)
        digits = Word(nums)
        symbols = Word(alphanums)
        dot = Literal('.')
        zero = Literal('0')
        one = Literal('1')
        degree = Combine((one + Optional(dot + Word('0'))) | (zero + Optional(dot + digits))).set_parse_action(lambda toks: float(toks[0]))

        separators = Suppress(Word(' '))
        new_line = Suppress(LineEnd())
        name = Combine(letter + Optional(symbols))

        # Элементы таблицы
        first_domain_elements = Group(delimitedList(name, separators))
        second_domain_elements = Group(delimitedList(name, separators))
        
        truth_degree_сonsequent_table = Group(delimitedList(degree, separators))
        rule_table_row = Group(delimitedList(degree, separators))
        truth_degree_rule_table = Group(delimitedList(rule_table_row, new_line))

        # Таблицы
        header = (name + new_line + new_line).set_parse_action(lambda toks: (self.tags.NAME, toks[0]))
        сonsequent_table = Group(second_domain_elements + new_line + truth_degree_сonsequent_table + new_line, True).set_parse_action(lambda toks: (self.tags.CONSEQUENT, toks[0]))
        rule_table = Group(first_domain_elements + new_line + truth_degree_rule_table + new_line, True).set_parse_action(lambda toks: (self.tags.RULE, toks[0]))

        # Общая грамматика базы знаний
        self.knowledge_base_grammar = header +\
            ((сonsequent_table + new_line + rule_table) | (rule_table + new_line + сonsequent_table))

    def parse(self, text: str) -> tuple[str, FuzzySet, FuzzyMap]:
        tokens = dict(self.knowledge_base_grammar.parseString(text, True).as_list())
        codomain = tokens[self.tags.CONSEQUENT][0]
        consequent = FuzzySet(
            dict(
                zip(
                    codomain,
                    tokens[self.tags.CONSEQUENT][1],
                )
            )
        )
        domain = tokens[self.tags.RULE][0]
        rule = FuzzyMap(
            dict(
                {x: {y: tokens[self.tags.RULE][1][j][i] for j, y in enumerate(codomain)} for i, x in enumerate(domain)}
            ),
        )
        return tokens[self.tags.NAME], consequent, rule
    

if __name__ == '__main__':
    text = """isTall

x1  x2  x3
1   0   0
0.5 0.3 0.2

y1 y2
1  0.5
"""
    lexer = Parser()
    try:
        print(text)
        print(*lexer.parse(text), sep='\n')
    except ParseException as e:
        print(e)