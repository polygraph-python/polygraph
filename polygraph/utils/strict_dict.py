class StrictDict(dict):
    """
    A dictionary that raises an exception if attempting to associate a known
    key with a different value
    """
    def __setitem__(self, key, item):
        if key in self and self[key] != item:
            raise ValueError(
                "Attempting to set {} to a different value {}".format(key, item)
            )
        return super().__setitem__(key, item)
