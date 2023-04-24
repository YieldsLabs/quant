from functools import lru_cache
import inspect
from numbers import Number


def extract_nested_instances(instance):
    nested_instances = []
    for _, attr_value in instance.__dict__.items():
        if isinstance(attr_value, list):
            for item in attr_value:
                if isinstance(item, tuple) and len(item) > 0:
                    nested_instance = item[0]
                    nested_instances.append(nested_instance)
        elif hasattr(attr_value, "__dict__"):
            nested_instances.extend(extract_nested_instances(attr_value))
    return nested_instances


@lru_cache(100)
def extract_numeric_params(instance):
    numeric_params = []
    nested_params = {}
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

    nested_instances = extract_nested_instances(instance)

    for nested_instance in nested_instances:
        nested_params.update(extract_numeric_params(nested_instance))

    for param in signature.parameters.values():
        value = None
        if param.default is not inspect._empty:
            value = param.default
        if param.name in bound_arguments.arguments:
            value = bound_arguments.arguments[param.name]

        value = nested_params.get(param.name, value)

        if value is not None and isinstance(value, Number):
            numeric_params.append((param.name, value))

    return numeric_params


def meta_label(cls):
    def new_str_method(self):
        suffix = super(cls, self).__str__()
        numeric_params = extract_numeric_params(self)
        params = ':'.join(str(v) for _, v in numeric_params)
        return f'{suffix}{params}'

    cls.__str__ = new_str_method
    return cls
