# Copyright (c) 2009, 2012 Dusty Phillips <dusty@linux.ca>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from optparse import OptionParser
import inspect

__version__ = "0.4"


def opterate(func):
    '''A decorator for a main function entry point to a script. It tries to
    automatically generate the options for the main entry point based on the
    arguments, keyword arguments, and docstring.

    All keyword arguments in the function definition are options. Positional
    arguments are mandatory arguments.  Varargs become a variable length (zero
    allowed) list of positional arguments. Varkwargs are currently not
    supported/translated.

    The default value assigned to a keyword argument helps determine the type
    of option and action. The defalut value is assigned directly to the option
    parser's default for that option. In addition, it determines the
    OptionParser action -- a default value of False implies store_true, while
    True implies store_false. If the default value is a list, the action is
    append (multiple instances of that option are permitted). Strings or None
    imply a store action.

    Options are further defined in the docstring. The top part of the docstring
    becomes the usage message for the app. Below that, :param: lines in the
    following format describe the option:

    :param variable_name: -v --verbose the help_text for the variable
    :param variable_name: -v the help_text no long option
    :param variable_name: --verbose the help_text no short option

    the format is:
    :param name: [short option and/or long option] help text

    Variable_name is the name of the variable in the function specification and
    must refer to a keyword argument. All options must have a :param: line like
    this. If you can have an arbitrary length of positional arguments, add a
    *arglist variable; It can be named with any valid python identifier.

    See opterator_test.py for some examples.'''
    argnames, varargs, varkw, defaults = inspect.getargspec(func)

    if defaults:
        positional_params = argnames[:-1 * len(defaults)]
        kw_params = argnames[-1 * len(defaults):]
    else:
        positional_params = argnames
        kw_params = []

    usage_text = ''
    parameters = {}
    if func.__doc__:
        param_doc = func.__doc__.split(':param')
        usage_text = param_doc.pop(0).strip()
        parameters = {}
        for param in param_doc:
            param_args = param.split()
            variable_name = param_args.pop(0)[:-1]
            parameters[variable_name] = param_args

    usage = "%prog [options]"
    if positional_params:
        usage += " " + " ".join(positional_params)
    if varargs:
        usage += " [%s]" % varargs
    usage += "\n\n%s" % usage_text

    option_names = []
    parser = OptionParser(usage)
    for variable_name in kw_params:
        option_strings = []
        param_args = parameters.get(variable_name, [])
        option_names.append(variable_name)
        if not param_args or not param_args[0].startswith('-'):
            option_strings.append('--' + variable_name)
            option_strings.append('-' + variable_name[0])
        while param_args and param_args[0].startswith('-'):
            option_strings.append(param_args.pop(0))
        help_text = ' '.join(param_args)

        if variable_name not in kw_params:
            raise ValueError('%s is not a valid :param: name.'
                    ':params: must match keyword argumentnames in the'
                    'function signature.' % variable_name)

        default = None
        if variable_name in kw_params:
            default = defaults[kw_params.index(variable_name)]

        if default == False:
            action = 'store_true'
        elif default == True:
            action = 'store_false'
        elif type(default) in (list, tuple):
            action = 'append'
        else:
            action = 'store'

        parser.add_option(action=action, default=default, help=help_text,
                dest=variable_name, *option_strings)

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
