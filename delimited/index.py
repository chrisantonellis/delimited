import abc
import copy


class SequenceIndex(abc.ABC):
    sequence = None
    
    def __init__(self, index):
        if not isinstance(index, int):
            raise TypeError(index)
        self.index = index
        
    def __str__(self):
        return str(self.index)
        
    def __repr__(self):
        return f'{self.__class__.__name__}({self.index})'


class ListIndex(SequenceIndex):
    sequence = list
