class Field:
    def __init__(self, name, return_type, description=None,
                 arg_types=None, deprecation_reason=None):
        self.name = name
        self.return_type = return_type
        self.description = description
        self.arg_types = arg_types
        self.deprecation_reason = deprecation_reason
        self.is_deprecated = bool(deprecation_reason)
