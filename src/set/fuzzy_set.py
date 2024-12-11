######################################################################################################
# Лабораторная работа 1 по дисциплине ЛОИС
# Выполненая студентами группы 221701 БГУИР Глёза Егором Дмитриевичем и Крупским Артёмом Викторович
#
# Класс нечёткого множества
#
# Источники:
# 
# - Нечёткая логика: алгебраическая основы и приложения: Монография / С.Л. Блюмин, И.А. Шуйкова,
#   П.В. Сараев, И.В. Черпаков. - Липецк: ЛЭГИ, 2002. - 111с. 
#
# 1.11.2024
#
from __future__ import annotations

from typing import Any

import numpy as np 
import pandas as pd


class FuzzySet:
    def __init__(
        self,
        membership: dict[Any, float] = None,
        domain: list | None = None,
    ) -> None:
        if domain is None:
            self._membership = pd.Series(membership)
            return
            
        self._membership = dict.fromkeys(domain, 0.)
        
        if membership is not None:
            for e in membership:
                if e not in domain:
                    raise ValueError()
            
            self._membership.update(membership)
            
        self._membership = pd.Series(self._membership)
    
    @property
    def domain(self) -> np.ndarray:
        return self._membership.index.to_numpy()
    
    @property
    def membership(self) -> np.ndarray:
        return self._membership.to_numpy()
    
    def is_empty(self) -> bool:
        return np.all(self.membership == 0)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FuzzySet):
            return False
        
        return np.array_equal(value.domain, self.domain) and np.array_equal(value.membership, self.membership)
    
    def __iter__(self):
        return iter(self._membership.to_dict().items())
    
    def __getitem__(self, item: Any):
        return self._membership[item]
    
    def __setitem__(self, item: Any, value: float):
        self._membership[item] = value

    def __gt__(self, other: FuzzySet):
        if not isinstance(other, FuzzySet):
            return False
        return np.all(self.membership > other.membership)
    
    def __lt__(self, other: FuzzySet):
        if not isinstance(other, FuzzySet):
            return False
        return np.all(self.membership < other.membership)
    
    def __eq__(self, other: FuzzySet):
        if not isinstance(other, FuzzySet):
            return False
        return np.array_equal(self.membership, other.membership)
    
    def __str__(self) -> str:
        return f'{{{ ", ".join(f"<{x}, {y}>" for x, y in self._membership.items()) }}}'
    
    
if __name__ == '__main__':
    s = FuzzySet(
        {
            'a': 0.2,
            'b': 0.8,
            'c': 0.43
        },
        ['a', 'b', 'c', 'd']
    )
    print(s)
    print(s.domain)
    print(s.membership)
    