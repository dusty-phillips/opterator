from optparse import OptionParser
import inspect
import sys

def opterate(func):
    '''A decorator for a main function entry point to a script. It tries to
    automatically generate the options for the main entry point based on the
    arguments, keyword arguments, and docstring.
    
    All keyword arguments in the function definition are options. Positional
    arguments are mandatory arguments.  Varargs become a variable length (zero
    allowed) list of positional arguments. Varkwargs are currently not
    supported/translated.

    Options are further defined in the docstring. The top part of the docstring
    becomes the usage message for the app. Below that, @param lines in the
    following format describe the option:

    @param variable_name store_true -v --verbose the help_text for the variable
    @param variable_name store -v the help_text no long option
    @param variable_name store_false -verbose the help_text no short option

    the format is:
    @param name action [short option and/or long option] help text

    Variable_name is the name of the variable in the function specification and
    must refer to a keyword argument. All options must have an @param line like
    this. If you can have an arbitrary length of positional arguments, add a
    *arglist variable; It can be named with any valid python identifier.

    See opterator_test.py for some examples.'''
    argnames, varargs, varkw, defaults = inspect.getargspec(func)

    if defaults:
        positional_params = argnames[:-1*len(defaults)]
        kw_params = argnames[-1*len(defaults):]
    else:
        positional_params = argnames
        kw_params = []

    usage_text = ''
    parameters = []
    if func.func_doc:
        parameters = func.func_doc.split('@param')
        usage_text = parameters.pop(0)

    usage = "%prog [options]"
    if positional_params:
        usage += " " + " ".join(positional_params)
    if varargs:
        usage += " [%s]" % varargs
    usage += "\n\n%s" % usage_text

    option_names = []
    parser = OptionParser(usage)
    for param in parameters:
        param_args = param.split()
        variable_name = param_args.pop(0)
        option_names.append(variable_name)
        action = param_args.pop(0)
        long_name = short_name = None
        #FIXME: Tired! This is way uglier than it needs be.
        if param_args[0].startswith('--'):
            long_name = param_args.pop(0)
        if param_args[0].startswith('-'):
            short_name = param_args.pop(0)
        if param_args[0].startswith('--'):
            long_name = param_args.pop(0)
        help_text = ' '.join(param_args)

        if variable_name not in kw_params:
            raise ValueError('%s is not a valid @param name.'
                    '@params must match keyword argumentnames in the'
                    'function signature.' % variable_name)

        default = None
        if variable_name in kw_params:
            default = defaults[kw_params.index(variable_name)]

        parser.add_option(short_name, long_name, action=action,
                default=default, help=help_text, dest=variable_name)

    def wrapper(argv=None):
        options, positional = parser.parse_args(argv)
        processed_args = []

        for arg_name in argnames:
            if arg_name in option_names:
                option_value = getattr(options, arg_name)
                if not option_value and arg_name not in kw_params:
                    parser.error('%s is required.' % arg_name)

                processed_args.append(option_value)
            else:
                if positional:
                    processed_args.append(positional.pop(0))
                else:
                    parser.error('Not enough arguments.')

        processed_args += positional

        if len(processed_args) > len(argnames) and not varargs:
            parser.error('Too many arguments.')

        func(*processed_args)
    return wrapper
