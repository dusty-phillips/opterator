# Copyright (c) 2009, 2012, 2014 Dusty Phillips <dusty@buchuki.com>
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


from argparse import ArgumentParser
import inspect
import sys

__version__ = "0.5"


def generate_options():
    '''Helper coroutine to identify short options that haven't been used
    yet. Yields lists of short option (if available) and long option for
    the given name, keeping track of which short options have been previously
    used.

    If you aren't familiar with coroutines, use similar to a generator:
    x = generate_options()
    next(x)  # advance coroutine past its initialization code
    params = x.send(param_name)
    '''
    used_short_options = set()
    param_name = yield
    while True:
        names = ['--' + param_name]
        for letter in param_name:
            if letter not in used_short_options:
                used_short_options.add(letter)
                names.insert(0, '-' + letter)
                break
        param_name = yield names


def portable_argspec(func):
    '''
    Given a function, return a tuple of
    (positional_params, keyword_params, varargs, defaults, annotations)
    where
    * positional_params is a list of parameters that don't have default values
    * keyword_params is a list of parameters that have default values
    * varargs is the string name for variable arguments
    * defaults is a dict of default values for the keyword parameters
    * annotations is a dictionary of param_name: annotation pairs
        it may be empty, and on python 2 will always be empty.

    This function is portable between Python 2 and Python 3, and does some
    extra processing of the output from inspect.
    '''
    if sys.version_info < (3, 0):  # PYTHON 2 MUST DIE
        argnames, varargs, varkw, defaults = inspect.getargspec(func)
        annotations = {}
    else:
        (
            argnames, varargs, varkw, defaults, kwa, kwd, annotations
        ) = inspect.getfullargspec(func)

    kw_boundary = len(argnames) - len(defaults) if defaults else len(argnames)
    positional_params = argnames[:kw_boundary]
    kw_params = argnames[kw_boundary:]
    return positional_params, kw_params, varargs, defaults, annotations


def opterate(func):
    '''A decorator for a main function entry point to a script. It
    automatically generates the options for the main entry point based on the
    arguments, keyword arguments, and docstring.

    All keyword arguments in the function definition are options. Positional
    arguments are mandatory arguments that store a string value.  Varargs
    become a variable length (zero allowed) list of positional arguments.
    Varkwargs are currently ignored.

    The default value assigned to a keyword argument helps determine the type
    of option and action. The defalut value is assigned directly to the
    parser's default for that option. In addition, it determines the
    ArgumentParser action -- a default value of False implies store_true, while
    True implies store_false. If the default value is a list, the action is
    append (multiple instances of that option are permitted). Strings or None
    imply a store action.

    Options are further defined in the docstring. The top part of the docstring
    becomes the usage message for the app. Below that, ReST-style :param: lines
    in the following format describe the option:

    :param variable_name: -v --verbose the help_text for the variable
    :param variable_name: -v the help_text no long option
    :param variable_name: --verbose the help_text no short option

    the format is:
    :param name: [short option and/or long option] help text

    Variable_name is the name of the variable in the function specification and
    must refer to a keyword argument. All options must have a :param: line like
    this. If you can have an arbitrary length of positional arguments, add a
    *arglist variable; It can be named with any valid python identifier.

    See opterator_test.py and examples/ for some examples.'''
    (
        positional_params, kw_params, varargs, defaults, annotations
    ) = portable_argspec(func)

    description = ''
    param_docs = {}
    if func.__doc__:
        param_doc = func.__doc__.split(':param')
        description = param_doc.pop(0).strip()
        for param in param_doc:
            param_args = param.split()
            variable_name = param_args.pop(0)[:-1]
            param_docs[variable_name] = param_args

    parser = ArgumentParser(description=description)
    option_generator = generate_options()
    next(option_generator)

    for param in positional_params:
        parser.add_argument(param, help=" ".join(param_docs.get(param, [])))
    for param in kw_params:
        default = defaults[kw_params.index(param)]
        names = []
        param_doc = []
        if param in annotations:
            names = annotations[param]
        if param in param_docs:
            param_doc = param_docs.get(param, [])
            while param_doc and param_doc[0].startswith('-'):
                names.append(param_doc.pop(0))

        names = names if names else option_generator.send(param)

        option_kwargs = {
            'action': 'store',
            'help': ' '.join(param_doc),
            'dest': param,
            'default': default
        }
        if default is False:
            option_kwargs['action'] = 'store_true'
        elif default is True:
            option_kwargs['action'] = 'store_false'
        elif type(default) in (list, tuple):
            if default:
                option_kwargs['choices'] = default
            else:
                option_kwargs['action'] = 'append'

        parser.add_argument(*names, **option_kwargs)
    if varargs:
        parser.add_argument(varargs, nargs='*')

    def wrapper(argv=None):
        args = vars(parser.parse_args(argv))
        processed_args = [args[p] for p in positional_params + kw_params]
        if varargs:
            processed_args.extend(args[varargs])
        func(*processed_args)
    return wrapper
