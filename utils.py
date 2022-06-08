import inspect
import sys


def inspect_type(func):
    if '.' not in func.__qualname__:
        ftype = 'function'
        # print('Normal function')
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


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth) or (
            inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__,
                                                                                                '__class__', None)):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects
