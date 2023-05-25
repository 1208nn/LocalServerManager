import os

if os.name == 'nt':
    from . import nt
    self = nt
else:
    from . import posix
    self = posix
globals().update(self.__dict__)
