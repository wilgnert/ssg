def pass_arguments(arg_names, arg_list):
    def replace(func):
        def wrapper(self):
            err = None
            failed_args = []
            s = ""
            for arg in arg_list:
                z = dict(zip(arg_names, arg))
                try:
                    func(self, **z)
                    s += "."
                except AssertionError as e:
                    s += "F"
                    failed_args.append(z)
                    err = e
            print(f"Subtests of {func.__qualname__}: {s}")
            if failed_args:
                print(f"Failed arguments: {failed_args}")
            if err:
                raise err

        return wrapper

    return replace