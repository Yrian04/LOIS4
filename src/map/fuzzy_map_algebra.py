######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс алгебры нечётких соответствий
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from itertools import product

import numpy as np

from .fuzzy_map import FuzzyMap
from ..set import FuzzySet, FuzzySetAlgebra


class FuzzyMapAlgebra:
    def __init__(
        self,
        set_algebra: FuzzySetAlgebra
    ) -> None:
        self.algebra = set_algebra
        
    def composition(
        self,
        a: FuzzyMap | FuzzySet,
        b: FuzzyMap
    ) -> FuzzyMap | FuzzySet:
        if isinstance(a, FuzzySet):
            return self._set_composition(a, b)
        
        if set(a.codomain) != set(b.domain):
            raise ValueError(f'codomain of\n{a}\nmust be equal to domain of\n{b}')
        
        result = FuzzyMap(
            domain=a.domain,
            codomain=b.codomain
        )
        
        for x in result.index:
            for y in result.columns:
                result[(x, y)] = self.algebra.intersection(a.xcut(x), b.ycut(y)).membership.max()
                
        return result
    
    def consequens(self, a: FuzzySet, b: FuzzySet) -> FuzzyMap:
        result = FuzzyMap(
            domain=a.domain,
            codomain=b.domain
        )
        
        for (a_i, m_a_i), (b_j, m_b_j) in product(a, b):
            result[a_i, b_j] = self.algebra.logic_algebra.impication(m_a_i, m_b_j)
            
        return result
    
    def _set_composition(
        self,
        a: FuzzySet,
        b: FuzzyMap
    ) -> FuzzyMap:
        if set(a.domain) != set(b.domain):
            raise ValueError(f'domain of {a} must be equal to domain of\n{b}')
        
        result = FuzzySet(
            domain=b.codomain,
        )
        
        for x in result.domain:
            result[x] = self.algebra.intersection(a, b.ycut(x)).membership.max()
                
        return result
