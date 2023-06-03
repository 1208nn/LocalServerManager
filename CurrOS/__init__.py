import os


import importlib

globals().update(importlib.import_module(f'.{os.name}', __package__).__dict__)

'''
if os.name == 'nt':
    from . import nt
    globals().update(nt.__dict__)
else:
    from . import posix
    globals().update(posix.__dict__)
'''
