def dec_with_param(title):
    def decorator(func):
        def wraps(*args, **kwargs):
            print(f'before {title}')
            func(*args, **kwargs)
            print(f'after {title}')
            return

        return wraps

    return decorator


@dec_with_param(title='complex print')
def print_hello(name: str):
    print(f"Hello {name}!")


print_hello('Kate')
