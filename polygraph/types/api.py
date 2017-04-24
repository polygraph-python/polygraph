from polygraph.types.lazy_type import LazyType


def typedef(type_):
    return type_.__type


def get_type_class(class_or_lazy_type):
    if isinstance(class_or_lazy_type, LazyType):
        return class_or_lazy_type.resolve_type()
    else:
        return class_or_lazy_type
