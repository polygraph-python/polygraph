from typing import Iterable


class AttrReprMixin:
    """
    Automagically builds a sensible repr, based on a user-defined list of attributes
    """
    def __repr_attributes__(self) -> Iterable[str]:
        if self.__slots__:
            return self.__slots__
        raise NotImplemented

    def __repr__(self):
        key_values = [
            "{}={}".format(key, getattr(self, key))
            for key in self.__repr_attributes__()
        ]
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(key_values)
        )
