class ParserUtils:
    def __init__(self):
        pass

    def is_int(self, n):
        if not self.is_not_bool(n):
            return False
        if n == True:
            return False
        if n == False:
            return False
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    def is_not_bool(self, s):
        return s not in ['True', 'False']

    def parse_arguments(self, arguments, positional_args=[], optional_pos_args=[]):
        arguments = list(arguments)

        pos = dict()
        opt = dict()
        fil = dict()

        for arg in arguments:
            if len(positional_args) > 0:
                pos[positional_args[0]] = arg
                positional_args.pop(0)

            elif arg[0] == '-':
                if '=' in arg:
                    split_opt = arg.split('=')
                    if len(split_opt) < 2:
                        opt[split_opt[0]] = ''
                    else:
                        opt[split_opt[0]] = split_opt[1]
                else:
                    opt[arg] = True

            elif len(optional_pos_args) > 0:
                pos[optional_pos_args[0]] = arg
                optional_pos_args.pop(0)

        if len(positional_args) > 0:
            return None

        return {'pos':pos, 'opt':opt, 'fil':fil}

    def get_option(self, options, full_opt, short_opt=None):
        if short_opt is None:
            short_opt = full_opt[0]
        return f'--{full_opt}' in options or f'-{short_opt}' in options

    def get_option_int_value(self, options, full_opt, short_opt=None, default=None):
        if f'--{full_opt}' in options:
            if self.is_int(options[f'--{full_opt}']):
                return int(options[f'--{full_opt}'])
            else:
                return default

        if short_opt is None:
            short_opt = full_opt[0]

        if f'-{short_opt}' in options:
            if self.is_int(options[f'-{short_opt}']):
                return int(options[f'-{short_opt}'])
            else:
                return default

        return None

    def get_option_string_value(self, options, full_opt, short_opt=None, default=None):
        if f'--{full_opt}' in options:
            if self.is_not_bool(options[f'--{full_opt}']):
                return options[f'--{full_opt}']
            else:
                return default

        if short_opt is None:
            short_opt = full_opt[0]

        if f'-{short_opt}' in options:
            if self.is_not_bool(options[f'-{short_opt}']):
                return options[f'-{short_opt}']
            else:
                return default

        return None