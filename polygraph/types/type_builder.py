from functools import wraps

type_builder_registry = {}


def type_builder_cache(method):
    @wraps(method)
    def wrapper(cls, *args):
        unique_args = frozenset(args)
        if (cls, unique_args) in type_builder_registry:
            return type_builder_registry[(cls, unique_args)]
        else:
            return_val = method(cls, *args)
            type_builder_registry[(cls, unique_args)] = return_val
            return return_val
    return wrapper


class TypeBuilderMeta(type):
    def __getitem__(self, value):
        try:
            return self.__new__(self, *value)
        except TypeError:
            return self.__new__(self, value)
