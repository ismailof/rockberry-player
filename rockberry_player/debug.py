from functools import wraps


# TODO: Change prints for debugs ?
def debug_function(_function_):
    @wraps(_function_)
    def wrapper(*args, **kwargs):
        print('[CALL] {}, args: {}, kwargs: {}'.format(
            _function_.__name__, args, kwargs)
        )

        try:
            return_value = _function_(*args, **kwargs)
        except Exception as ex:
            print('[EXCEPTION] {} \n {}'.format(
                _function_.__name__, ex)
            )
            return None

        if return_value is not None:
            print('[RETURN] {} returned {} {}'.format(
                _function_.__name__,
                return_value,
                type(return_value))
            )
            return return_value

    return wrapper
