def deduplicate(iterable):
    """
    Yields deduplicated values, in original order.

    The values of iterable must be hashable
    """
    seen = set()
    for val in iterable:
        if val not in seen:
            seen.add(val)
            yield val
