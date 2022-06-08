import sys


def inspect_type(func):
    if '.' not in func.__qualname__:
        ftype = 'function'
    else:
        # __qualname__: 'className.functioNname'
        cls_name = func.__qualname__.rsplit('.', 1)[0]
        # Get the class by name
        cls = getattr(sys.modules[func.__module__], cls_name)
        # cls.__dict__[func.__name__] should return like <class 'staticmethod'>
        func_name = func.__name__
        if func.__name__.startswith('__'):
            func_name = f"_{cls_name}{func.__name__}"

        ftype = cls.__dict__[func_name].__class__.__name__
        if ftype not in ['staticmethod', 'classmethod', 'function']:
            raise TypeError('Unknown Type %s, Please check input is method or function' % func)
    return ftype
