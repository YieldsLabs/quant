import inspect
from cachetools import cached, LRUCache


@cached(cache=LRUCache(maxsize=1000))
def extract_numeric_params(instance):
    numeric_params = []
    signature = inspect.signature(instance.__class__.__init__)

    bound_arguments = {}
    for name in signature.parameters:
        if name in instance.__dict__:
            bound_arguments[name] = instance.__dict__[name]
        else:
            for _, attr_value in instance.__dict__.items():
                if hasattr(attr_value, "__dict__") and name in attr_value.__dict__:
                    bound_arguments[name] = attr_value.__dict__[name]
                    break

    bound_arguments = signature.bind_partial(**bound_arguments)
    bound_arguments.apply_defaults()

    for param in signature.parameters.values():
        value = None
        if param.default is not inspect._empty:
            value = param.default
        if param.name in bound_arguments.arguments:
            value = bound_arguments.arguments[param.name]

        if value is not None and isinstance(value, (int, float)):
            numeric_params.append((param.name, value))
        elif value is not None and hasattr(value, "__dict__"):
            numeric_params.extend(extract_numeric_params(value))
        elif value is not None and isinstance(value, type) and issubclass(value, object):
            nested_instance = None
            if param.name in instance.__dict__:
                nested_instance = instance.__dict__[param.name]
            elif param.name in bound_arguments.arguments:
                nested_instance = bound_arguments.arguments[param.name]
            if nested_instance is not None:
                numeric_params.extend(extract_numeric_params(nested_instance))
            else:
                nested_class = value
                nested_params = extract_numeric_params(nested_class(**bound_arguments.arguments))
                numeric_params.extend(nested_params)

    return numeric_params


def meta_label(cls):
    def new_str_method(self):
        suffix = super(cls, self).__str__()
        numeric_params = extract_numeric_params(self)
        params = ':'.join(str(v) for _, v in numeric_params)
        return f'{suffix}{params}'

    cls.__str__ = new_str_method
    return cls
