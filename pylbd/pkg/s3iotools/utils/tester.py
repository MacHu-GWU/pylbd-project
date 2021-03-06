# -*- coding: utf-8 -*-


def is_instance_or_subclass(val, class_):
    """
    Return True if ``val`` is either a subclass or instance of ``class_``.
    """
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)
