import os

if os.name == 'nt':
    from . import nt
    globals().update(nt.__dict__)
else:
    from . import posix
    globals().update(posix.__dict__)
