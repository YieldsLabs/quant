import inspect
from cachetools import cached

@cached(cache={})
def extract_numeric_params(instance):
    numeric_params = []
    signature = inspect.signature(instance.__class__.__init__)
    for param in signature.parameters.values():
        if param.default is not inspect._empty:
            value = param.default
        elif param.name in instance.__dict__:
            value = instance.__dict__[param.name]
        else:
            continue
        if isinstance(value, (int, float)):
            numeric_params.append((param.name, value))
        elif hasattr(value, "__dict__"):
            numeric_params.extend(extract_numeric_params(value))
    return numeric_params


def has_default_arguments(cls):
    members = inspect.getmembers(cls)
    for name, value in members:
        if name == "__init__":
            signature = inspect.signature(value)
            for param in signature.parameters.values():
                if param.default is not inspect._empty:
                    return True
            return False
    return False


def meta_label(cls):
    def new_str_method(self):
        suffix = super(cls, self).__str__()
        numeric_params = extract_numeric_params(self)
        params = ':'.join(str(v) for _, v in numeric_params)
        return f'{suffix}{params}'

    cls.__str__ = new_str_method
    return cls
