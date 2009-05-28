from opterator import opterate
import py


class Checker(object):
    '''Just something to get closure-like behaviour so I can call the internal
    function and set or check values to ensure the decorator is behaving
    correctly.'''
    pass

def test_noargs():
    '''Ensure a method that expects no arguments runs properly when it receives
    none.'''
    result = Checker()
    @opterate
    def main():
        result.x = 5
    main([])
    assert result.x == 5

def test_noarg_help():
    '''assert that a help message is shown when -h is passed.'''
    capture = py.io.StdCapture()
    @opterate
    def main():
        '''a docstring'''
        pass
    py.test.raises(SystemExit, main, ['-h'])
    out, error = capture.reset()
    assert error == ''
    assert out.strip() == """Usage: py.test [options]

a docstring

Options:
  -h, --help  show this help message and exit"""

def test_noarg_invalid():
    '''Ensure that passing an illegal argument is caught as such.'''
    capture = py.io.StdCapture()
    @opterate
    def main():
        '''a docstring'''
        pass
    py.test.raises(SystemExit, main, ['--invalidopt'])
    out, error = capture.reset()
    assert out == ''
    assert error.strip() == ('Usage: py.test [options]'
            '\n\na docstring\n\n'
            'py.test: error: no such option: --invalidopt')

def test_noarg_param():
    '''Ensure that passing a parameter is rejected.'''
    capture = py.io.StdCapture()
    @opterate
    def main():
        '''a docstring'''
        pass
    py.test.raises(SystemExit, main, ['invalidarg'])
    out, error = capture.reset()
    assert out == ''
    assert error.strip() == ('Usage: py.test [options]'
            '\n\na docstring\n\n'
            'py.test: error: Too many arguments.')

def test_var_positional_noopts():
    '''Try passing a list of positional arguments to the function.'''
    result = Checker()
    @opterate
    def main(*filenames):
        '''list files in a directory.'''
        result.filenames = filenames
    filenames = ['file1', 'file2', 'file3']
    main(filenames)
    assert list(result.filenames) == filenames

def test_var_positional_help():
    capture = py.io.StdCapture()
    @opterate
    def main(*filenames):
        'list files'
        pass
    py.test.raises(SystemExit, main,
            ['--help'])
    out, error = capture.reset()
    assert error == ''
    assert out.strip() == ('Usage: py.test [options] [filenames]'
            '\n\nlist files\n\n'
            'Options:\n  -h, --help  show this help message and exit')

def test_required_positional():
    result = Checker()
    @opterate
    def main(source, dest):
        'move a file'
        result.source = source
        result.dest = dest
    main(['sourcename', 'destname'])
    assert result.source == 'sourcename'
    assert result.dest == 'destname'

def test_too_many_positional():
    capture = py.io.StdCapture()
    @opterate
    def main(source, dest):
        'copy a file'
        pass
    py.test.raises(SystemExit, main,
            ['sourcename', 'destname', 'somethingextra'])
    out, error = capture.reset()
    assert out == ''
    assert error.strip() == ('Usage: py.test [options] source dest'
            '\n\ncopy a file\n\n'
            'py.test: error: Too many arguments.')

def test_not_enough_positional():
    capture = py.io.StdCapture()
    @opterate
    def main(source, dest):
        'copy a file'
        pass
    py.test.raises(SystemExit, main,
            ['sourcename'])
    out, error = capture.reset()
    assert out == ''
    assert error.strip() == ('Usage: py.test [options] source dest'
            '\n\ncopy a file\n\n'
            'py.test: error: Not enough arguments.')

def test_keyword_option():
    result = Checker()
    @opterate
    def main(myoption='novalue'):
        '''A script with one optional option.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption

    main(['-m', 'avalue'])
    assert result.myoption == 'avalue'

def test_keyword_option_helptext():
    capture = py.io.StdCapture()
    @opterate
    def main(myoption='novalue'):
        '''A script with one optional option.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption
    py.test.raises(SystemExit, main, ['-h'])
    out, error = capture.reset()
    print out
    assert error == ''
    assert out.strip() == """Usage: py.test [options]

A script with one optional option.

Options:
  -h, --help            show this help message and exit
  -m MYOPTION, --mine=MYOPTION
                        the myoption helptext"""

def test_short_option_only():
    result = Checker()
    @opterate
    def main(myoption='novalue'):
        '''A script with one optional option.
        @param myoption store -m the myoption helptext'''
        result.myoption = myoption

    main(['-m', 'avalue'])
    assert result.myoption == 'avalue'

