
class BaseException(Exception):
    pass
    
class StopPathIteration(Exception):
    
    def __init__(self, haystack, status=None):
        self.haystack = haystack
        self.status = status
        
    def get(self):
        return self.haystack, self.status