######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс нечёткого соответствия
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from typing import Any
from functools import reduce

import numpy as np
import pandas as pd

from ..set import FuzzySet


class FuzzyMap:
    def __init__(
        self,
        cuts: dict[Any, dict[Any, float]] = None,
        *,
        domain: list[Any] = None,
        codomain: list[Any] = None,
    ) -> None:
        if cuts is None:
            if domain is None or codomain is None:
                raise ValueError()
            
            self._matrix = pd.DataFrame(
                data=np.zeros((len(domain), len(codomain))),
                index=domain,
                columns=codomain,
            )
            return
            
        if domain is None:
            domain = cuts.keys()
            
        if codomain is None:
            codomain = reduce(lambda cut1, cut2: cut1 | cut2, cuts.values())
            
        matrix = pd.DataFrame(
            index=domain,
            columns=codomain
        )
        for key in domain:
            membership_dict = {}
            if key in cuts:
                membership_dict = cuts[key]
            
            if not isinstance(membership_dict, dict):
                raise ValueError()
            
            for value in codomain:
                membership = 0.
                if value in membership_dict:
                    membership = membership_dict[value]
                    if not isinstance(membership, float):
                        raise ValueError()
                matrix.loc[key, value] = membership
        self._matrix = matrix
    
    @property
    def domain(self):
        return self._matrix.index.to_numpy()
        
    @property
    def codomain(self):
        return self._matrix.columns.to_numpy()
    
    def xcut(self, x: Any) -> FuzzySet:
        
        if x not in self.domain:
            raise ValueError(f'{x} must be in the domen of\n{self}')
        
        return FuzzySet(self._matrix.loc[x])
        
    def ycut(self, y: Any) -> FuzzySet:
        
        if y not in self.codomain:
            raise ValueError(f'{y} must be in the codomen of\n{self}')
        
        return FuzzySet(self._matrix[y])
    
    def __getitem__(self, item: tuple[Any, Any]) -> float:
        x, y = item
        
        if x not in self.domain:
            raise ValueError(f'{x} must be in the domen of\n{self}')
        
        if y not in self.codomain:
            raise ValueError(f'{y} must be in the codomen of\n{self}')
        
        return self._matrix.loc[item]
         
    def __setitem__(self, item: tuple[Any, Any], value: float) -> None:
        self._matrix.loc[item] = value

    def __iter__(self):
        for x in self.domain:
            yield self._matrix[x]
    
    def __str__(self) -> str:
        return str(self._matrix)
          
                    
if __name__ == '__main__':
    m = FuzzyMap(
        {
            'a': {
                '1': 0.2,
                '2': 0.4,
            },
            'b': {
                '1': 0.9,
            },
        },
        # keys=['a', 'b', 'c'],
        codomain=['1', '2', '3'],
    )             
    print(m)
    print(m.xcut('a'))
    print(m.ycut('1'))
    print(m['a', '1'])      