def test_long_option_only():
    result = Checker()
    @opterate
    def main(myoption='novalue'):
        '''A script with one optional option.
        @param myoption store --mine the myoption helptext'''
        result.myoption = myoption

    main(['--mine', 'avalue'])
    assert result.myoption == 'avalue'
    
def test_keyword_option_is_optional():
    result = Checker()
    @opterate
    def main(myoption='novalue'):
        '''A script with one optional option.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption

    main([])
    assert result.myoption == 'novalue'

def test_required_arg_kw_option():
    result = Checker()
    @opterate
    def main(firstarg, myoption='novalue'):
        '''A script with one required argument and one optional value.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption
        result.firstarg = firstarg

    main(['-m', 'avalue', 'thearg'])
    assert result.myoption == 'avalue'
    assert result.firstarg == 'thearg'

def test_required_arg_kw_option_is_optional():
    result = Checker()
    @opterate
    def main(firstarg, myoption='novalue'):
        '''A script with one required argument and one optional value.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption
        result.firstarg = firstarg

    main(['thearg'])
    assert result.myoption == 'novalue'
    assert result.firstarg == 'thearg'

def test_varargs_kw_option():
    result = Checker()
    @opterate
    def main(myoption='novalue', *someargs):
        '''A script with one required argument and one optional value.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption
        result.someargs = someargs

    main(['-m', 'avalue', 'anarg', 'thearg'])
    assert result.myoption == 'avalue'
    assert result.someargs == ('anarg', 'thearg')

def test_varargs_kw_option_is_optional():
    result = Checker()
    @opterate
    def main(myoption='novalue', *someargs):
        '''A script with one required argument and one optional value.
        @param myoption store -m --mine the myoption helptext'''
        result.myoption = myoption
        result.someargs = someargs

    main(['anarg', 'thearg'])
    assert result.myoption == 'novalue'
    assert result.someargs == ('anarg', 'thearg')

def test_two_kw_options():
    result = Checker()
    @opterate
    def main(myoption='novalue', secondoption=False):
        '''A script with one required argument and one optional value.
        @param myoption store -m --mine the myoption helptext
        @param secondoption store_true -s --second the second helptext'''
        result.myoption = myoption
        result.secondoption = secondoption

    main(['-m', 'avalue', '--second'])
    assert result.myoption == 'avalue'
    assert result.secondoption == True

def test_comprehensive_example():
    result = Checker()
    @opterate
    def main(filename1, filename2, recursive=False, interactive=False,
            suffix='~', *other_filenames):
        '''An example copy script with some example parameters borrowed from
        the cp man page. Illustrates some of the simplicity and pitfalls of
        this option parsing method.
        
        @param recursive store_true -r --recursive copy directories
            recursively
        @param interactive store_true -i --interactive prompt before
            overwrite
        @param suffix store -S --suffix override the usual backup
            suffix '''
        # When two filenames are required and others optional you have to build
        # funny lists like this.
        filenames = [filename1, filename2] + list(other_filenames)
        destination = filenames.pop()
        # call function that does the actual checking, copying, like with any
        # option parsed app.
        # 
        # ...
        result.filename1 = filename1
        result.filename2 = filename2
        result.recursive = recursive
        result.interactive = interactive
        result.suffix = suffix
        result.other_filenames = other_filenames

    capture = py.io.StdCapture()
    py.test.raises(SystemExit, main, ['-h'])
    out, error = capture.reset()
    print out

    assert error == ''
    assert out.strip() == '''Usage: py.test [options] filename1 filename2 [other_filenames]

An example copy script with some example parameters borrowed from
        the cp man page. Illustrates some of the simplicity and pitfalls of
        this option parsing method.

Options:
  -h, --help            show this help message and exit
  -r, --recursive       copy directories recursively
  -i, --interactive     prompt before overwrite
  -S SUFFIX, --suffix=SUFFIX
                        override the usual backup suffix'''


    main(['source', 'dest'])
    assert result.filename1 == 'source'
    assert result.filename2 == 'dest'
    assert result.recursive == False
    assert result.interactive == False
    assert result.suffix == '~'
    assert not result.other_filenames

    main(['source', 'dest', '-r'])
    assert result.filename1 == 'source'
    assert result.filename2 == 'dest'
    assert result.recursive == True
    assert result.interactive == False
    assert result.suffix == '~'
    assert not result.other_filenames

    main(['-i', 'source', 'dest', '-r', 'another', 'directory'])
    assert result.filename1 == 'source'
    assert result.filename2 == 'dest'
    assert result.recursive == True
    assert result.interactive == True
    assert result.suffix == '~'
    assert result.other_filenames == ('another', 'directory')
