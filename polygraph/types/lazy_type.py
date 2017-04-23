import importlib
import inspect


class LazyType:
    """
    Defines a type that is lazily imported at runtime. Used mainly to resolve
    circular definitions (e.g. object fields whose return type is the object itself)
    """
    def __init__(self, class_name, module_name=None):
        self.class_name = class_name
        if not module_name:
            # Try and get module from which LazyType was declared
            frame = inspect.stack()[1]
            module_name = inspect.getmodule(frame[0]).__name__
        self.module_name = module_name

    def resolve_type(self):
        module = importlib.import_module(self.module_name)
        class_ = getattr(module, self.class_name)
        return class_

    def __call__(self, *args, **kwargs):
        return self.resolve_type()(*args, **kwargs)
