from functools import wraps


def debug_function(_function_):
    @wraps(_function_)
    def wrapper(*args, **kwargs):
        print('[CALL] %r, args: %r, kwargs: %s' % (_function_.__name__,
                                                   args,
                                                   kwargs))
        return_value = _function_(*args, **kwargs)
        if return_value is not None:
            print('[RETURN] %r returned %r %r' % (_function_.__name__,
                                                  return_value,
                                                  type(return_value)))
            return return_value

    return wrapper
